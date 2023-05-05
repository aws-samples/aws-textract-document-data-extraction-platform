# api_python_client.model.form_field_extraction_metadata.FormFieldExtractionMetadata

Metadata to assist with the extraction of this form field from a document

#### Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**formKey** | **str** | The literal text uses as the key for this field in a form, eg &#x27;Name of Entity&#x27;. Capitalisation should be the same as appears in the form. | [optional] 
**tablePosition** | **int** | The 1-indexed table number in which this field appears. | [optional] 
**rowPosition** | **int** | The 1-indexed row number within the table in which this field appears | [optional] 
**columnPosition** | **int** | The 1-indexed column number within the table in which this field appears. | [optional] 
**textractQuery** | **str** | When specified, try to extract the field using this textract query before falling back to other means | [optional] 
**any string name** | dict, frozendict, str, date, datetime, int, float, bool, Decimal, None, list, tuple, bytes | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

