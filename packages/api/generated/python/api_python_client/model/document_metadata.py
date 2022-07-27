# coding: utf-8

"""
    ASX Docs API

    API for ASX Docs  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""

import re  # noqa: F401
import sys  # noqa: F401
import typing  # noqa: F401
import functools  # noqa: F401

from frozendict import frozendict  # noqa: F401

import decimal  # noqa: F401
from datetime import date, datetime  # noqa: F401
from frozendict import frozendict  # noqa: F401

from api_python_client.schemas import (  # noqa: F401
    AnyTypeSchema,
    ComposedSchema,
    DictSchema,
    ListSchema,
    StrSchema,
    IntSchema,
    Int32Schema,
    Int64Schema,
    Float32Schema,
    Float64Schema,
    NumberSchema,
    UUIDSchema,
    DateSchema,
    DateTimeSchema,
    DecimalSchema,
    BoolSchema,
    BinarySchema,
    NoneSchema,
    none_type,
    Configuration,
    Unset,
    unset,
    ComposedBase,
    ListBase,
    DictBase,
    NoneBase,
    StrBase,
    IntBase,
    Int32Base,
    Int64Base,
    Float32Base,
    Float64Base,
    NumberBase,
    UUIDBase,
    DateBase,
    DateTimeBase,
    BoolBase,
    BinaryBase,
    Schema,
    _SchemaValidator,
    _SchemaTypeChecker,
    _SchemaEnumMaker
)


class DocumentMetadata(
    ComposedBase,
    DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Metadata about a document
    """
    _required_property_names = set((
        'documentId',
        'name',
        'location',
        'statusTransitionLog',
    ))
    documentId = StrSchema
    name = StrSchema

    @classmethod
    @property
    def location(cls) -> typing.Type['S3Location']:
        return S3Location

    @classmethod
    @property
    def ingestionExecution(cls) -> typing.Type['IngestionExecution']:
        return IngestionExecution
    numberOfPages = IntSchema
    numberOfClassifiedForms = IntSchema
    url = StrSchema
    
    
    class statusTransitionLog(
        ListSchema
    ):
    
        @classmethod
        @property
        def _items(cls) -> typing.Type['StatusTransition']:
            return StatusTransition

    @classmethod
    @property
    @functools.cache
    def _composed_schemas(cls):
        # we need this here to make our import statements work
        # we must store _composed_schemas in here so the code is only run
        # when we invoke this method. If we kept this at the class
        # level we would get an error because the class level
        # code would be run when this module is imported, and these composed
        # classes don't exist yet because their module has not finished
        # loading
        return {
            'allOf': [
                CreateUpdateDetails,
            ],
            'oneOf': [
            ],
            'anyOf': [
            ],
            'not':
                None
        }

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict, ],
        documentId: documentId,
        name: name,
        location: location,
        statusTransitionLog: statusTransitionLog,
        ingestionExecution: typing.Union['IngestionExecution', Unset] = unset,
        numberOfPages: typing.Union[numberOfPages, Unset] = unset,
        numberOfClassifiedForms: typing.Union[numberOfClassifiedForms, Unset] = unset,
        url: typing.Union[url, Unset] = unset,
        _configuration: typing.Optional[Configuration] = None,
        **kwargs: typing.Type[Schema],
    ) -> 'DocumentMetadata':
        return super().__new__(
            cls,
            *args,
            documentId=documentId,
            name=name,
            location=location,
            statusTransitionLog=statusTransitionLog,
            ingestionExecution=ingestionExecution,
            numberOfPages=numberOfPages,
            numberOfClassifiedForms=numberOfClassifiedForms,
            url=url,
            _configuration=_configuration,
            **kwargs,
        )

from api_python_client.model.create_update_details import CreateUpdateDetails
from api_python_client.model.ingestion_execution import IngestionExecution
from api_python_client.model.s3_location import S3Location
from api_python_client.model.status_transition import StatusTransition
