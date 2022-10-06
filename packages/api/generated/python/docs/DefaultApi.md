# api_python_client.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_form_review_workflow_tag**](DefaultApi.md#create_form_review_workflow_tag) | **POST** /tags | 
[**create_form_schema**](DefaultApi.md#create_form_schema) | **POST** /schemas | 
[**delete_form_schema**](DefaultApi.md#delete_form_schema) | **DELETE** /schemas/{schemaId} | 
[**get_document**](DefaultApi.md#get_document) | **GET** /documents/{documentId} | 
[**get_document_form**](DefaultApi.md#get_document_form) | **GET** /documents/{documentId}/forms/{formId} | 
[**get_document_upload_url**](DefaultApi.md#get_document_upload_url) | **GET** /documents/upload-url | 
[**get_form_schema**](DefaultApi.md#get_form_schema) | **GET** /schemas/{schemaId} | 
[**get_metrics**](DefaultApi.md#get_metrics) | **GET** /metrics | 
[**list_document_forms**](DefaultApi.md#list_document_forms) | **GET** /documents/{documentId}/forms | 
[**list_documents**](DefaultApi.md#list_documents) | **GET** /documents | 
[**list_form_review_workflow_tags**](DefaultApi.md#list_form_review_workflow_tags) | **GET** /tags | 
[**list_form_schemas**](DefaultApi.md#list_form_schemas) | **GET** /schemas | 
[**list_forms**](DefaultApi.md#list_forms) | **GET** /forms | 
[**submit_source_document**](DefaultApi.md#submit_source_document) | **POST** /sources/document | 
[**update_form_review**](DefaultApi.md#update_form_review) | **PUT** /documents/{documentId}/forms/{formId}/review | 
[**update_form_schema**](DefaultApi.md#update_form_schema) | **PUT** /schemas/{schemaId} | 
[**update_status**](DefaultApi.md#update_status) | **PUT** /documents/{documentId}/forms/{formId}/status | 

# **create_form_review_workflow_tag**
> FormReviewWorkflowTag create_form_review_workflow_tag(create_form_review_workflow_tag_input)



create a form review workflow tag

### Example

```python
import api_python_client
from api_python_client.api import default_api
from api_python_client.model.form_review_workflow_tag import FormReviewWorkflowTag
from api_python_client.model.create_form_review_workflow_tag_input import CreateFormReviewWorkflowTagInput
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = api_python_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with api_python_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)

    # example passing only required values which don't have defaults set
    body = CreateFormReviewWorkflowTagInput(
        tag_text="tag_text_example",
    )
    try:
        api_response = api_instance.create_form_review_workflow_tag(
            body=body,
        )
        pprint(api_response)
    except api_python_client.ApiException as e:
        print("Exception when calling DefaultApi->create_form_review_workflow_tag: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

#### SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**CreateFormReviewWorkflowTagInput**](CreateFormReviewWorkflowTagInput.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | ApiResponseFor200 | Returned on successful addition of a form review workflow tag

#### ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**FormReviewWorkflowTag**](FormReviewWorkflowTag.md) |  | 



[**FormReviewWorkflowTag**](FormReviewWorkflowTag.md)

### Authorization

No authorization required

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_form_schema**
> FormSchema create_form_schema(form_schema_input)



Create a new form schema

### Example

```python
import api_python_client
from api_python_client.api import default_api
from api_python_client.model.form_schema import FormSchema
from api_python_client.model.form_schema_input import FormSchemaInput
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = api_python_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with api_python_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)

    # example passing only required values which don't have defaults set
    body = FormSchemaInput(
        title="title_example",
        description="description_example",
        schema=FormJSONSchema(
            order=1,
            extraction_metadata=FormFieldExtractionMetadata(
                formKey="form_key_example",
                tablePosition=1,
                rowPosition=1,
                columnPosition=1,
                textractQuery="textract_query_example",
            ),
            title="title_example",
            multiple_of=0,
            maximum=3.14,
            exclusive_maximum=False,
            minimum=3.14,
            exclusive_minimum=False,
            max_length=0,
            min_length=0,
            pattern="pattern_example",
            max_items=0,
            min_items=0,
            unique_items=False,
            max_properties=0,
            min_properties=0,
            required=[
                "required_example"
            ],
            enum=[
                None
            ],
            type_of="array",
            not_of=FormJSONSchema(),
            all_of=[
                FormJSONSchema()
            ],
            one_of=[],
            any_of=[],
            items=FormJSONSchema(),
            properties=FormJSONSchemaProperties(
                key=FormJSONSchema(),
            ),
            additional_properties=True,
            description="description_example",
            format_type="format_type_example",
            default=None,
            nullable=False,
            read_only=False,
            write_only=False,
            example=None,
            deprecated=False,
        ),
    )
    try:
        api_response = api_instance.create_form_schema(
            body=body,
        )
        pprint(api_response)
    except api_python_client.ApiException as e:
        print("Exception when calling DefaultApi->create_form_schema: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

#### SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**FormSchemaInput**](FormSchemaInput.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | ApiResponseFor200 | The newly created schema

#### ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**FormSchema**](FormSchema.md) |  | 



[**FormSchema**](FormSchema.md)

### Authorization

No authorization required

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_form_schema**
> FormSchema delete_form_schema(schema_id)



Delete a form schema

### Example

```python
import api_python_client
from api_python_client.api import default_api
from api_python_client.model.form_schema import FormSchema
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = api_python_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with api_python_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'schemaId': "schemaId_example",
    }
    try:
        api_response = api_instance.delete_form_schema(
            path_params=path_params,
        )
        pprint(api_response)
    except api_python_client.ApiException as e:
        print("Exception when calling DefaultApi->delete_form_schema: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
schemaId | SchemaIdSchema | | 

#### SchemaIdSchema

Type | Description | Notes
------------- | ------------- | -------------
**str** |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | ApiResponseFor200 | The deleted schema

#### ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**FormSchema**](FormSchema.md) |  | 



[**FormSchema**](FormSchema.md)

### Authorization

No authorization required

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_document**
> DocumentMetadata get_document(document_id)



Get details about a document being ingested

### Example

```python
import api_python_client
from api_python_client.api import default_api
from api_python_client.model.api_error import ApiError
from api_python_client.model.document_metadata import DocumentMetadata
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = api_python_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with api_python_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'documentId': "documentId_example",
    }
    try:
        api_response = api_instance.get_document(
            path_params=path_params,
        )
        pprint(api_response)
    except api_python_client.ApiException as e:
        print("Exception when calling DefaultApi->get_document: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
documentId | DocumentIdSchema | | 

#### DocumentIdSchema

Type | Description | Notes
------------- | ------------- | -------------
**str** |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | ApiResponseFor200 | Returned on successful retrieval of document metadata
404 | ApiResponseFor404 | Returned when a document is not found

#### ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DocumentMetadata**](DocumentMetadata.md) |  | 


#### ApiResponseFor404
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor404ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor404ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiError**](ApiError.md) |  | 



[**DocumentMetadata**](DocumentMetadata.md)

### Authorization

No authorization required

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_document_form**
> FormMetadata get_document_form(document_idform_id)



Get details about a form within a processed document

### Example

```python
import api_python_client
from api_python_client.api import default_api
from api_python_client.model.api_error import ApiError
from api_python_client.model.form_metadata import FormMetadata
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = api_python_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with api_python_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'documentId': "documentId_example",
        'formId': "formId_example",
    }
    try:
        api_response = api_instance.get_document_form(
            path_params=path_params,
        )
        pprint(api_response)
    except api_python_client.ApiException as e:
        print("Exception when calling DefaultApi->get_document_form: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
documentId | DocumentIdSchema | | 
formId | FormIdSchema | | 

#### DocumentIdSchema

Type | Description | Notes
------------- | ------------- | -------------
**str** |  | 

#### FormIdSchema

Type | Description | Notes
------------- | ------------- | -------------
**str** |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | ApiResponseFor200 | Returned on successful retrieval of the form
404 | ApiResponseFor404 | Returned when a document is not found

#### ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**FormMetadata**](FormMetadata.md) |  | 


#### ApiResponseFor404
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor404ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor404ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiError**](ApiError.md) |  | 



[**FormMetadata**](FormMetadata.md)

### Authorization

No authorization required

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_document_upload_url**
> GetDocumentUploadUrlResponse get_document_upload_url(file_namecontent_type)



Get a presigned url for uploading a document

### Example

```python
import api_python_client
from api_python_client.api import default_api
from api_python_client.model.get_document_upload_url_response import GetDocumentUploadUrlResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = api_python_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with api_python_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)

    # example passing only required values which don't have defaults set
    query_params = {
        'fileName': "fileName_example",
        'contentType': "contentType_example",
    }
    try:
        api_response = api_instance.get_document_upload_url(
            query_params=query_params,
        )
        pprint(api_response)
    except api_python_client.ApiException as e:
        print("Exception when calling DefaultApi->get_document_upload_url: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
fileName | FileNameSchema | | 
contentType | ContentTypeSchema | | 


#### FileNameSchema

Type | Description | Notes
------------- | ------------- | -------------
**str** |  | 

#### ContentTypeSchema

Type | Description | Notes
------------- | ------------- | -------------
**str** |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | ApiResponseFor200 | Returned presigned url for uploading a document

#### ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**GetDocumentUploadUrlResponse**](GetDocumentUploadUrlResponse.md) |  | 



[**GetDocumentUploadUrlResponse**](GetDocumentUploadUrlResponse.md)

### Authorization

No authorization required

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_form_schema**
> FormSchema get_form_schema(schema_id)



Retrieve a specific form schema

### Example

```python
import api_python_client
from api_python_client.api import default_api
from api_python_client.model.form_schema import FormSchema
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = api_python_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with api_python_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'schemaId': "schemaId_example",
    }
    try:
        api_response = api_instance.get_form_schema(
            path_params=path_params,
        )
        pprint(api_response)
    except api_python_client.ApiException as e:
        print("Exception when calling DefaultApi->get_form_schema: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
schemaId | SchemaIdSchema | | 

#### SchemaIdSchema

Type | Description | Notes
------------- | ------------- | -------------
**str** |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | ApiResponseFor200 | The newly created schema

#### ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**FormSchema**](FormSchema.md) |  | 



[**FormSchema**](FormSchema.md)

### Authorization

No authorization required

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_metrics**
> AggregateMetrics get_metrics(start_timestampend_timestamp)



Retrieve average aggregate metrics for disclosure data extraction for the given time period

### Example

```python
import api_python_client
from api_python_client.api import default_api
from api_python_client.model.aggregate_metrics import AggregateMetrics
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = api_python_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with api_python_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)

    # example passing only required values which don't have defaults set
    query_params = {
        'startTimestamp': "startTimestamp_example",
        'endTimestamp': "endTimestamp_example",
    }
    try:
        api_response = api_instance.get_metrics(
            query_params=query_params,
        )
        pprint(api_response)
    except api_python_client.ApiException as e:
        print("Exception when calling DefaultApi->get_metrics: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
startTimestamp | StartTimestampSchema | | 
endTimestamp | EndTimestampSchema | | 


#### StartTimestampSchema

Type | Description | Notes
------------- | ------------- | -------------
**str** |  | 

#### EndTimestampSchema

Type | Description | Notes
------------- | ------------- | -------------
**str** |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | ApiResponseFor200 | Aggregate metrics

#### ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**AggregateMetrics**](AggregateMetrics.md) |  | 



[**AggregateMetrics**](AggregateMetrics.md)

### Authorization

No authorization required

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_document_forms**
> ListFormsResponse list_document_forms(document_idpage_size)



Get details about the forms within a processed document

### Example

```python
import api_python_client
from api_python_client.api import default_api
from api_python_client.model.api_error import ApiError
from api_python_client.model.list_forms_response import ListFormsResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = api_python_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with api_python_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'documentId': "documentId_example",
    }
    query_params = {
        'pageSize': 1,
    }
    try:
        api_response = api_instance.list_document_forms(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except api_python_client.ApiException as e:
        print("Exception when calling DefaultApi->list_document_forms: %s\n" % e)

    # example passing only optional values
    path_params = {
        'documentId': "documentId_example",
    }
    query_params = {
        'pageSize': 1,
        'nextToken': "nextToken_example",
    }
    try:
        api_response = api_instance.list_document_forms(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except api_python_client.ApiException as e:
        print("Exception when calling DefaultApi->list_document_forms: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
pageSize | PageSizeSchema | | 
nextToken | NextTokenSchema | | optional


#### PageSizeSchema

Type | Description | Notes
------------- | ------------- | -------------
**int** |  | 

#### NextTokenSchema

Type | Description | Notes
------------- | ------------- | -------------
**str** |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
documentId | DocumentIdSchema | | 

#### DocumentIdSchema

Type | Description | Notes
------------- | ------------- | -------------
**str** |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | ApiResponseFor200 | Returned on successful retrieval of document forms
404 | ApiResponseFor404 | Returned when a document is not found

#### ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ListFormsResponse**](ListFormsResponse.md) |  | 


#### ApiResponseFor404
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor404ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor404ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiError**](ApiError.md) |  | 



[**ListFormsResponse**](ListFormsResponse.md)

### Authorization

No authorization required

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_documents**
> ListDocumentsResponse list_documents(page_size)



List all documents

### Example

```python
import api_python_client
from api_python_client.api import default_api
from api_python_client.model.list_documents_response import ListDocumentsResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = api_python_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with api_python_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)

    # example passing only required values which don't have defaults set
    query_params = {
        'pageSize': 1,
    }
    try:
        api_response = api_instance.list_documents(
            query_params=query_params,
        )
        pprint(api_response)
    except api_python_client.ApiException as e:
        print("Exception when calling DefaultApi->list_documents: %s\n" % e)

    # example passing only optional values
    query_params = {
        'pageSize': 1,
        'nextToken': "nextToken_example",
    }
    try:
        api_response = api_instance.list_documents(
            query_params=query_params,
        )
        pprint(api_response)
    except api_python_client.ApiException as e:
        print("Exception when calling DefaultApi->list_documents: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
pageSize | PageSizeSchema | | 
nextToken | NextTokenSchema | | optional


#### PageSizeSchema

Type | Description | Notes
------------- | ------------- | -------------
**int** |  | 

#### NextTokenSchema

Type | Description | Notes
------------- | ------------- | -------------
**str** |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | ApiResponseFor200 | Returns a list of documents

#### ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ListDocumentsResponse**](ListDocumentsResponse.md) |  | 



[**ListDocumentsResponse**](ListDocumentsResponse.md)

### Authorization

No authorization required

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_form_review_workflow_tags**
> ListFormReviewWorkflowTagsResponse list_form_review_workflow_tags(page_size)



List all form review workflow tags

### Example

```python
import api_python_client
from api_python_client.api import default_api
from api_python_client.model.list_form_review_workflow_tags_response import ListFormReviewWorkflowTagsResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = api_python_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with api_python_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)

    # example passing only required values which don't have defaults set
    query_params = {
        'pageSize': 1,
    }
    try:
        api_response = api_instance.list_form_review_workflow_tags(
            query_params=query_params,
        )
        pprint(api_response)
    except api_python_client.ApiException as e:
        print("Exception when calling DefaultApi->list_form_review_workflow_tags: %s\n" % e)

    # example passing only optional values
    query_params = {
        'pageSize': 1,
        'nextToken': "nextToken_example",
    }
    try:
        api_response = api_instance.list_form_review_workflow_tags(
            query_params=query_params,
        )
        pprint(api_response)
    except api_python_client.ApiException as e:
        print("Exception when calling DefaultApi->list_form_review_workflow_tags: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
pageSize | PageSizeSchema | | 
nextToken | NextTokenSchema | | optional


#### PageSizeSchema

Type | Description | Notes
------------- | ------------- | -------------
**int** |  | 

#### NextTokenSchema

Type | Description | Notes
------------- | ------------- | -------------
**str** |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | ApiResponseFor200 | Returned on successful list of all form review workflow tags

#### ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ListFormReviewWorkflowTagsResponse**](ListFormReviewWorkflowTagsResponse.md) |  | 



[**ListFormReviewWorkflowTagsResponse**](ListFormReviewWorkflowTagsResponse.md)

### Authorization

No authorization required

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_form_schemas**
> ListFormSchemasResponse list_form_schemas(page_size)



List all schemas for forms

### Example

```python
import api_python_client
from api_python_client.api import default_api
from api_python_client.model.list_form_schemas_response import ListFormSchemasResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = api_python_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with api_python_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)

    # example passing only required values which don't have defaults set
    query_params = {
        'pageSize': 1,
    }
    try:
        api_response = api_instance.list_form_schemas(
            query_params=query_params,
        )
        pprint(api_response)
    except api_python_client.ApiException as e:
        print("Exception when calling DefaultApi->list_form_schemas: %s\n" % e)

    # example passing only optional values
    query_params = {
        'pageSize': 1,
        'nextToken': "nextToken_example",
    }
    try:
        api_response = api_instance.list_form_schemas(
            query_params=query_params,
        )
        pprint(api_response)
    except api_python_client.ApiException as e:
        print("Exception when calling DefaultApi->list_form_schemas: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
pageSize | PageSizeSchema | | 
nextToken | NextTokenSchema | | optional


#### PageSizeSchema

Type | Description | Notes
------------- | ------------- | -------------
**int** |  | 

#### NextTokenSchema

Type | Description | Notes
------------- | ------------- | -------------
**str** |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | ApiResponseFor200 | List all registered form schemas

#### ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ListFormSchemasResponse**](ListFormSchemasResponse.md) |  | 



[**ListFormSchemasResponse**](ListFormSchemasResponse.md)

### Authorization

No authorization required

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_forms**
> ListFormsResponse list_forms(page_size)



List all forms within documents

### Example

```python
import api_python_client
from api_python_client.api import default_api
from api_python_client.model.list_forms_response import ListFormsResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = api_python_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with api_python_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)

    # example passing only required values which don't have defaults set
    query_params = {
        'pageSize': 1,
    }
    try:
        api_response = api_instance.list_forms(
            query_params=query_params,
        )
        pprint(api_response)
    except api_python_client.ApiException as e:
        print("Exception when calling DefaultApi->list_forms: %s\n" % e)

    # example passing only optional values
    query_params = {
        'pageSize': 1,
        'nextToken': "nextToken_example",
    }
    try:
        api_response = api_instance.list_forms(
            query_params=query_params,
        )
        pprint(api_response)
    except api_python_client.ApiException as e:
        print("Exception when calling DefaultApi->list_forms: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
pageSize | PageSizeSchema | | 
nextToken | NextTokenSchema | | optional


#### PageSizeSchema

Type | Description | Notes
------------- | ------------- | -------------
**int** |  | 

#### NextTokenSchema

Type | Description | Notes
------------- | ------------- | -------------
**str** |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | ApiResponseFor200 | Returns a list of forms

#### ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ListFormsResponse**](ListFormsResponse.md) |  | 



[**ListFormsResponse**](ListFormsResponse.md)

### Authorization

No authorization required

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **submit_source_document**
> DocumentMetadata submit_source_document(submit_source_document_input)



Submit a document for processing

### Example

```python
import api_python_client
from api_python_client.api import default_api
from api_python_client.model.document_metadata import DocumentMetadata
from api_python_client.model.submit_source_document_input import SubmitSourceDocumentInput
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = api_python_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with api_python_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)

    # example passing only required values which don't have defaults set
    body = SubmitSourceDocumentInput(
        schema_id="schema_id_example",
        document_id="document_id_example",
        name="name_example",
        location=S3Location(
            bucket="bucket_example",
            objectKey="key_example",
        ),
    )
    try:
        api_response = api_instance.submit_source_document(
            body=body,
        )
        pprint(api_response)
    except api_python_client.ApiException as e:
        print("Exception when calling DefaultApi->submit_source_document: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

#### SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**SubmitSourceDocumentInput**](SubmitSourceDocumentInput.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | ApiResponseFor200 | Returned on successful submission of a form

#### ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DocumentMetadata**](DocumentMetadata.md) |  | 



[**DocumentMetadata**](DocumentMetadata.md)

### Authorization

No authorization required

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_form_review**
> FormMetadata update_form_review(document_idform_idupdate_form_input)



Update the extracted data details object from a document form

### Example

```python
import api_python_client
from api_python_client.api import default_api
from api_python_client.model.api_error import ApiError
from api_python_client.model.update_form_input import UpdateFormInput
from api_python_client.model.form_metadata import FormMetadata
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = api_python_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with api_python_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'documentId': "documentId_example",
        'formId': "formId_example",
    }
    body = UpdateFormInput(
        extracted_data=dict(),
        tags=[
            "tags_example"
        ],
        notes="notes_example",
    )
    try:
        api_response = api_instance.update_form_review(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except api_python_client.ApiException as e:
        print("Exception when calling DefaultApi->update_form_review: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

#### SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**UpdateFormInput**](UpdateFormInput.md) |  | 


### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
documentId | DocumentIdSchema | | 
formId | FormIdSchema | | 

#### DocumentIdSchema

Type | Description | Notes
------------- | ------------- | -------------
**str** |  | 

#### FormIdSchema

Type | Description | Notes
------------- | ------------- | -------------
**str** |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | ApiResponseFor200 | Returned on successful update of the form
404 | ApiResponseFor404 | Returned when a document is not found

#### ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**FormMetadata**](FormMetadata.md) |  | 


#### ApiResponseFor404
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor404ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor404ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiError**](ApiError.md) |  | 



[**FormMetadata**](FormMetadata.md)

### Authorization

No authorization required

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_form_schema**
> FormSchema update_form_schema(schema_idform_schema)



Update an existing form schema

### Example

```python
import api_python_client
from api_python_client.api import default_api
from api_python_client.model.form_schema import FormSchema
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = api_python_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with api_python_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'schemaId': "schemaId_example",
    }
    body = FormSchema(
        schema_id="schema_id_example",
        title="title_example",
        description="description_example",
        schema=FormJSONSchema(
            order=1,
            extraction_metadata=FormFieldExtractionMetadata(
                form_key="form_key_example",
                table_position=1,
                row_position=1,
                column_position=1,
                textract_query="textract_query_example",
            ),
            title="title_example",
            multiple_of=0,
            maximum=3.14,
            exclusive_maximum=False,
            minimum=3.14,
            exclusive_minimum=False,
            max_length=0,
            min_length=0,
            pattern="pattern_example",
            max_items=0,
            min_items=0,
            unique_items=False,
            max_properties=0,
            min_properties=0,
            required=[
                "required_example"
            ],
            enum=[
                None
            ],
            type_of="array",
            not_of=FormJSONSchema(),
            all_of=[
                FormJSONSchema()
            ],
            one_of=[],
            any_of=[],
            items=FormJSONSchema(),
            properties=FormJSONSchemaProperties(
                key=FormJSONSchema(),
            ),
            additional_properties=True,
            description="description_example",
            format_type="format_type_example",
            default=None,
            nullable=False,
            read_only=False,
            write_only=False,
            example=None,
            deprecated=False,
        ),
        created_by="created_by_example",
        updated_by="updated_by_example",
        created_timestamp="created_timestamp_example",
        updated_timestamp="updated_timestamp_example",
    )
    try:
        api_response = api_instance.update_form_schema(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except api_python_client.ApiException as e:
        print("Exception when calling DefaultApi->update_form_schema: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

#### SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**FormSchema**](FormSchema.md) |  | 


### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
schemaId | SchemaIdSchema | | 

#### SchemaIdSchema

Type | Description | Notes
------------- | ------------- | -------------
**str** |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | ApiResponseFor200 | The updated schema

#### ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**FormSchema**](FormSchema.md) |  | 



[**FormSchema**](FormSchema.md)

### Authorization

No authorization required

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_status**
> FormMetadata update_status(document_idform_idupdate_status_input)



start a new review

### Example

```python
import api_python_client
from api_python_client.api import default_api
from api_python_client.model.form_metadata import FormMetadata
from api_python_client.model.update_status_input import UpdateStatusInput
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = api_python_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with api_python_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'documentId': "documentId_example",
        'formId': "formId_example",
    }
    body = UpdateStatusInput(
        new_status="new_status_example",
    )
    try:
        api_response = api_instance.update_status(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except api_python_client.ApiException as e:
        print("Exception when calling DefaultApi->update_status: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

#### SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**UpdateStatusInput**](UpdateStatusInput.md) |  | 


### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
documentId | DocumentIdSchema | | 
formId | FormIdSchema | | 

#### DocumentIdSchema

Type | Description | Notes
------------- | ------------- | -------------
**str** |  | 

#### FormIdSchema

Type | Description | Notes
------------- | ------------- | -------------
**str** |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | ApiResponseFor200 | The newly updated form metadata

#### ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**FormMetadata**](FormMetadata.md) |  | 



[**FormMetadata**](FormMetadata.md)

### Authorization

No authorization required

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

