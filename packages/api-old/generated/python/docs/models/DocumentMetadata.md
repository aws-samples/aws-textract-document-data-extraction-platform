# api_python_client.model.document_metadata.DocumentMetadata

Metadata about a document

#### Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**statusTransitionLog** | **[StatusTransition]** | A log of status transitions | 
**name** | **str** | The name of the document | 
**documentId** | **str** |  | 
**location** | [**S3Location**](S3Location.md) |  | 
**ingestionExecution** | [**IngestionExecution**](IngestionExecution.md) |  | [optional] 
**numberOfPages** | **int** | The number of pages in the document, discovered during classification | [optional] 
**numberOfClassifiedForms** | **int** | The number of forms discovered within the document | [optional] 
**url** | **str** | Presigned url for fetching the document (returned on get individual document only) | [optional] 
**any string name** | dict, frozendict, str, date, datetime, int, float, bool, Decimal, None, list, tuple, bytes | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

