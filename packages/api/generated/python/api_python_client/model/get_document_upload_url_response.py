# coding: utf-8

"""
    AWS Docs API

    API for AWS Docs  # noqa: E501

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


class GetDocumentUploadUrlResponse(
    DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Response to getting a document upload url
    """
    _required_property_names = set((
        'documentId',
        'url',
        'location',
    ))
    documentId = StrSchema
    url = StrSchema

    @classmethod
    @property
    def location(cls) -> typing.Type['S3Location']:
        return S3Location


    def __new__(
        cls,
        *args: typing.Union[dict, frozendict, ],
        documentId: documentId,
        url: url,
        location: location,
        _configuration: typing.Optional[Configuration] = None,
        **kwargs: typing.Type[Schema],
    ) -> 'GetDocumentUploadUrlResponse':
        return super().__new__(
            cls,
            *args,
            documentId=documentId,
            url=url,
            location=location,
            _configuration=_configuration,
            **kwargs,
        )

from api_python_client.model.s3_location import S3Location
