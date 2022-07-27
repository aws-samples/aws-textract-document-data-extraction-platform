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


class ExtractionExecutionStatus(
    _SchemaEnumMaker(
        enum_value_to_name={
            "NOT_STARTED": "NOT_STARTED",
            "IN_PROGRESS": "IN_PROGRESS",
            "READY_FOR_REVIEW": "READY_FOR_REVIEW",
            "REVIEWING": "REVIEWING",
            "REVIEWED": "REVIEWED",
            "FAILED": "FAILED",
        }
    ),
    StrSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    
    @classmethod
    @property
    def NOT_STARTED(cls):
        return cls("NOT_STARTED")
    
    @classmethod
    @property
    def IN_PROGRESS(cls):
        return cls("IN_PROGRESS")
    
    @classmethod
    @property
    def READY_FOR_REVIEW(cls):
        return cls("READY_FOR_REVIEW")
    
    @classmethod
    @property
    def REVIEWING(cls):
        return cls("REVIEWING")
    
    @classmethod
    @property
    def REVIEWED(cls):
        return cls("REVIEWED")
    
    @classmethod
    @property
    def FAILED(cls):
        return cls("FAILED")
