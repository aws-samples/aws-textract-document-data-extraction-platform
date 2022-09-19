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
import uuid  # noqa: F401

import frozendict  # noqa: F401

from api_python_client import schemas  # noqa: F401


class CreateUpdateDetails(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Metadata about when an item was created/updated
    """


    class MetaOapg:
        class properties:
            createdBy = schemas.StrSchema
            updatedBy = schemas.StrSchema
            createdTimestamp = schemas.StrSchema
            updatedTimestamp = schemas.StrSchema
            __annotations__ = {
                "createdBy": createdBy,
                "updatedBy": updatedBy,
                "createdTimestamp": createdTimestamp,
                "updatedTimestamp": updatedTimestamp,
            }
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["createdBy"]) -> MetaOapg.properties.createdBy: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["updatedBy"]) -> MetaOapg.properties.updatedBy: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["createdTimestamp"]) -> MetaOapg.properties.createdTimestamp: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["updatedTimestamp"]) -> MetaOapg.properties.updatedTimestamp: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing.Literal["createdBy", "updatedBy", "createdTimestamp", "updatedTimestamp", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["createdBy"]) -> typing.Union[MetaOapg.properties.createdBy, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["updatedBy"]) -> typing.Union[MetaOapg.properties.updatedBy, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["createdTimestamp"]) -> typing.Union[MetaOapg.properties.createdTimestamp, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["updatedTimestamp"]) -> typing.Union[MetaOapg.properties.updatedTimestamp, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing.Literal["createdBy", "updatedBy", "createdTimestamp", "updatedTimestamp", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        createdBy: typing.Union[MetaOapg.properties.createdBy, str, schemas.Unset] = schemas.unset,
        updatedBy: typing.Union[MetaOapg.properties.updatedBy, str, schemas.Unset] = schemas.unset,
        createdTimestamp: typing.Union[MetaOapg.properties.createdTimestamp, str, schemas.Unset] = schemas.unset,
        updatedTimestamp: typing.Union[MetaOapg.properties.updatedTimestamp, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'CreateUpdateDetails':
        return super().__new__(
            cls,
            *args,
            createdBy=createdBy,
            updatedBy=updatedBy,
            createdTimestamp=createdTimestamp,
            updatedTimestamp=updatedTimestamp,
            _configuration=_configuration,
            **kwargs,
        )
