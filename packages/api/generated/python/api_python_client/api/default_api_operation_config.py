import urllib.parse
import json
from typing import Callable, Any, Dict, List, NamedTuple, TypeVar, Generic, Union, TypedDict, Protocol, Optional
from functools import wraps
from dataclasses import dataclass

from api_python_client.model.aggregate_metrics import AggregateMetrics
from api_python_client.model.api_error import ApiError
from api_python_client.model.create_form_review_workflow_tag_input import CreateFormReviewWorkflowTagInput
from api_python_client.model.document_metadata import DocumentMetadata
from api_python_client.model.form_metadata import FormMetadata
from api_python_client.model.form_review_workflow_tag import FormReviewWorkflowTag
from api_python_client.model.form_schema import FormSchema
from api_python_client.model.form_schema_input import FormSchemaInput
from api_python_client.model.get_document_upload_url_response import GetDocumentUploadUrlResponse
from api_python_client.model.list_documents_response import ListDocumentsResponse
from api_python_client.model.list_form_review_workflow_tags_response import ListFormReviewWorkflowTagsResponse
from api_python_client.model.list_form_schemas_response import ListFormSchemasResponse
from api_python_client.model.list_forms_response import ListFormsResponse
from api_python_client.model.submit_source_document_input import SubmitSourceDocumentInput
from api_python_client.model.update_form_input import UpdateFormInput
from api_python_client.model.update_status_input import UpdateStatusInput

from api_python_client.schemas import (
    date,
    datetime,
    file_type,
    none_type,
)

T = TypeVar('T')

# Generic type for object keyed by operation names
@dataclass
class OperationConfig(Generic[T]):
    create_form_review_workflow_tag: T
    create_form_schema: T
    delete_form_schema: T
    get_document: T
    get_document_form: T
    get_document_upload_url: T
    get_form_schema: T
    get_metrics: T
    list_document_forms: T
    list_documents: T
    list_form_review_workflow_tags: T
    list_form_schemas: T
    list_forms: T
    submit_source_document: T
    update_form_review: T
    update_form_schema: T
    update_status: T
    ...

# Look up path and http method for a given operation name
OperationLookup = {
    "create_form_review_workflow_tag": {
        "path": "/tags",
        "method": "POST",
    },
    "create_form_schema": {
        "path": "/schemas",
        "method": "POST",
    },
    "delete_form_schema": {
        "path": "/schemas/{schemaId}",
        "method": "DELETE",
    },
    "get_document": {
        "path": "/documents/{documentId}",
        "method": "GET",
    },
    "get_document_form": {
        "path": "/documents/{documentId}/forms/{formId}",
        "method": "GET",
    },
    "get_document_upload_url": {
        "path": "/documents/upload-url",
        "method": "GET",
    },
    "get_form_schema": {
        "path": "/schemas/{schemaId}",
        "method": "GET",
    },
    "get_metrics": {
        "path": "/metrics",
        "method": "GET",
    },
    "list_document_forms": {
        "path": "/documents/{documentId}/forms",
        "method": "GET",
    },
    "list_documents": {
        "path": "/documents",
        "method": "GET",
    },
    "list_form_review_workflow_tags": {
        "path": "/tags",
        "method": "GET",
    },
    "list_form_schemas": {
        "path": "/schemas",
        "method": "GET",
    },
    "list_forms": {
        "path": "/forms",
        "method": "GET",
    },
    "submit_source_document": {
        "path": "/sources/document",
        "method": "POST",
    },
    "update_form_review": {
        "path": "/documents/{documentId}/forms/{formId}/review",
        "method": "PUT",
    },
    "update_form_schema": {
        "path": "/schemas/{schemaId}",
        "method": "PUT",
    },
    "update_status": {
        "path": "/documents/{documentId}/forms/{formId}/status",
        "method": "PUT",
    },
}

def uri_decode(value):
    """
    URI decode a value or list of values
    """
    if isinstance(value, list):
        return [urllib.parse.unquote(v) for v in value]
    return urllib.parse.unquote(value)

def decode_request_parameters(parameters):
    """
    URI decode api request parameters (path, query or multi-value query)
    """
    return { key: uri_decode(parameters[key]) if parameters[key] is not None else parameters[key] for key in parameters.keys() }

def parse_body(body, content_types, model):
    """
    Parse the body of an api request into the given model if present
    """
    if len([c for c in content_types if c != 'application/json']) == 0:
        body = json.loads(body or '{}')
        if model != Any:
            body = model(**body)
    return body


RequestParameters = TypeVar('RequestParameters')
RequestArrayParameters = TypeVar('RequestArrayParameters')
RequestBody = TypeVar('RequestBody')


@dataclass
class ApiRequest(Generic[RequestParameters, RequestArrayParameters, RequestBody]):
    request_parameters: RequestParameters
    request_array_parameters: RequestArrayParameters
    body: RequestBody
    event: Any
    context: Any


ResponseBody = TypeVar('ResponseBody')
ApiError = TypeVar('ApiError')


@dataclass
class ApiResponse(Generic[ResponseBody, ApiError]):
    status_code: int
    headers: Dict[str, str]
    body: Union[ResponseBody, ApiError]



# Request parameters are single value query params or path params
class CreateFormReviewWorkflowTagRequestParameters(TypedDict):
    ...

# Request array parameters are multi-value query params
class CreateFormReviewWorkflowTagRequestArrayParameters(TypedDict):
    ...

# Request body type (default to Any when no body parameters exist)
CreateFormReviewWorkflowTagRequestBody = CreateFormReviewWorkflowTagInput

# Request type for create_form_review_workflow_tag
CreateFormReviewWorkflowTagRequest = ApiRequest[CreateFormReviewWorkflowTagRequestParameters, CreateFormReviewWorkflowTagRequestArrayParameters, CreateFormReviewWorkflowTagRequestBody]

class CreateFormReviewWorkflowTagHandlerFunction(Protocol):
    def __call__(self, input: CreateFormReviewWorkflowTagRequest, **kwargs) -> ApiResponse[FormReviewWorkflowTag, ApiError]:
        ...

def create_form_review_workflow_tag_handler(handler: CreateFormReviewWorkflowTagHandlerFunction):
    """
    Decorator for an api handler for the create_form_review_workflow_tag operation, providing a typed interface for inputs and outputs
    """
    @wraps(handler)
    def wrapper(event, context, **kwargs):
        request_parameters = decode_request_parameters({
            **(event['pathParameters'] or {}),
            **(event['queryStringParameters'] or {}),
        })
        request_array_parameters = decode_request_parameters({
            **(event['multiValueQueryStringParameters'] or {}),
        })
        body = parse_body(event['body'], ['application/json',], CreateFormReviewWorkflowTagRequestBody)
        response = handler(ApiRequest(
            request_parameters,
            request_array_parameters,
            body,
            event,
            context,
        ), **kwargs)
        return {
            'statusCode': response.status_code,
            'headers': response.headers,
            'body': json.dumps(response.body) if response.body is not None else '',
        }
    return wrapper


# Request parameters are single value query params or path params
class CreateFormSchemaRequestParameters(TypedDict):
    ...

# Request array parameters are multi-value query params
class CreateFormSchemaRequestArrayParameters(TypedDict):
    ...

# Request body type (default to Any when no body parameters exist)
CreateFormSchemaRequestBody = FormSchemaInput

# Request type for create_form_schema
CreateFormSchemaRequest = ApiRequest[CreateFormSchemaRequestParameters, CreateFormSchemaRequestArrayParameters, CreateFormSchemaRequestBody]

class CreateFormSchemaHandlerFunction(Protocol):
    def __call__(self, input: CreateFormSchemaRequest, **kwargs) -> ApiResponse[FormSchema, ApiError]:
        ...

def create_form_schema_handler(handler: CreateFormSchemaHandlerFunction):
    """
    Decorator for an api handler for the create_form_schema operation, providing a typed interface for inputs and outputs
    """
    @wraps(handler)
    def wrapper(event, context, **kwargs):
        request_parameters = decode_request_parameters({
            **(event['pathParameters'] or {}),
            **(event['queryStringParameters'] or {}),
        })
        request_array_parameters = decode_request_parameters({
            **(event['multiValueQueryStringParameters'] or {}),
        })
        body = parse_body(event['body'], ['application/json',], CreateFormSchemaRequestBody)
        response = handler(ApiRequest(
            request_parameters,
            request_array_parameters,
            body,
            event,
            context,
        ), **kwargs)
        return {
            'statusCode': response.status_code,
            'headers': response.headers,
            'body': json.dumps(response.body) if response.body is not None else '',
        }
    return wrapper


# Request parameters are single value query params or path params
class DeleteFormSchemaRequestParameters(TypedDict):
    schemaId: str
    ...

# Request array parameters are multi-value query params
class DeleteFormSchemaRequestArrayParameters(TypedDict):
    ...

# Request body type (default to Any when no body parameters exist)
DeleteFormSchemaRequestBody = Any

# Request type for delete_form_schema
DeleteFormSchemaRequest = ApiRequest[DeleteFormSchemaRequestParameters, DeleteFormSchemaRequestArrayParameters, DeleteFormSchemaRequestBody]

class DeleteFormSchemaHandlerFunction(Protocol):
    def __call__(self, input: DeleteFormSchemaRequest, **kwargs) -> ApiResponse[FormSchema, ApiError]:
        ...

def delete_form_schema_handler(handler: DeleteFormSchemaHandlerFunction):
    """
    Decorator for an api handler for the delete_form_schema operation, providing a typed interface for inputs and outputs
    """
    @wraps(handler)
    def wrapper(event, context, **kwargs):
        request_parameters = decode_request_parameters({
            **(event['pathParameters'] or {}),
            **(event['queryStringParameters'] or {}),
        })
        request_array_parameters = decode_request_parameters({
            **(event['multiValueQueryStringParameters'] or {}),
        })
        body = parse_body(event['body'], [], DeleteFormSchemaRequestBody)
        response = handler(ApiRequest(
            request_parameters,
            request_array_parameters,
            body,
            event,
            context,
        ), **kwargs)
        return {
            'statusCode': response.status_code,
            'headers': response.headers,
            'body': json.dumps(response.body) if response.body is not None else '',
        }
    return wrapper


# Request parameters are single value query params or path params
class GetDocumentRequestParameters(TypedDict):
    documentId: str
    ...

# Request array parameters are multi-value query params
class GetDocumentRequestArrayParameters(TypedDict):
    ...

# Request body type (default to Any when no body parameters exist)
GetDocumentRequestBody = Any

# Request type for get_document
GetDocumentRequest = ApiRequest[GetDocumentRequestParameters, GetDocumentRequestArrayParameters, GetDocumentRequestBody]

class GetDocumentHandlerFunction(Protocol):
    def __call__(self, input: GetDocumentRequest, **kwargs) -> ApiResponse[DocumentMetadata, ApiError]:
        ...

def get_document_handler(handler: GetDocumentHandlerFunction):
    """
    Decorator for an api handler for the get_document operation, providing a typed interface for inputs and outputs
    """
    @wraps(handler)
    def wrapper(event, context, **kwargs):
        request_parameters = decode_request_parameters({
            **(event['pathParameters'] or {}),
            **(event['queryStringParameters'] or {}),
        })
        request_array_parameters = decode_request_parameters({
            **(event['multiValueQueryStringParameters'] or {}),
        })
        body = parse_body(event['body'], [], GetDocumentRequestBody)
        response = handler(ApiRequest(
            request_parameters,
            request_array_parameters,
            body,
            event,
            context,
        ), **kwargs)
        return {
            'statusCode': response.status_code,
            'headers': response.headers,
            'body': json.dumps(response.body) if response.body is not None else '',
        }
    return wrapper


# Request parameters are single value query params or path params
class GetDocumentFormRequestParameters(TypedDict):
    documentId: str
    formId: str
    ...

# Request array parameters are multi-value query params
class GetDocumentFormRequestArrayParameters(TypedDict):
    ...

# Request body type (default to Any when no body parameters exist)
GetDocumentFormRequestBody = Any

# Request type for get_document_form
GetDocumentFormRequest = ApiRequest[GetDocumentFormRequestParameters, GetDocumentFormRequestArrayParameters, GetDocumentFormRequestBody]

class GetDocumentFormHandlerFunction(Protocol):
    def __call__(self, input: GetDocumentFormRequest, **kwargs) -> ApiResponse[FormMetadata, ApiError]:
        ...

def get_document_form_handler(handler: GetDocumentFormHandlerFunction):
    """
    Decorator for an api handler for the get_document_form operation, providing a typed interface for inputs and outputs
    """
    @wraps(handler)
    def wrapper(event, context, **kwargs):
        request_parameters = decode_request_parameters({
            **(event['pathParameters'] or {}),
            **(event['queryStringParameters'] or {}),
        })
        request_array_parameters = decode_request_parameters({
            **(event['multiValueQueryStringParameters'] or {}),
        })
        body = parse_body(event['body'], [], GetDocumentFormRequestBody)
        response = handler(ApiRequest(
            request_parameters,
            request_array_parameters,
            body,
            event,
            context,
        ), **kwargs)
        return {
            'statusCode': response.status_code,
            'headers': response.headers,
            'body': json.dumps(response.body) if response.body is not None else '',
        }
    return wrapper


# Request parameters are single value query params or path params
class GetDocumentUploadUrlRequestParameters(TypedDict):
    fileName: str
    contentType: str
    ...

# Request array parameters are multi-value query params
class GetDocumentUploadUrlRequestArrayParameters(TypedDict):
    ...

# Request body type (default to Any when no body parameters exist)
GetDocumentUploadUrlRequestBody = Any

# Request type for get_document_upload_url
GetDocumentUploadUrlRequest = ApiRequest[GetDocumentUploadUrlRequestParameters, GetDocumentUploadUrlRequestArrayParameters, GetDocumentUploadUrlRequestBody]

class GetDocumentUploadUrlHandlerFunction(Protocol):
    def __call__(self, input: GetDocumentUploadUrlRequest, **kwargs) -> ApiResponse[GetDocumentUploadUrlResponse, ApiError]:
        ...

def get_document_upload_url_handler(handler: GetDocumentUploadUrlHandlerFunction):
    """
    Decorator for an api handler for the get_document_upload_url operation, providing a typed interface for inputs and outputs
    """
    @wraps(handler)
    def wrapper(event, context, **kwargs):
        request_parameters = decode_request_parameters({
            **(event['pathParameters'] or {}),
            **(event['queryStringParameters'] or {}),
        })
        request_array_parameters = decode_request_parameters({
            **(event['multiValueQueryStringParameters'] or {}),
        })
        body = parse_body(event['body'], [], GetDocumentUploadUrlRequestBody)
        response = handler(ApiRequest(
            request_parameters,
            request_array_parameters,
            body,
            event,
            context,
        ), **kwargs)
        return {
            'statusCode': response.status_code,
            'headers': response.headers,
            'body': json.dumps(response.body) if response.body is not None else '',
        }
    return wrapper


# Request parameters are single value query params or path params
class GetFormSchemaRequestParameters(TypedDict):
    schemaId: str
    ...

# Request array parameters are multi-value query params
class GetFormSchemaRequestArrayParameters(TypedDict):
    ...

# Request body type (default to Any when no body parameters exist)
GetFormSchemaRequestBody = Any

# Request type for get_form_schema
GetFormSchemaRequest = ApiRequest[GetFormSchemaRequestParameters, GetFormSchemaRequestArrayParameters, GetFormSchemaRequestBody]

class GetFormSchemaHandlerFunction(Protocol):
    def __call__(self, input: GetFormSchemaRequest, **kwargs) -> ApiResponse[FormSchema, ApiError]:
        ...

def get_form_schema_handler(handler: GetFormSchemaHandlerFunction):
    """
    Decorator for an api handler for the get_form_schema operation, providing a typed interface for inputs and outputs
    """
    @wraps(handler)
    def wrapper(event, context, **kwargs):
        request_parameters = decode_request_parameters({
            **(event['pathParameters'] or {}),
            **(event['queryStringParameters'] or {}),
        })
        request_array_parameters = decode_request_parameters({
            **(event['multiValueQueryStringParameters'] or {}),
        })
        body = parse_body(event['body'], [], GetFormSchemaRequestBody)
        response = handler(ApiRequest(
            request_parameters,
            request_array_parameters,
            body,
            event,
            context,
        ), **kwargs)
        return {
            'statusCode': response.status_code,
            'headers': response.headers,
            'body': json.dumps(response.body) if response.body is not None else '',
        }
    return wrapper


# Request parameters are single value query params or path params
class GetMetricsRequestParameters(TypedDict):
    startTimestamp: str
    endTimestamp: str
    ...

# Request array parameters are multi-value query params
class GetMetricsRequestArrayParameters(TypedDict):
    ...

# Request body type (default to Any when no body parameters exist)
GetMetricsRequestBody = Any

# Request type for get_metrics
GetMetricsRequest = ApiRequest[GetMetricsRequestParameters, GetMetricsRequestArrayParameters, GetMetricsRequestBody]

class GetMetricsHandlerFunction(Protocol):
    def __call__(self, input: GetMetricsRequest, **kwargs) -> ApiResponse[AggregateMetrics, ApiError]:
        ...

def get_metrics_handler(handler: GetMetricsHandlerFunction):
    """
    Decorator for an api handler for the get_metrics operation, providing a typed interface for inputs and outputs
    """
    @wraps(handler)
    def wrapper(event, context, **kwargs):
        request_parameters = decode_request_parameters({
            **(event['pathParameters'] or {}),
            **(event['queryStringParameters'] or {}),
        })
        request_array_parameters = decode_request_parameters({
            **(event['multiValueQueryStringParameters'] or {}),
        })
        body = parse_body(event['body'], [], GetMetricsRequestBody)
        response = handler(ApiRequest(
            request_parameters,
            request_array_parameters,
            body,
            event,
            context,
        ), **kwargs)
        return {
            'statusCode': response.status_code,
            'headers': response.headers,
            'body': json.dumps(response.body) if response.body is not None else '',
        }
    return wrapper


# Request parameters are single value query params or path params
class ListDocumentFormsRequestParameters(TypedDict):
    documentId: str
    pageSize: str
    nextToken: str
    ...

# Request array parameters are multi-value query params
class ListDocumentFormsRequestArrayParameters(TypedDict):
    ...

# Request body type (default to Any when no body parameters exist)
ListDocumentFormsRequestBody = Any

# Request type for list_document_forms
ListDocumentFormsRequest = ApiRequest[ListDocumentFormsRequestParameters, ListDocumentFormsRequestArrayParameters, ListDocumentFormsRequestBody]

class ListDocumentFormsHandlerFunction(Protocol):
    def __call__(self, input: ListDocumentFormsRequest, **kwargs) -> ApiResponse[ListFormsResponse, ApiError]:
        ...

def list_document_forms_handler(handler: ListDocumentFormsHandlerFunction):
    """
    Decorator for an api handler for the list_document_forms operation, providing a typed interface for inputs and outputs
    """
    @wraps(handler)
    def wrapper(event, context, **kwargs):
        request_parameters = decode_request_parameters({
            **(event['pathParameters'] or {}),
            **(event['queryStringParameters'] or {}),
        })
        request_array_parameters = decode_request_parameters({
            **(event['multiValueQueryStringParameters'] or {}),
        })
        body = parse_body(event['body'], [], ListDocumentFormsRequestBody)
        response = handler(ApiRequest(
            request_parameters,
            request_array_parameters,
            body,
            event,
            context,
        ), **kwargs)
        return {
            'statusCode': response.status_code,
            'headers': response.headers,
            'body': json.dumps(response.body) if response.body is not None else '',
        }
    return wrapper


# Request parameters are single value query params or path params
class ListDocumentsRequestParameters(TypedDict):
    pageSize: str
    nextToken: str
    ...

# Request array parameters are multi-value query params
class ListDocumentsRequestArrayParameters(TypedDict):
    ...

# Request body type (default to Any when no body parameters exist)
ListDocumentsRequestBody = Any

# Request type for list_documents
ListDocumentsRequest = ApiRequest[ListDocumentsRequestParameters, ListDocumentsRequestArrayParameters, ListDocumentsRequestBody]

class ListDocumentsHandlerFunction(Protocol):
    def __call__(self, input: ListDocumentsRequest, **kwargs) -> ApiResponse[ListDocumentsResponse, ApiError]:
        ...

def list_documents_handler(handler: ListDocumentsHandlerFunction):
    """
    Decorator for an api handler for the list_documents operation, providing a typed interface for inputs and outputs
    """
    @wraps(handler)
    def wrapper(event, context, **kwargs):
        request_parameters = decode_request_parameters({
            **(event['pathParameters'] or {}),
            **(event['queryStringParameters'] or {}),
        })
        request_array_parameters = decode_request_parameters({
            **(event['multiValueQueryStringParameters'] or {}),
        })
        body = parse_body(event['body'], [], ListDocumentsRequestBody)
        response = handler(ApiRequest(
            request_parameters,
            request_array_parameters,
            body,
            event,
            context,
        ), **kwargs)
        return {
            'statusCode': response.status_code,
            'headers': response.headers,
            'body': json.dumps(response.body) if response.body is not None else '',
        }
    return wrapper


# Request parameters are single value query params or path params
class ListFormReviewWorkflowTagsRequestParameters(TypedDict):
    pageSize: str
    nextToken: str
    ...

# Request array parameters are multi-value query params
class ListFormReviewWorkflowTagsRequestArrayParameters(TypedDict):
    ...

# Request body type (default to Any when no body parameters exist)
ListFormReviewWorkflowTagsRequestBody = Any

# Request type for list_form_review_workflow_tags
ListFormReviewWorkflowTagsRequest = ApiRequest[ListFormReviewWorkflowTagsRequestParameters, ListFormReviewWorkflowTagsRequestArrayParameters, ListFormReviewWorkflowTagsRequestBody]

class ListFormReviewWorkflowTagsHandlerFunction(Protocol):
    def __call__(self, input: ListFormReviewWorkflowTagsRequest, **kwargs) -> ApiResponse[ListFormReviewWorkflowTagsResponse, ApiError]:
        ...

def list_form_review_workflow_tags_handler(handler: ListFormReviewWorkflowTagsHandlerFunction):
    """
    Decorator for an api handler for the list_form_review_workflow_tags operation, providing a typed interface for inputs and outputs
    """
    @wraps(handler)
    def wrapper(event, context, **kwargs):
        request_parameters = decode_request_parameters({
            **(event['pathParameters'] or {}),
            **(event['queryStringParameters'] or {}),
        })
        request_array_parameters = decode_request_parameters({
            **(event['multiValueQueryStringParameters'] or {}),
        })
        body = parse_body(event['body'], [], ListFormReviewWorkflowTagsRequestBody)
        response = handler(ApiRequest(
            request_parameters,
            request_array_parameters,
            body,
            event,
            context,
        ), **kwargs)
        return {
            'statusCode': response.status_code,
            'headers': response.headers,
            'body': json.dumps(response.body) if response.body is not None else '',
        }
    return wrapper


# Request parameters are single value query params or path params
class ListFormSchemasRequestParameters(TypedDict):
    pageSize: str
    nextToken: str
    ...

# Request array parameters are multi-value query params
class ListFormSchemasRequestArrayParameters(TypedDict):
    ...

# Request body type (default to Any when no body parameters exist)
ListFormSchemasRequestBody = Any

# Request type for list_form_schemas
ListFormSchemasRequest = ApiRequest[ListFormSchemasRequestParameters, ListFormSchemasRequestArrayParameters, ListFormSchemasRequestBody]

class ListFormSchemasHandlerFunction(Protocol):
    def __call__(self, input: ListFormSchemasRequest, **kwargs) -> ApiResponse[ListFormSchemasResponse, ApiError]:
        ...

def list_form_schemas_handler(handler: ListFormSchemasHandlerFunction):
    """
    Decorator for an api handler for the list_form_schemas operation, providing a typed interface for inputs and outputs
    """
    @wraps(handler)
    def wrapper(event, context, **kwargs):
        request_parameters = decode_request_parameters({
            **(event['pathParameters'] or {}),
            **(event['queryStringParameters'] or {}),
        })
        request_array_parameters = decode_request_parameters({
            **(event['multiValueQueryStringParameters'] or {}),
        })
        body = parse_body(event['body'], [], ListFormSchemasRequestBody)
        response = handler(ApiRequest(
            request_parameters,
            request_array_parameters,
            body,
            event,
            context,
        ), **kwargs)
        return {
            'statusCode': response.status_code,
            'headers': response.headers,
            'body': json.dumps(response.body) if response.body is not None else '',
        }
    return wrapper


# Request parameters are single value query params or path params
class ListFormsRequestParameters(TypedDict):
    pageSize: str
    nextToken: str
    ...

# Request array parameters are multi-value query params
class ListFormsRequestArrayParameters(TypedDict):
    ...

# Request body type (default to Any when no body parameters exist)
ListFormsRequestBody = Any

# Request type for list_forms
ListFormsRequest = ApiRequest[ListFormsRequestParameters, ListFormsRequestArrayParameters, ListFormsRequestBody]

class ListFormsHandlerFunction(Protocol):
    def __call__(self, input: ListFormsRequest, **kwargs) -> ApiResponse[ListFormsResponse, ApiError]:
        ...

def list_forms_handler(handler: ListFormsHandlerFunction):
    """
    Decorator for an api handler for the list_forms operation, providing a typed interface for inputs and outputs
    """
    @wraps(handler)
    def wrapper(event, context, **kwargs):
        request_parameters = decode_request_parameters({
            **(event['pathParameters'] or {}),
            **(event['queryStringParameters'] or {}),
        })
        request_array_parameters = decode_request_parameters({
            **(event['multiValueQueryStringParameters'] or {}),
        })
        body = parse_body(event['body'], [], ListFormsRequestBody)
        response = handler(ApiRequest(
            request_parameters,
            request_array_parameters,
            body,
            event,
            context,
        ), **kwargs)
        return {
            'statusCode': response.status_code,
            'headers': response.headers,
            'body': json.dumps(response.body) if response.body is not None else '',
        }
    return wrapper


# Request parameters are single value query params or path params
class SubmitSourceDocumentRequestParameters(TypedDict):
    ...

# Request array parameters are multi-value query params
class SubmitSourceDocumentRequestArrayParameters(TypedDict):
    ...

# Request body type (default to Any when no body parameters exist)
SubmitSourceDocumentRequestBody = SubmitSourceDocumentInput

# Request type for submit_source_document
SubmitSourceDocumentRequest = ApiRequest[SubmitSourceDocumentRequestParameters, SubmitSourceDocumentRequestArrayParameters, SubmitSourceDocumentRequestBody]

class SubmitSourceDocumentHandlerFunction(Protocol):
    def __call__(self, input: SubmitSourceDocumentRequest, **kwargs) -> ApiResponse[DocumentMetadata, ApiError]:
        ...

def submit_source_document_handler(handler: SubmitSourceDocumentHandlerFunction):
    """
    Decorator for an api handler for the submit_source_document operation, providing a typed interface for inputs and outputs
    """
    @wraps(handler)
    def wrapper(event, context, **kwargs):
        request_parameters = decode_request_parameters({
            **(event['pathParameters'] or {}),
            **(event['queryStringParameters'] or {}),
        })
        request_array_parameters = decode_request_parameters({
            **(event['multiValueQueryStringParameters'] or {}),
        })
        body = parse_body(event['body'], ['application/json',], SubmitSourceDocumentRequestBody)
        response = handler(ApiRequest(
            request_parameters,
            request_array_parameters,
            body,
            event,
            context,
        ), **kwargs)
        return {
            'statusCode': response.status_code,
            'headers': response.headers,
            'body': json.dumps(response.body) if response.body is not None else '',
        }
    return wrapper


# Request parameters are single value query params or path params
class UpdateFormReviewRequestParameters(TypedDict):
    documentId: str
    formId: str
    ...

# Request array parameters are multi-value query params
class UpdateFormReviewRequestArrayParameters(TypedDict):
    ...

# Request body type (default to Any when no body parameters exist)
UpdateFormReviewRequestBody = UpdateFormInput

# Request type for update_form_review
UpdateFormReviewRequest = ApiRequest[UpdateFormReviewRequestParameters, UpdateFormReviewRequestArrayParameters, UpdateFormReviewRequestBody]

class UpdateFormReviewHandlerFunction(Protocol):
    def __call__(self, input: UpdateFormReviewRequest, **kwargs) -> ApiResponse[FormMetadata, ApiError]:
        ...

def update_form_review_handler(handler: UpdateFormReviewHandlerFunction):
    """
    Decorator for an api handler for the update_form_review operation, providing a typed interface for inputs and outputs
    """
    @wraps(handler)
    def wrapper(event, context, **kwargs):
        request_parameters = decode_request_parameters({
            **(event['pathParameters'] or {}),
            **(event['queryStringParameters'] or {}),
        })
        request_array_parameters = decode_request_parameters({
            **(event['multiValueQueryStringParameters'] or {}),
        })
        body = parse_body(event['body'], ['application/json',], UpdateFormReviewRequestBody)
        response = handler(ApiRequest(
            request_parameters,
            request_array_parameters,
            body,
            event,
            context,
        ), **kwargs)
        return {
            'statusCode': response.status_code,
            'headers': response.headers,
            'body': json.dumps(response.body) if response.body is not None else '',
        }
    return wrapper


# Request parameters are single value query params or path params
class UpdateFormSchemaRequestParameters(TypedDict):
    schemaId: str
    ...

# Request array parameters are multi-value query params
class UpdateFormSchemaRequestArrayParameters(TypedDict):
    ...

# Request body type (default to Any when no body parameters exist)
UpdateFormSchemaRequestBody = FormSchema

# Request type for update_form_schema
UpdateFormSchemaRequest = ApiRequest[UpdateFormSchemaRequestParameters, UpdateFormSchemaRequestArrayParameters, UpdateFormSchemaRequestBody]

class UpdateFormSchemaHandlerFunction(Protocol):
    def __call__(self, input: UpdateFormSchemaRequest, **kwargs) -> ApiResponse[FormSchema, ApiError]:
        ...

def update_form_schema_handler(handler: UpdateFormSchemaHandlerFunction):
    """
    Decorator for an api handler for the update_form_schema operation, providing a typed interface for inputs and outputs
    """
    @wraps(handler)
    def wrapper(event, context, **kwargs):
        request_parameters = decode_request_parameters({
            **(event['pathParameters'] or {}),
            **(event['queryStringParameters'] or {}),
        })
        request_array_parameters = decode_request_parameters({
            **(event['multiValueQueryStringParameters'] or {}),
        })
        body = parse_body(event['body'], ['application/json',], UpdateFormSchemaRequestBody)
        response = handler(ApiRequest(
            request_parameters,
            request_array_parameters,
            body,
            event,
            context,
        ), **kwargs)
        return {
            'statusCode': response.status_code,
            'headers': response.headers,
            'body': json.dumps(response.body) if response.body is not None else '',
        }
    return wrapper


# Request parameters are single value query params or path params
class UpdateStatusRequestParameters(TypedDict):
    documentId: str
    formId: str
    ...

# Request array parameters are multi-value query params
class UpdateStatusRequestArrayParameters(TypedDict):
    ...

# Request body type (default to Any when no body parameters exist)
UpdateStatusRequestBody = UpdateStatusInput

# Request type for update_status
UpdateStatusRequest = ApiRequest[UpdateStatusRequestParameters, UpdateStatusRequestArrayParameters, UpdateStatusRequestBody]

class UpdateStatusHandlerFunction(Protocol):
    def __call__(self, input: UpdateStatusRequest, **kwargs) -> ApiResponse[FormMetadata, ApiError]:
        ...

def update_status_handler(handler: UpdateStatusHandlerFunction):
    """
    Decorator for an api handler for the update_status operation, providing a typed interface for inputs and outputs
    """
    @wraps(handler)
    def wrapper(event, context, **kwargs):
        request_parameters = decode_request_parameters({
            **(event['pathParameters'] or {}),
            **(event['queryStringParameters'] or {}),
        })
        request_array_parameters = decode_request_parameters({
            **(event['multiValueQueryStringParameters'] or {}),
        })
        body = parse_body(event['body'], ['application/json',], UpdateStatusRequestBody)
        response = handler(ApiRequest(
            request_parameters,
            request_array_parameters,
            body,
            event,
            context,
        ), **kwargs)
        return {
            'statusCode': response.status_code,
            'headers': response.headers,
            'body': json.dumps(response.body) if response.body is not None else '',
        }
    return wrapper

