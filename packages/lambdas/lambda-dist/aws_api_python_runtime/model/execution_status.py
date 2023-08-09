# coding: utf-8

"""
    AWS Docs API

    API for AWS Docs  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from aws_api_python_runtime import schemas  # noqa: F401


class ExecutionStatus(
    schemas.EnumBase,
    schemas.StrSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        enum_value_to_name = {
            "IN_PROGRESS": "IN_PROGRESS",
            "SUCCEEDED": "SUCCEEDED",
            "FAILED": "FAILED",
        }
    
    @schemas.classproperty
    def IN_PROGRESS(cls):
        return cls("IN_PROGRESS")
    
    @schemas.classproperty
    def SUCCEEDED(cls):
        return cls("SUCCEEDED")
    
    @schemas.classproperty
    def FAILED(cls):
        return cls("FAILED")
