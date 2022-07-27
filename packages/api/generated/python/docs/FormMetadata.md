# FormMetadata

Metadata about a form within a document

#### Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**documentId** | **str** |  | 
**documentName** | **str** |  | 
**formId** | **str** |  | 
**schemaId** | **str** |  | 
**numberOfPages** | **int** | The number of pages in the form | 
**startPageIndex** | **int** |  | 
**endPageIndex** | **int** |  | 
**location** | [**S3Location**](S3Location.md) |  | 
**extractionExecution** | [**ExtractionExecution**](ExtractionExecution.md) |  | 
**extractedData** | **bool, date, datetime, dict, float, int, list, str, none_type** | Data extracted from the form - has any type, will be of the shape of the schema. This can be modified by reviewers who may correct data that has been inaccurately extracted | [optional] 
**originalExtractedData** | **bool, date, datetime, dict, float, int, list, str, none_type** | The original data extracted from the form - has any type, will be of the shape of the schema. This is what was originally extracted by the system, prior to any human review. | [optional] 
**extractedDataMetadata** | **bool, date, datetime, dict, float, int, list, str, none_type** | Metadata of extracted data values, of same shape as the data above, but leaf values contain confidence and bounding box metadata. | [optional] 
**extractionAccuracy** | [**ExtractionAccuracy**](ExtractionAccuracy.md) |  | [optional] 
**averageConfidence** | **int, float** | The average confidence computed by textract for all fields in the form | [optional] 
**schemaSnapshot** | [**FormJSONSchema**](FormJSONSchema.md) |  | 
**url** | **str** | Presigned url for fetching the document (returned on get individual form only) | [optional] 
**textractOutputLocation** | [**S3Location**](S3Location.md) |  | [optional] 
**statusTransitionLog** | **[StatusTransition]** | A log of status transitions | 
**tags** | **[str]** |  | [optional] 
**notes** | **str** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

