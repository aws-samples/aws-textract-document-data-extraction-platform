#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from dataclasses import dataclass
import urllib.parse
import decimal
import json
from typing import Optional, Dict, Mapping, Any, Generic, TypeVar, TypedDict, List
from aws_lambdas.utils.base64 import base64_decode, base64_encode
from aws_api_python_runtime.api_client import JSONEncoder

from aws_api_python_runtime.schemas import DictSchema

from aws_lambdas.utils.time import utc_now
from aws_api_python_runtime.configuration import Configuration

Document = TypeVar("Document", bound=DictSchema)
T = TypeVar("T")


@dataclass
class PaginationParameters:
    """
    Defines the parameters used for paginated requests
    """

    page_size: int
    next_token: Optional[str]


def to_pagination_parameters(params: Mapping[str, Any]) -> PaginationParameters:
    """
    Given the request parameters for an api call, generate pagination parameters with default values where omitted
    """
    if "pageSize" not in params or params["pageSize"] is None:
        raise Exception("pageSize is required for list operation")

    page_size = int(params["pageSize"])
    next_token = (
        None
        if "nextToken" not in params or params["nextToken"] is None
        else params["nextToken"]
    )
    return PaginationParameters(page_size=page_size, next_token=next_token)


@dataclass
class PaginatedItemsResponse(Generic[T]):
    """
    A response to a paginated request for items
    """

    items: List[T]
    error: Optional[str] = None
    next_token: Optional[str] = None


def to_paginated_response_args(response: PaginatedItemsResponse) -> Dict:
    """
    Given a paginated items response, return the additional arguments used in constructions of the response model
    which inherits from PaginatedResponse, ie set the next_token if present
    """
    args = {}
    if response.next_token is not None:
        args["next_token"] = response.next_token
    return args


def _to_dynamodb_args(**fetch_page_kwargs):
    """
    Returns the kwargs to pass to dynamodb given the kwargs for a page fetch function wrapper, or fetch page function.
    """
    dynamodb_kwargs = {}

    def _update_if_present(dynamo_key: str, fetch_page_key: str):
        if (
            fetch_page_key in fetch_page_kwargs
            and fetch_page_kwargs[fetch_page_key] is not None
        ):
            dynamodb_kwargs[dynamo_key] = fetch_page_kwargs[fetch_page_key]

    _update_if_present("Limit", "limit")
    _update_if_present("ExclusiveStartKey", "exclusive_start_key")
    _update_if_present("KeyConditionExpression", "key_condition_expression")
    _update_if_present("FilterExpression", "filter_expression")
    _update_if_present("ExpressionAttributeValues", "expression_attribute_values")
    _update_if_present("ExpressionAttributeNames", "expression_attribute_names")

    return dynamodb_kwargs


def fetch_page_with_scan(**fetch_page_common_kwargs):
    """
    Fetch a page of results from dynamodb using the scan operation
    """

    def fetch(table, **kwargs):
        return table.scan(**_to_dynamodb_args(**kwargs, **fetch_page_common_kwargs))

    return fetch


def fetch_page_with_query(key_condition_expression, **fetch_page_common_kwargs):
    """
    Fetch a page of results from dynamodb using the query operation
    """

    def fetch(table, **kwargs):
        return table.query(
            **_to_dynamodb_args(
                **kwargs,
                **fetch_page_common_kwargs,
                key_condition_expression=key_condition_expression
            )
        )

    return fetch


def fetch_page_with_query_for_key_equals(key_name: str, key_value: str):
    """
    Fetch a page of results where the partition key attribute has the given value
    :param key_name: name of the partition key attribute
    :param key_value: value of the attribute to query for
    """
    return fetch_page_with_query(
        key_condition_expression="#key = :value",
        expression_attribute_names={"#key": key_name},
        expression_attribute_values={":value": key_value},
    )


class Token(TypedDict):
    """
    Defines a deserialised token
    """

    last_evaluated_key: Dict


def _from_token(next_token: Optional[str]) -> Optional[Token]:
    """
    Deserialise a next token
    """
    if next_token is not None:
        return json.loads(base64_decode(urllib.parse.unquote(next_token)))
    return None


def _to_token(token: Optional[Token]) -> Optional[str]:
    """
    Serialize a next token
    """
    if token is not None:
        return urllib.parse.quote(base64_encode(json.dumps(token)))
    return None


def list_with_pagination_parameters(
    table,
    pagination_parameters: PaginationParameters,
    fetch_page=fetch_page_with_scan(),
) -> PaginatedItemsResponse[Dict]:
    """
    List items from dynamodb according to the given pagination parameters
    :param table: the table to list items from
    :param pagination_parameters: parameters indicating the page of results to fetch
    :param fetch_page: method to fetch a page of results
    :return: a page of items
    """
    try:
        token = _from_token(pagination_parameters.next_token)
    except Exception:
        return PaginatedItemsResponse(items=[], error="Invalid nextToken supplied")

    kwargs = {}
    if token is not None:
        kwargs["exclusive_start_key"] = token["last_evaluated_key"]

    page = fetch_page(table, limit=pagination_parameters.page_size, **kwargs)

    new_token: Optional[Token] = None
    if "LastEvaluatedKey" in page and page["LastEvaluatedKey"] is not None:
        new_token = {"last_evaluated_key": page["LastEvaluatedKey"]}

    return PaginatedItemsResponse(
        items=(page["Items"] if "Items" in page and page["Items"] is not None else []),
        next_token=_to_token(new_token),
    )


def _sanitise_ddb_document_response(item):
    """
    Sanitise numbers returned by dynamodb as decimals into int/float values compatible with our model types
    :param item: item returned from dynamodb
    :return: sanitised item
    """
    if isinstance(item, list):
        for i in range(0, len(item)):
            item[i] = _sanitise_ddb_document_response(item[i])
        return item
    elif isinstance(item, dict):
        for k in item.keys():
            item[k] = _sanitise_ddb_document_response(item[k])
            # setattr(item, k, _sanitise_ddb_document_response(item[k]))
            # item.update({ k: _sanitise_ddb_document_response(item[k]) })
        return item
    elif isinstance(item, decimal.Decimal):
        if item % 1 == 0:
            return int(item)
        else:
            return float(item)
    else:
        return item


decimal_context = decimal.Context(prec=38)


def _sanitise_dict_for_ddb(item):
    """
    Sanitise floats for storage in dynamodb as decimals
    """
    if isinstance(item, list):
        for i in range(0, len(item)):
            item[i] = _sanitise_dict_for_ddb(item[i])
        return item
    elif isinstance(item, dict):
        for k in item.keys():
            item[k] = _sanitise_dict_for_ddb(item[k])
        return item
    elif isinstance(item, float):
        return decimal_context.create_decimal_from_float(item)
    else:
        return item


class Store(Generic[Document]):
    """
    Generic class for interacting with dynamodb and converting to/from types defined in the openapi spec
    """

    def __init__(self, table, model):
        """
        :param table: boto3 dynamodb table resource
        :param model: the generated model class
        """
        self.table = table
        self.model = model

    def _get(self, key: Dict) -> Optional[Dict]:
        return self.table.get_item(Key=key, ConsistentRead=True).get("Item")

    def _deserialize(self, document_dict: Dict):
        return self.model(
            **_sanitise_ddb_document_response(document_dict),
            # _spec_property_naming=True,
            _configuration=Configuration()
        )

    def _serialize(self, document: Document) -> Dict:
        return _sanitise_dict_for_ddb(JSONEncoder().default(document))

    def get(self, key: Dict) -> Optional[Document]:
        item = self._get(key)
        if item is None:
            return None
        return self._deserialize(item)

    def _add_metadata(
        self,
        key: Dict,
        user: str,
        document_dict: Dict,
        existing_document_dict: Optional[Dict],
    ) -> Dict:
        now = utc_now()
        metadata = {
            "createdBy": user
            if existing_document_dict is None
            else existing_document_dict["createdBy"],
            "updatedBy": user,
            "createdTimestamp": now
            if existing_document_dict is None
            else existing_document_dict["createdTimestamp"],
            "updatedTimestamp": now,
        }
        return {
            **document_dict,
            **metadata,
            **key,
        }

    def _put(self, key: Dict, user: str, document: Dict) -> Dict:
        existing_document = self._get(key)
        document_to_write = self._add_metadata(key, user, document, existing_document)
        self.table.put_item(Item=document_to_write)
        return document_to_write

    def put(self, key: Dict, user: str, document: Document) -> Document:
        return self._deserialize(self._put(key, user, self._serialize(document)))

    def list(
        self,
        pagination_parameters: PaginationParameters,
        fetch_page=fetch_page_with_scan(),
    ) -> PaginatedItemsResponse[Document]:
        res = list_with_pagination_parameters(
            self.table, pagination_parameters, fetch_page
        )
        return PaginatedItemsResponse(
            items=[self._deserialize(item) for item in res.items],
            error=res.error,
            next_token=res.next_token,
        )

    def delete_if_exists(self, key: Dict):
        item = self.get(key)
        if item is not None:
            self.table.delete_item(Key=key)
        return item
