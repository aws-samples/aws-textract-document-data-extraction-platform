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


class ListDocumentsResponse(
    schemas.ComposedBase,
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    A list of documents
    """


    class MetaOapg:
        required = {
            "documents",
        }
        class properties:
            
            
            class documents(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
            
                    @classmethod
                    @property
                    def items(cls) -> typing.Type['DocumentMetadata']:
                        return DocumentMetadata
            
                def __new__(
                    cls,
                    arg: typing.Union[typing.Tuple['DocumentMetadata'], typing.List['DocumentMetadata']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'documents':
                    return super().__new__(
                        cls,
                        arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'DocumentMetadata':
                    return super().__getitem__(i)
            __annotations__ = {
                "documents": documents,
            }
        
        @classmethod
        @property
        @functools.cache
        def all_of(cls):
            # we need this here to make our import statements work
            # we must store _composed_schemas in here so the code is only run
            # when we invoke this method. If we kept this at the class
            # level we would get an error because the class level
            # code would be run when this module is imported, and these composed
            # classes don't exist yet because their module has not finished
            # loading
            return [
                PaginatedResponse,
            ]

    
    documents: MetaOapg.properties.documents
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["documents"]) -> MetaOapg.properties.documents: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing.Literal["documents", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["documents"]) -> MetaOapg.properties.documents: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing.Literal["documents", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        documents: typing.Union[MetaOapg.properties.documents, tuple, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'ListDocumentsResponse':
        return super().__new__(
            cls,
            *args,
            documents=documents,
            _configuration=_configuration,
            **kwargs,
        )

from api_python_client.model.document_metadata import DocumentMetadata
from api_python_client.model.paginated_response import PaginatedResponse