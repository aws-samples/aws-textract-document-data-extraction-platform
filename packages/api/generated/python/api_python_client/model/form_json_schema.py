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


class FormJSONSchema(
    DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Schema for a json schema for a form, an extended definition of a standard JSON schema. See  See https://github.com/OAI/OpenAPI-Specification/blob/main/schemas/v3.0/schema.yaml
    """
    order = IntSchema

    @classmethod
    @property
    def extractionMetadata(cls) -> typing.Type['FormFieldExtractionMetadata']:
        return FormFieldExtractionMetadata
    title = StrSchema
    
    
    class multipleOf(
        _SchemaValidator(
            exclusive_minimuminclusive_minimum=0,
        ),
        NumberSchema
    ):
        pass
    maximum = NumberSchema
    exclusiveMaximum = BoolSchema
    minimum = NumberSchema
    exclusiveMinimum = BoolSchema
    
    
    class maxLength(
        _SchemaValidator(
            inclusive_minimum=0,
        ),
        IntSchema
    ):
        pass
    
    
    class minLength(
        _SchemaValidator(
            inclusive_minimum=0,
        ),
        IntSchema
    ):
        pass
    pattern = StrSchema
    
    
    class maxItems(
        _SchemaValidator(
            inclusive_minimum=0,
        ),
        IntSchema
    ):
        pass
    
    
    class minItems(
        _SchemaValidator(
            inclusive_minimum=0,
        ),
        IntSchema
    ):
        pass
    uniqueItems = BoolSchema
    
    
    class maxProperties(
        _SchemaValidator(
            inclusive_minimum=0,
        ),
        IntSchema
    ):
        pass
    
    
    class minProperties(
        _SchemaValidator(
            inclusive_minimum=0,
        ),
        IntSchema
    ):
        pass
    
    
    class required(
        _SchemaValidator(
            min_items=1,
        ),
        ListSchema
    ):
        _items = StrSchema
    
    
    class enum(
        _SchemaValidator(
            min_items=1,
        ),
        ListSchema
    ):
        _items = AnyTypeSchema
    
    
    class typeOf(
        _SchemaEnumMaker(
            enum_value_to_name={
                "array": "ARRAY",
                "boolean": "BOOLEAN",
                "integer": "INTEGER",
                "number": "NUMBER",
                "object": "OBJECT",
                "string": "STRING",
            }
        ),
        StrSchema
    ):
        
        @classmethod
        @property
        def ARRAY(cls):
            return cls("array")
        
        @classmethod
        @property
        def BOOLEAN(cls):
            return cls("boolean")
        
        @classmethod
        @property
        def INTEGER(cls):
            return cls("integer")
        
        @classmethod
        @property
        def NUMBER(cls):
            return cls("number")
        
        @classmethod
        @property
        def OBJECT(cls):
            return cls("object")
        
        @classmethod
        @property
        def STRING(cls):
            return cls("string")

    @classmethod
    @property
    def _not(cls) -> typing.Type['FormJSONSchema']:
        return FormJSONSchema
    
    
    class allOf(
        ListSchema
    ):
    
        @classmethod
        @property
        def _items(cls) -> typing.Type['FormJSONSchema']:
            return FormJSONSchema
    
    
    class oneOf(
        ListSchema
    ):
    
        @classmethod
        @property
        def _items(cls) -> typing.Type['FormJSONSchema']:
            return FormJSONSchema
    
    
    class anyOf(
        ListSchema
    ):
    
        @classmethod
        @property
        def _items(cls) -> typing.Type['FormJSONSchema']:
            return FormJSONSchema

    @classmethod
    @property
    def items(cls) -> typing.Type['FormJSONSchema']:
        return FormJSONSchema
    
    
    class properties(
        DictSchema
    ):
    
        @classmethod
        @property
        def _additional_properties(cls) -> typing.Type['FormJSONSchema']:
            return FormJSONSchema
    
    
        def __new__(
            cls,
            *args: typing.Union[dict, frozendict, ],
            _configuration: typing.Optional[Configuration] = None,
            **kwargs: typing.Type[Schema],
        ) -> 'properties':
            return super().__new__(
                cls,
                *args,
                _configuration=_configuration,
                **kwargs,
            )
    additionalProperties = BoolSchema
    description = StrSchema
    formatType = StrSchema
    default = AnyTypeSchema
    nullable = BoolSchema
    readOnly = BoolSchema
    writeOnly = BoolSchema
    example = AnyTypeSchema
    deprecated = BoolSchema


    def __new__(
        cls,
        order: typing.Union[order, Unset] = unset,
        extractionMetadata: typing.Union['FormFieldExtractionMetadata', Unset] = unset,
        title: typing.Union[title, Unset] = unset,
        multipleOf: typing.Union[multipleOf, Unset] = unset,
        maximum: typing.Union[maximum, Unset] = unset,
        exclusiveMaximum: typing.Union[exclusiveMaximum, Unset] = unset,
        minimum: typing.Union[minimum, Unset] = unset,
        exclusiveMinimum: typing.Union[exclusiveMinimum, Unset] = unset,
        maxLength: typing.Union[maxLength, Unset] = unset,
        minLength: typing.Union[minLength, Unset] = unset,
        pattern: typing.Union[pattern, Unset] = unset,
        maxItems: typing.Union[maxItems, Unset] = unset,
        minItems: typing.Union[minItems, Unset] = unset,
        uniqueItems: typing.Union[uniqueItems, Unset] = unset,
        maxProperties: typing.Union[maxProperties, Unset] = unset,
        minProperties: typing.Union[minProperties, Unset] = unset,
        required: typing.Union[required, Unset] = unset,
        enum: typing.Union[enum, Unset] = unset,
        typeOf: typing.Union[typeOf, Unset] = unset,
        _not: typing.Union['FormJSONSchema', Unset] = unset,
        allOf: typing.Union[allOf, Unset] = unset,
        oneOf: typing.Union[oneOf, Unset] = unset,
        anyOf: typing.Union[anyOf, Unset] = unset,
        items: typing.Union['FormJSONSchema', Unset] = unset,
        properties: typing.Union[properties, Unset] = unset,
        additionalProperties: typing.Union[additionalProperties, Unset] = unset,
        description: typing.Union[description, Unset] = unset,
        formatType: typing.Union[formatType, Unset] = unset,
        default: typing.Union[default, Unset] = unset,
        nullable: typing.Union[nullable, Unset] = unset,
        readOnly: typing.Union[readOnly, Unset] = unset,
        writeOnly: typing.Union[writeOnly, Unset] = unset,
        example: typing.Union[example, Unset] = unset,
        deprecated: typing.Union[deprecated, Unset] = unset,
        _configuration: typing.Optional[Configuration] = None,
        *args: typing.Union[dict, frozendict, ],
        **kwargs: typing.Type[AnyTypeSchema],
    ) -> 'FormJSONSchema':
        print("~~~~ FormJSONSchema #2 ~~~~  title : {} args:{} kwargs: {}".format(title, args, kwargs))
        return super().__new__(
            cls,
            *args,
            order=order,
            extractionMetadata=extractionMetadata,
            title=title,
            multipleOf=multipleOf,
            maximum=maximum,
            exclusiveMaximum=exclusiveMaximum,
            minimum=minimum,
            exclusiveMinimum=exclusiveMinimum,
            maxLength=maxLength,
            minLength=minLength,
            pattern=pattern,
            maxItems=maxItems,
            minItems=minItems,
            uniqueItems=uniqueItems,
            maxProperties=maxProperties,
            minProperties=minProperties,
            required=required,
            enum=enum,
            typeOf=typeOf,
            _not=_not,
            allOf=allOf,
            oneOf=oneOf,
            anyOf=anyOf,
            items=items,
            properties=properties,
            additionalProperties=additionalProperties,
            description=description,
            formatType=formatType,
            default=default,
            nullable=nullable,
            readOnly=readOnly,
            writeOnly=writeOnly,
            example=example,
            deprecated=deprecated,
            _configuration=_configuration,
            **kwargs,
        )

from api_python_client.model.form_field_extraction_metadata import FormFieldExtractionMetadata
