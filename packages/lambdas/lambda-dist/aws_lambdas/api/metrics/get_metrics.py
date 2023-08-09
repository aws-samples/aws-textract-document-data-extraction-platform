#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from typing import List

from aws_api_python_runtime.apis.tags.default_api_operation_config import (
    get_metrics_handler,
    GetMetricsRequest,
)
from aws_api_python_runtime.model.aggregate_metrics import AggregateMetrics
from aws_api_python_runtime.model.form_schema import FormSchema

from aws_lambdas.api.utils.api import api, identity_interceptor
from aws_lambdas.api.utils.response import Response, ApiResponse
from aws_lambdas.utils.ddb.form_schema_store import FormSchemaStore
from aws_lambdas.utils.ddb.store import PaginationParameters
from aws_lambdas.utils.metrics.metrics import Metrics


def _list_all_schemas() -> List[FormSchema]:
    """
    List all schemas in the store
    """
    store = FormSchemaStore()

    schemas: List[FormSchema] = []
    has_more_results = True
    next_token = None

    while has_more_results:
        response = store.list_all(
            PaginationParameters(page_size=100, next_token=next_token)
        )
        schemas += response.items
        next_token = response.next_token
        has_more_results = next_token is not None

    return schemas


@get_metrics_handler(interceptors=[identity_interceptor])
def handler(input: GetMetricsRequest, **kwargs) -> ApiResponse[AggregateMetrics]:
    """
    Handler for retrieving aggregate metrics
    """
    start_timestamp = input.request_parameters["startTimestamp"]
    end_timestamp = input.request_parameters["endTimestamp"]

    schema_ids = [schema.schemaId for schema in _list_all_schemas()]

    return Response.success(
        Metrics().get_aggregate_metrics(start_timestamp, end_timestamp, schema_ids)
    )
