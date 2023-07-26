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


class FormJSONSchema(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Schema for a json schema for a form, an extended definition of a standard JSON schema. See  See https://github.com/OAI/OpenAPI-Specification/blob/main/schemas/v3.0/schema.yaml
    """


    class MetaOapg:
        class properties:
            order = schemas.IntSchema
        
            @classmethod
            @property
            def extractionMetadata(cls) -> typing.Type['FormFieldExtractionMetadata']:
                return FormFieldExtractionMetadata
            title = schemas.StrSchema
            
            
            class multipleOf(
                schemas.NumberSchema
            ):
                pass
            maximum = schemas.NumberSchema
            exclusiveMaximum = schemas.BoolSchema
            minimum = schemas.NumberSchema
            exclusiveMinimum = schemas.BoolSchema
            
            
            class maxLength(
                schemas.IntSchema
            ):
                pass
            
            
            class minLength(
                schemas.IntSchema
            ):
                pass
            pattern = schemas.StrSchema
            
            
            class maxItems(
                schemas.IntSchema
            ):
                pass
            
            
            class minItems(
                schemas.IntSchema
            ):
                pass
            uniqueItems = schemas.BoolSchema
            
            
            class maxProperties(
                schemas.IntSchema
            ):
                pass
            
            
            class minProperties(
                schemas.IntSchema
            ):
                pass
            
            
            class required(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    items = schemas.StrSchema
            
                def __new__(
                    cls,
                    arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, ]], typing.List[typing.Union[MetaOapg.items, str, ]]],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'required':
                    return super().__new__(
                        cls,
                        arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> MetaOapg.items:
                    return super().__getitem__(i)
            
            
            class enum(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    items = schemas.AnyTypeSchema
            
                def __new__(
                    cls,
                    arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes, ]], typing.List[typing.Union[MetaOapg.items, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes, ]]],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'enum':
                    return super().__new__(
                        cls,
                        arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> MetaOapg.items:
                    return super().__getitem__(i)
            
            
            class typeOf(
                schemas.SchemaEnumMakerClsFactory(
                    enum_value_to_name={
                        "array": "ARRAY",
                        "boolean": "BOOLEAN",
                        "integer": "INTEGER",
                        "number": "NUMBER",
                        "object": "OBJECT",
                        "string": "STRING",
                    }
                ),
                schemas.StrSchema
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
            
            
            class allOf(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
            
                    @classmethod
                    @property
                    def items(cls) -> typing.Type['FormJSONSchema']:
                        return FormJSONSchema
            
                def __new__(
                    cls,
                    arg: typing.Union[typing.Tuple['FormJSONSchema'], typing.List['FormJSONSchema']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'allOf':
                    return super().__new__(
                        cls,
                        arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'FormJSONSchema':
                    return super().__getitem__(i)
            
            
            class oneOf(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
            
                    @classmethod
                    @property
                    def items(cls) -> typing.Type['FormJSONSchema']:
                        return FormJSONSchema
            
                def __new__(
                    cls,
                    arg: typing.Union[typing.Tuple['FormJSONSchema'], typing.List['FormJSONSchema']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'oneOf':
                    return super().__new__(
                        cls,
                        arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'FormJSONSchema':
                    return super().__getitem__(i)
            
            
            class anyOf(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
            
                    @classmethod
                    @property
                    def items(cls) -> typing.Type['FormJSONSchema']:
                        return FormJSONSchema
            
                def __new__(
                    cls,
                    arg: typing.Union[typing.Tuple['FormJSONSchema'], typing.List['FormJSONSchema']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'anyOf':
                    return super().__new__(
                        cls,
                        arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'FormJSONSchema':
                    return super().__getitem__(i)
        
            @classmethod
            @property
            def items(cls) -> typing.Type['FormJSONSchema']:
                return FormJSONSchema
            
            
            class properties(
                schemas.DictSchema
            ):
            
            
                class MetaOapg:
                    
                    @classmethod
                    @property
                    def additional_properties(cls) -> typing.Type['FormJSONSchema']:
                        return FormJSONSchema
                
                def __getitem__(self, name: typing.Union[str, ]) -> 'FormJSONSchema':
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                def get_item_oapg(self, name: typing.Union[str, ]) -> 'FormJSONSchema':
                    return super().get_item_oapg(name)
            
                def __new__(
                    cls,
                    *args: typing.Union[dict, frozendict.frozendict, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: 'FormJSONSchema',
                ) -> 'properties':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            additionalProperties = schemas.BoolSchema
            description = schemas.StrSchema
            formatType = schemas.StrSchema
            default = schemas.AnyTypeSchema
            nullable = schemas.BoolSchema
            readOnly = schemas.BoolSchema
            writeOnly = schemas.BoolSchema
            example = schemas.AnyTypeSchema
            deprecated = schemas.BoolSchema
            __annotations__ = {
                "order": order,
                "extractionMetadata": extractionMetadata,
                "title": title,
                "multipleOf": multipleOf,
                "maximum": maximum,
                "exclusiveMaximum": exclusiveMaximum,
                "minimum": minimum,
                "exclusiveMinimum": exclusiveMinimum,
                "maxLength": maxLength,
                "minLength": minLength,
                "pattern": pattern,
                "maxItems": maxItems,
                "minItems": minItems,
                "uniqueItems": uniqueItems,
                "maxProperties": maxProperties,
                "minProperties": minProperties,
                "required": required,
                "enum": enum,
                "typeOf": typeOf,
                "allOf": allOf,
                "oneOf": oneOf,
                "anyOf": anyOf,
                "items": items,
                "properties": properties,
                "additionalProperties": additionalProperties,
                "description": description,
                "formatType": formatType,
                "default": default,
                "nullable": nullable,
                "readOnly": readOnly,
                "writeOnly": writeOnly,
                "example": example,
                "deprecated": deprecated,
            }
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["order"]) -> MetaOapg.properties.order: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["extractionMetadata"]) -> 'FormFieldExtractionMetadata': ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["title"]) -> MetaOapg.properties.title: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["multipleOf"]) -> MetaOapg.properties.multipleOf: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["maximum"]) -> MetaOapg.properties.maximum: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["exclusiveMaximum"]) -> MetaOapg.properties.exclusiveMaximum: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["minimum"]) -> MetaOapg.properties.minimum: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["exclusiveMinimum"]) -> MetaOapg.properties.exclusiveMinimum: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["maxLength"]) -> MetaOapg.properties.maxLength: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["minLength"]) -> MetaOapg.properties.minLength: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["pattern"]) -> MetaOapg.properties.pattern: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["maxItems"]) -> MetaOapg.properties.maxItems: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["minItems"]) -> MetaOapg.properties.minItems: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["uniqueItems"]) -> MetaOapg.properties.uniqueItems: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["maxProperties"]) -> MetaOapg.properties.maxProperties: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["minProperties"]) -> MetaOapg.properties.minProperties: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["required"]) -> MetaOapg.properties.required: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["enum"]) -> MetaOapg.properties.enum: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["typeOf"]) -> MetaOapg.properties.typeOf: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["allOf"]) -> MetaOapg.properties.allOf: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["oneOf"]) -> MetaOapg.properties.oneOf: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["anyOf"]) -> MetaOapg.properties.anyOf: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["items"]) -> 'FormJSONSchema': ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["properties"]) -> MetaOapg.properties.properties: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["additionalProperties"]) -> MetaOapg.properties.additionalProperties: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["description"]) -> MetaOapg.properties.description: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["formatType"]) -> MetaOapg.properties.formatType: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["default"]) -> MetaOapg.properties.default: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["nullable"]) -> MetaOapg.properties.nullable: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["readOnly"]) -> MetaOapg.properties.readOnly: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["writeOnly"]) -> MetaOapg.properties.writeOnly: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["example"]) -> MetaOapg.properties.example: ...
    
    @typing.overload
    def __getitem__(self, name: typing.Literal["deprecated"]) -> MetaOapg.properties.deprecated: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing.Literal["order", "extractionMetadata", "title", "multipleOf", "maximum", "exclusiveMaximum", "minimum", "exclusiveMinimum", "maxLength", "minLength", "pattern", "maxItems", "minItems", "uniqueItems", "maxProperties", "minProperties", "required", "enum", "typeOf", "allOf", "oneOf", "anyOf", "items", "properties", "additionalProperties", "description", "formatType", "default", "nullable", "readOnly", "writeOnly", "example", "deprecated", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["order"]) -> typing.Union[MetaOapg.properties.order, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["extractionMetadata"]) -> typing.Union['FormFieldExtractionMetadata', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["title"]) -> typing.Union[MetaOapg.properties.title, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["multipleOf"]) -> typing.Union[MetaOapg.properties.multipleOf, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["maximum"]) -> typing.Union[MetaOapg.properties.maximum, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["exclusiveMaximum"]) -> typing.Union[MetaOapg.properties.exclusiveMaximum, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["minimum"]) -> typing.Union[MetaOapg.properties.minimum, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["exclusiveMinimum"]) -> typing.Union[MetaOapg.properties.exclusiveMinimum, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["maxLength"]) -> typing.Union[MetaOapg.properties.maxLength, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["minLength"]) -> typing.Union[MetaOapg.properties.minLength, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["pattern"]) -> typing.Union[MetaOapg.properties.pattern, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["maxItems"]) -> typing.Union[MetaOapg.properties.maxItems, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["minItems"]) -> typing.Union[MetaOapg.properties.minItems, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["uniqueItems"]) -> typing.Union[MetaOapg.properties.uniqueItems, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["maxProperties"]) -> typing.Union[MetaOapg.properties.maxProperties, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["minProperties"]) -> typing.Union[MetaOapg.properties.minProperties, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["required"]) -> typing.Union[MetaOapg.properties.required, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["enum"]) -> typing.Union[MetaOapg.properties.enum, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["typeOf"]) -> typing.Union[MetaOapg.properties.typeOf, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["allOf"]) -> typing.Union[MetaOapg.properties.allOf, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["oneOf"]) -> typing.Union[MetaOapg.properties.oneOf, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["anyOf"]) -> typing.Union[MetaOapg.properties.anyOf, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["items"]) -> typing.Union['FormJSONSchema', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["properties"]) -> typing.Union[MetaOapg.properties.properties, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["additionalProperties"]) -> typing.Union[MetaOapg.properties.additionalProperties, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["description"]) -> typing.Union[MetaOapg.properties.description, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["formatType"]) -> typing.Union[MetaOapg.properties.formatType, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["default"]) -> typing.Union[MetaOapg.properties.default, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["nullable"]) -> typing.Union[MetaOapg.properties.nullable, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["readOnly"]) -> typing.Union[MetaOapg.properties.readOnly, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["writeOnly"]) -> typing.Union[MetaOapg.properties.writeOnly, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["example"]) -> typing.Union[MetaOapg.properties.example, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing.Literal["deprecated"]) -> typing.Union[MetaOapg.properties.deprecated, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing.Literal["order", "extractionMetadata", "title", "multipleOf", "maximum", "exclusiveMaximum", "minimum", "exclusiveMinimum", "maxLength", "minLength", "pattern", "maxItems", "minItems", "uniqueItems", "maxProperties", "minProperties", "required", "enum", "typeOf", "allOf", "oneOf", "anyOf", "items", "properties", "additionalProperties", "description", "formatType", "default", "nullable", "readOnly", "writeOnly", "example", "deprecated", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        order: typing.Union[MetaOapg.properties.order, int, schemas.Unset] = schemas.unset,
        extractionMetadata: typing.Union['FormFieldExtractionMetadata', schemas.Unset] = schemas.unset,
        title: typing.Union[MetaOapg.properties.title, str, schemas.Unset] = schemas.unset,
        multipleOf: typing.Union[MetaOapg.properties.multipleOf, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        maximum: typing.Union[MetaOapg.properties.maximum, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        exclusiveMaximum: typing.Union[MetaOapg.properties.exclusiveMaximum, bool, schemas.Unset] = schemas.unset,
        minimum: typing.Union[MetaOapg.properties.minimum, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        exclusiveMinimum: typing.Union[MetaOapg.properties.exclusiveMinimum, bool, schemas.Unset] = schemas.unset,
        maxLength: typing.Union[MetaOapg.properties.maxLength, int, schemas.Unset] = schemas.unset,
        minLength: typing.Union[MetaOapg.properties.minLength, int, schemas.Unset] = schemas.unset,
        pattern: typing.Union[MetaOapg.properties.pattern, str, schemas.Unset] = schemas.unset,
        maxItems: typing.Union[MetaOapg.properties.maxItems, int, schemas.Unset] = schemas.unset,
        minItems: typing.Union[MetaOapg.properties.minItems, int, schemas.Unset] = schemas.unset,
        uniqueItems: typing.Union[MetaOapg.properties.uniqueItems, bool, schemas.Unset] = schemas.unset,
        maxProperties: typing.Union[MetaOapg.properties.maxProperties, int, schemas.Unset] = schemas.unset,
        minProperties: typing.Union[MetaOapg.properties.minProperties, int, schemas.Unset] = schemas.unset,
        required: typing.Union[MetaOapg.properties.required, tuple, schemas.Unset] = schemas.unset,
        enum: typing.Union[MetaOapg.properties.enum, tuple, schemas.Unset] = schemas.unset,
        typeOf: typing.Union[MetaOapg.properties.typeOf, str, schemas.Unset] = schemas.unset,
        allOf: typing.Union[MetaOapg.properties.allOf, tuple, schemas.Unset] = schemas.unset,
        oneOf: typing.Union[MetaOapg.properties.oneOf, tuple, schemas.Unset] = schemas.unset,
        anyOf: typing.Union[MetaOapg.properties.anyOf, tuple, schemas.Unset] = schemas.unset,
        items: typing.Union['FormJSONSchema', schemas.Unset] = schemas.unset,
        properties: typing.Union[MetaOapg.properties.properties, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        additionalProperties: typing.Union[MetaOapg.properties.additionalProperties, bool, schemas.Unset] = schemas.unset,
        description: typing.Union[MetaOapg.properties.description, str, schemas.Unset] = schemas.unset,
        formatType: typing.Union[MetaOapg.properties.formatType, str, schemas.Unset] = schemas.unset,
        default: typing.Union[MetaOapg.properties.default, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes, schemas.Unset] = schemas.unset,
        nullable: typing.Union[MetaOapg.properties.nullable, bool, schemas.Unset] = schemas.unset,
        readOnly: typing.Union[MetaOapg.properties.readOnly, bool, schemas.Unset] = schemas.unset,
        writeOnly: typing.Union[MetaOapg.properties.writeOnly, bool, schemas.Unset] = schemas.unset,
        example: typing.Union[MetaOapg.properties.example, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes, schemas.Unset] = schemas.unset,
        deprecated: typing.Union[MetaOapg.properties.deprecated, bool, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'FormJSONSchema':
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