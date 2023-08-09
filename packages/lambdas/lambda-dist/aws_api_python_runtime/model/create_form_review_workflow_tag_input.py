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


class CreateFormReviewWorkflowTagInput(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Describes the input for creating a new form review workflow tag
    """


    class MetaOapg:
        required = {
            "tagText",
        }
        
        class properties:
            tagText = schemas.StrSchema
            __annotations__ = {
                "tagText": tagText,
            }
    
    tagText: MetaOapg.properties.tagText
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["tagText"]) -> MetaOapg.properties.tagText: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["tagText", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["tagText"]) -> MetaOapg.properties.tagText: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["tagText", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        tagText: typing.Union[MetaOapg.properties.tagText, str, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'CreateFormReviewWorkflowTagInput':
        return super().__new__(
            cls,
            *_args,
            tagText=tagText,
            _configuration=_configuration,
            **kwargs,
        )
