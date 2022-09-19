# FormJSONSchema

Schema for a json schema for a form, an extended definition of a standard JSON schema. See  See https://github.com/OAI/OpenAPI-Specification/blob/main/schemas/v3.0/schema.yaml

#### Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order** | **int** | The relative order of this property (for use in object types) | [optional] 
**extractionMetadata** | [**FormFieldExtractionMetadata**](FormFieldExtractionMetadata.md) |  | [optional] 
**title** | **str** |  | [optional] 
**multipleOf** | **int, float** |  | [optional] 
**maximum** | **int, float** |  | [optional] 
**exclusiveMaximum** | **bool** |  | [optional]  if omitted the server will use the default value of False
**minimum** | **int, float** |  | [optional] 
**exclusiveMinimum** | **bool** |  | [optional]  if omitted the server will use the default value of False
**maxLength** | **int** |  | [optional] 
**minLength** | **int** |  | [optional]  if omitted the server will use the default value of 0
**pattern** | **str** |  | [optional] 
**maxItems** | **int** |  | [optional] 
**minItems** | **int** |  | [optional]  if omitted the server will use the default value of 0
**uniqueItems** | **bool** |  | [optional]  if omitted the server will use the default value of False
**maxProperties** | **int** |  | [optional] 
**minProperties** | **int** |  | [optional]  if omitted the server will use the default value of 0
**required** | **[str]** |  | [optional] 
**enum** | **[bool, date, datetime, dict, float, int, list, str, none_type]** |  | [optional] 
**typeOf** | **str** |  | [optional] 
**notOf** | [**FormJSONSchema**](FormJSONSchema.md) |  | [optional] 
**allOf** | **[FormJSONSchema]** |  | [optional] 
**oneOf** | **[FormJSONSchema]** |  | [optional] 
**anyOf** | **[FormJSONSchema]** |  | [optional] 
**items** | [**FormJSONSchema**](FormJSONSchema.md) |  | [optional] 
**properties** | [**FormJSONSchemaProperties**](FormJSONSchemaProperties.md) |  | [optional] 
**additionalProperties** | **bool** |  | [optional]  if omitted the server will use the default value of True
**description** | **str** |  | [optional] 
**formatType** | **str** |  | [optional] 
**default** | **bool, date, datetime, dict, float, int, list, str, none_type** |  | [optional] 
**nullable** | **bool** |  | [optional]  if omitted the server will use the default value of False
**readOnly** | **bool** |  | [optional]  if omitted the server will use the default value of False
**writeOnly** | **bool** |  | [optional]  if omitted the server will use the default value of False
**example** | **bool, date, datetime, dict, float, int, list, str, none_type** |  | [optional] 
**deprecated** | **bool** |  | [optional]  if omitted the server will use the default value of False
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

