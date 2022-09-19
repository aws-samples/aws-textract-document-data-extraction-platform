import urllib.parse
import json
from typing import Callable, Any, Dict, List, NamedTuple, TypeVar, Generic, Union, TypedDict, Protocol, Optional, Literal
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
from api_python_client.api_client import JSONEncoder

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
        "method": "post",
    },
    "create_form_schema": {
        "path": "/schemas",
        "method": "post",
    },
    "delete_form_schema": {
        "path": "/schemas/{schemaId}",
        "method": "delete",
    },
    "get_document": {
        "path": "/documents/{documentId}",
        "method": "get",
    },
    "get_document_form": {
        "path": "/documents/{documentId}/forms/{formId}",
        "method": "get",
    },
    "get_document_upload_url": {
        "path": "/documents/upload-url",
        "method": "get",
    },
    "get_form_schema": {
        "path": "/schemas/{schemaId}",
        "method": "get",
    },
    "get_metrics": {
        "path": "/metrics",
        "method": "get",
    },
    "list_document_forms": {
        "path": "/documents/{documentId}/forms",
        "method": "get",
    },
    "list_documents": {
        "path": "/documents",
        "method": "get",
    },
    "list_form_review_workflow_tags": {
        "path": "/tags",
        "method": "get",
    },
    "list_form_schemas": {
        "path": "/schemas",
        "method": "get",
    },
    "list_forms": {
        "path": "/forms",
        "method": "get",
    },
    "submit_source_document": {
        "path": "/sources/document",
        "method": "post",
    },
    "update_form_review": {
        "path": "/documents/{documentId}/forms/{formId}/review",
        "method": "put",
    },
    "update_form_schema": {
        "path": "/schemas/{schemaId}",
        "method": "put",
    },
    "update_status": {
        "path": "/documents/{documentId}/forms/{formId}/status",
        "method": "put",
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
ResponseBody = TypeVar('ResponseBody')
StatusCode = TypeVar('StatusCode')

@dataclass
class ApiRequest(Generic[RequestParameters, RequestArrayParameters, RequestBody]):
    request_parameters: RequestParameters
    request_array_parameters: RequestArrayParameters
    body: RequestBody
    event: Any
    context: Any
    interceptor_context: Dict[str, Any]

@dataclass
class ChainedApiRequest(ApiRequest[RequestParameters, RequestArrayParameters, RequestBody],
    Generic[RequestParameters, RequestArrayParameters, RequestBody]):

    chain: 'HandlerChain'

@dataclass
class ApiResponse(Generic[StatusCode, ResponseBody]):
    status_code: StatusCode
    headers: Dict[str, str]
    body: ResponseBody

class HandlerChain(Generic[RequestParameters, RequestArrayParameters, RequestBody, StatusCode, ResponseBody]):
    def next(self, request: ChainedApiRequest[RequestParameters, RequestArrayParameters, RequestBody]) -> ApiResponse[StatusCode, ResponseBody]:
        raise Exception("Not implemented!")

def _build_handler_chain(_interceptors, handler) -> HandlerChain:
    if len(_interceptors) == 0:
        class BaseHandlerChain(HandlerChain[RequestParameters, RequestArrayParameters, RequestBody, StatusCode, ResponseBody]):
            def next(self, request: ApiRequest[RequestParameters, RequestArrayParameters, RequestBody]) -> ApiResponse[StatusCode, ResponseBody]:
                return handler(request)
        return BaseHandlerChain()
    else:
        interceptor = _interceptors.pop(0)

        class RemainingHandlerChain(HandlerChain[RequestParameters, RequestArrayParameters, RequestBody, StatusCode, ResponseBody]):
            def next(self, request: ChainedApiRequest[RequestParameters, RequestArrayParameters, RequestBody]) -> ApiResponse[StatusCode, ResponseBody]:
                return interceptor(ChainedApiRequest(
                    request_parameters = request.request_parameters,
                    request_array_parameters = request.request_array_parameters,
                    body = request.body,
                    event = request.event,
                    context = request.context,
                    interceptor_context = request.interceptor_context,
                    chain = _build_handler_chain(_interceptors, handler),
                ))
        return RemainingHandlerChain()


# Request parameters are single value query params or path params
class CreateFormReviewWorkflowTagRequestParameters(TypedDict):
    ...

# Request array parameters are multi-value query params
class CreateFormReviewWorkflowTagRequestArrayParameters(TypedDict):
    ...

# Request body type (default to Any when no body parameters exist)
CreateFormReviewWorkflowTagRequestBody = CreateFormReviewWorkflowTagInput

CreateFormReviewWorkflowTag200OperationResponse = ApiResponse[Literal[200], FormReviewWorkflowTag]
CreateFormReviewWorkflowTagOperationResponses = Union[CreateFormReviewWorkflowTag200OperationResponse, ]

# Request type for create_form_review_workflow_tag
CreateFormReviewWorkflowTagRequest = ApiRequest[CreateFormReviewWorkflowTagRequestParameters, CreateFormReviewWorkflowTagRequestArrayParameters, CreateFormReviewWorkflowTagRequestBody]
CreateFormReviewWorkflowTagChainedRequest = ChainedApiRequest[CreateFormReviewWorkflowTagRequestParameters, CreateFormReviewWorkflowTagRequestArrayParameters, CreateFormReviewWorkflowTagRequestBody]

class CreateFormReviewWorkflowTagHandlerFunction(Protocol):
    def __call__(self, input: CreateFormReviewWorkflowTagRequest, **kwargs) -> CreateFormReviewWorkflowTagOperationResponses:
        ...

CreateFormReviewWorkflowTagInterceptor = Callable[[CreateFormReviewWorkflowTagChainedRequest], CreateFormReviewWorkflowTagOperationResponses]

def create_form_review_workflow_tag_handler(_handler: CreateFormReviewWorkflowTagHandlerFunction = None, interceptors: List[CreateFormReviewWorkflowTagInterceptor] = []):
    """
    Decorator for an api handler for the create_form_review_workflow_tag operation, providing a typed interface for inputs and outputs
    """
    def _handler_wrapper(handler: CreateFormReviewWorkflowTagHandlerFunction):
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

            interceptor_context = {}

            chain = _build_handler_chain(interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)
            return {
                'statusCode': response.status_code,
                'headers': response.headers,
                'body': json.dumps(JSONEncoder().default(response.body)) if response.body is not None else '',
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by create_form_review_workflow_tag_handler.")

# Request parameters are single value query params or path params
class CreateFormSchemaRequestParameters(TypedDict):
    ...

# Request array parameters are multi-value query params
class CreateFormSchemaRequestArrayParameters(TypedDict):
    ...

# Request body type (default to Any when no body parameters exist)
CreateFormSchemaRequestBody = FormSchemaInput

CreateFormSchema200OperationResponse = ApiResponse[Literal[200], FormSchema]
CreateFormSchemaOperationResponses = Union[CreateFormSchema200OperationResponse, ]

# Request type for create_form_schema
CreateFormSchemaRequest = ApiRequest[CreateFormSchemaRequestParameters, CreateFormSchemaRequestArrayParameters, CreateFormSchemaRequestBody]
CreateFormSchemaChainedRequest = ChainedApiRequest[CreateFormSchemaRequestParameters, CreateFormSchemaRequestArrayParameters, CreateFormSchemaRequestBody]

class CreateFormSchemaHandlerFunction(Protocol):
    def __call__(self, input: CreateFormSchemaRequest, **kwargs) -> CreateFormSchemaOperationResponses:
        ...

CreateFormSchemaInterceptor = Callable[[CreateFormSchemaChainedRequest], CreateFormSchemaOperationResponses]

def create_form_schema_handler(_handler: CreateFormSchemaHandlerFunction = None, interceptors: List[CreateFormSchemaInterceptor] = []):
    """
    Decorator for an api handler for the create_form_schema operation, providing a typed interface for inputs and outputs
    """
    def _handler_wrapper(handler: CreateFormSchemaHandlerFunction):
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

            interceptor_context = {}

            chain = _build_handler_chain(interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)
            return {
                'statusCode': response.status_code,
                'headers': response.headers,
                'body': json.dumps(JSONEncoder().default(response.body)) if response.body is not None else '',
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by create_form_schema_handler.")

# Request parameters are single value query params or path params
class DeleteFormSchemaRequestParameters(TypedDict):
    schemaId: str
    ...

# Request array parameters are multi-value query params
class DeleteFormSchemaRequestArrayParameters(TypedDict):
    ...

# Request body type (default to Any when no body parameters exist)
DeleteFormSchemaRequestBody = Any

DeleteFormSchema200OperationResponse = ApiResponse[Literal[200], FormSchema]
DeleteFormSchemaOperationResponses = Union[DeleteFormSchema200OperationResponse, ]

# Request type for delete_form_schema
DeleteFormSchemaRequest = ApiRequest[DeleteFormSchemaRequestParameters, DeleteFormSchemaRequestArrayParameters, DeleteFormSchemaRequestBody]
DeleteFormSchemaChainedRequest = ChainedApiRequest[DeleteFormSchemaRequestParameters, DeleteFormSchemaRequestArrayParameters, DeleteFormSchemaRequestBody]

class DeleteFormSchemaHandlerFunction(Protocol):
    def __call__(self, input: DeleteFormSchemaRequest, **kwargs) -> DeleteFormSchemaOperationResponses:
        ...

DeleteFormSchemaInterceptor = Callable[[DeleteFormSchemaChainedRequest], DeleteFormSchemaOperationResponses]

def delete_form_schema_handler(_handler: DeleteFormSchemaHandlerFunction = None, interceptors: List[DeleteFormSchemaInterceptor] = []):
    """
    Decorator for an api handler for the delete_form_schema operation, providing a typed interface for inputs and outputs
    """
    def _handler_wrapper(handler: DeleteFormSchemaHandlerFunction):
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

            interceptor_context = {}

            chain = _build_handler_chain(interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)
            return {
                'statusCode': response.status_code,
                'headers': response.headers,
                'body': json.dumps(JSONEncoder().default(response.body)) if response.body is not None else '',
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by delete_form_schema_handler.")

# Request parameters are single value query params or path params
class GetDocumentRequestParameters(TypedDict):
    documentId: str
    ...

# Request array parameters are multi-value query params
class GetDocumentRequestArrayParameters(TypedDict):
    ...

# Request body type (default to Any when no body parameters exist)
GetDocumentRequestBody = Any

GetDocument200OperationResponse = ApiResponse[Literal[200], DocumentMetadata]
GetDocument404OperationResponse = ApiResponse[Literal[404], ApiError]
GetDocumentOperationResponses = Union[GetDocument200OperationResponse, GetDocument404OperationResponse, ]

# Request type for get_document
GetDocumentRequest = ApiRequest[GetDocumentRequestParameters, GetDocumentRequestArrayParameters, GetDocumentRequestBody]
GetDocumentChainedRequest = ChainedApiRequest[GetDocumentRequestParameters, GetDocumentRequestArrayParameters, GetDocumentRequestBody]

class GetDocumentHandlerFunction(Protocol):
    def __call__(self, input: GetDocumentRequest, **kwargs) -> GetDocumentOperationResponses:
        ...

GetDocumentInterceptor = Callable[[GetDocumentChainedRequest], GetDocumentOperationResponses]

def get_document_handler(_handler: GetDocumentHandlerFunction = None, interceptors: List[GetDocumentInterceptor] = []):
    """
    Decorator for an api handler for the get_document operation, providing a typed interface for inputs and outputs
    """
    def _handler_wrapper(handler: GetDocumentHandlerFunction):
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

            interceptor_context = {}

            chain = _build_handler_chain(interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)
            return {
                'statusCode': response.status_code,
                'headers': response.headers,
                'body': json.dumps(JSONEncoder().default(response.body)) if response.body is not None else '',
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by get_document_handler.")

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

GetDocumentForm200OperationResponse = ApiResponse[Literal[200], FormMetadata]
GetDocumentForm404OperationResponse = ApiResponse[Literal[404], ApiError]
GetDocumentFormOperationResponses = Union[GetDocumentForm200OperationResponse, GetDocumentForm404OperationResponse, ]

# Request type for get_document_form
GetDocumentFormRequest = ApiRequest[GetDocumentFormRequestParameters, GetDocumentFormRequestArrayParameters, GetDocumentFormRequestBody]
GetDocumentFormChainedRequest = ChainedApiRequest[GetDocumentFormRequestParameters, GetDocumentFormRequestArrayParameters, GetDocumentFormRequestBody]

class GetDocumentFormHandlerFunction(Protocol):
    def __call__(self, input: GetDocumentFormRequest, **kwargs) -> GetDocumentFormOperationResponses:
        ...

GetDocumentFormInterceptor = Callable[[GetDocumentFormChainedRequest], GetDocumentFormOperationResponses]

def get_document_form_handler(_handler: GetDocumentFormHandlerFunction = None, interceptors: List[GetDocumentFormInterceptor] = []):
    """
    Decorator for an api handler for the get_document_form operation, providing a typed interface for inputs and outputs
    """
    def _handler_wrapper(handler: GetDocumentFormHandlerFunction):
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

            interceptor_context = {}

            chain = _build_handler_chain(interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)
            return {
                'statusCode': response.status_code,
                'headers': response.headers,
                'body': json.dumps(JSONEncoder().default(response.body)) if response.body is not None else '',
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by get_document_form_handler.")

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

GetDocumentUploadUrl200OperationResponse = ApiResponse[Literal[200], GetDocumentUploadUrlResponse]
GetDocumentUploadUrlOperationResponses = Union[GetDocumentUploadUrl200OperationResponse, ]

# Request type for get_document_upload_url
GetDocumentUploadUrlRequest = ApiRequest[GetDocumentUploadUrlRequestParameters, GetDocumentUploadUrlRequestArrayParameters, GetDocumentUploadUrlRequestBody]
GetDocumentUploadUrlChainedRequest = ChainedApiRequest[GetDocumentUploadUrlRequestParameters, GetDocumentUploadUrlRequestArrayParameters, GetDocumentUploadUrlRequestBody]

class GetDocumentUploadUrlHandlerFunction(Protocol):
    def __call__(self, input: GetDocumentUploadUrlRequest, **kwargs) -> GetDocumentUploadUrlOperationResponses:
        ...

GetDocumentUploadUrlInterceptor = Callable[[GetDocumentUploadUrlChainedRequest], GetDocumentUploadUrlOperationResponses]

def get_document_upload_url_handler(_handler: GetDocumentUploadUrlHandlerFunction = None, interceptors: List[GetDocumentUploadUrlInterceptor] = []):
    """
    Decorator for an api handler for the get_document_upload_url operation, providing a typed interface for inputs and outputs
    """
    def _handler_wrapper(handler: GetDocumentUploadUrlHandlerFunction):
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

            interceptor_context = {}

            chain = _build_handler_chain(interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)
            return {
                'statusCode': response.status_code,
                'headers': response.headers,
                'body': json.dumps(JSONEncoder().default(response.body)) if response.body is not None else '',
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by get_document_upload_url_handler.")

# Request parameters are single value query params or path params
class GetFormSchemaRequestParameters(TypedDict):
    schemaId: str
    ...

# Request array parameters are multi-value query params
class GetFormSchemaRequestArrayParameters(TypedDict):
    ...

# Request body type (default to Any when no body parameters exist)
GetFormSchemaRequestBody = Any

GetFormSchema200OperationResponse = ApiResponse[Literal[200], FormSchema]
GetFormSchemaOperationResponses = Union[GetFormSchema200OperationResponse, ]

# Request type for get_form_schema
GetFormSchemaRequest = ApiRequest[GetFormSchemaRequestParameters, GetFormSchemaRequestArrayParameters, GetFormSchemaRequestBody]
GetFormSchemaChainedRequest = ChainedApiRequest[GetFormSchemaRequestParameters, GetFormSchemaRequestArrayParameters, GetFormSchemaRequestBody]

class GetFormSchemaHandlerFunction(Protocol):
    def __call__(self, input: GetFormSchemaRequest, **kwargs) -> GetFormSchemaOperationResponses:
        ...

GetFormSchemaInterceptor = Callable[[GetFormSchemaChainedRequest], GetFormSchemaOperationResponses]

def get_form_schema_handler(_handler: GetFormSchemaHandlerFunction = None, interceptors: List[GetFormSchemaInterceptor] = []):
    """
    Decorator for an api handler for the get_form_schema operation, providing a typed interface for inputs and outputs
    """
    def _handler_wrapper(handler: GetFormSchemaHandlerFunction):
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

            interceptor_context = {}

            chain = _build_handler_chain(interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)
            return {
                'statusCode': response.status_code,
                'headers': response.headers,
                'body': json.dumps(JSONEncoder().default(response.body)) if response.body is not None else '',
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by get_form_schema_handler.")

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

GetMetrics200OperationResponse = ApiResponse[Literal[200], AggregateMetrics]
GetMetricsOperationResponses = Union[GetMetrics200OperationResponse, ]

# Request type for get_metrics
GetMetricsRequest = ApiRequest[GetMetricsRequestParameters, GetMetricsRequestArrayParameters, GetMetricsRequestBody]
GetMetricsChainedRequest = ChainedApiRequest[GetMetricsRequestParameters, GetMetricsRequestArrayParameters, GetMetricsRequestBody]

class GetMetricsHandlerFunction(Protocol):
    def __call__(self, input: GetMetricsRequest, **kwargs) -> GetMetricsOperationResponses:
        ...

GetMetricsInterceptor = Callable[[GetMetricsChainedRequest], GetMetricsOperationResponses]

def get_metrics_handler(_handler: GetMetricsHandlerFunction = None, interceptors: List[GetMetricsInterceptor] = []):
    """
    Decorator for an api handler for the get_metrics operation, providing a typed interface for inputs and outputs
    """
    def _handler_wrapper(handler: GetMetricsHandlerFunction):
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

            interceptor_context = {}

            chain = _build_handler_chain(interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)
            return {
                'statusCode': response.status_code,
                'headers': response.headers,
                'body': json.dumps(JSONEncoder().default(response.body)) if response.body is not None else '',
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by get_metrics_handler.")

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

ListDocumentForms200OperationResponse = ApiResponse[Literal[200], ListFormsResponse]
ListDocumentForms404OperationResponse = ApiResponse[Literal[404], ApiError]
ListDocumentFormsOperationResponses = Union[ListDocumentForms200OperationResponse, ListDocumentForms404OperationResponse, ]

# Request type for list_document_forms
ListDocumentFormsRequest = ApiRequest[ListDocumentFormsRequestParameters, ListDocumentFormsRequestArrayParameters, ListDocumentFormsRequestBody]
ListDocumentFormsChainedRequest = ChainedApiRequest[ListDocumentFormsRequestParameters, ListDocumentFormsRequestArrayParameters, ListDocumentFormsRequestBody]

class ListDocumentFormsHandlerFunction(Protocol):
    def __call__(self, input: ListDocumentFormsRequest, **kwargs) -> ListDocumentFormsOperationResponses:
        ...

ListDocumentFormsInterceptor = Callable[[ListDocumentFormsChainedRequest], ListDocumentFormsOperationResponses]

def list_document_forms_handler(_handler: ListDocumentFormsHandlerFunction = None, interceptors: List[ListDocumentFormsInterceptor] = []):
    """
    Decorator for an api handler for the list_document_forms operation, providing a typed interface for inputs and outputs
    """
    def _handler_wrapper(handler: ListDocumentFormsHandlerFunction):
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

            interceptor_context = {}

            chain = _build_handler_chain(interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)
            return {
                'statusCode': response.status_code,
                'headers': response.headers,
                'body': json.dumps(JSONEncoder().default(response.body)) if response.body is not None else '',
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by list_document_forms_handler.")

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

ListDocuments200OperationResponse = ApiResponse[Literal[200], ListDocumentsResponse]
ListDocumentsOperationResponses = Union[ListDocuments200OperationResponse, ]

# Request type for list_documents
ListDocumentsRequest = ApiRequest[ListDocumentsRequestParameters, ListDocumentsRequestArrayParameters, ListDocumentsRequestBody]
ListDocumentsChainedRequest = ChainedApiRequest[ListDocumentsRequestParameters, ListDocumentsRequestArrayParameters, ListDocumentsRequestBody]

class ListDocumentsHandlerFunction(Protocol):
    def __call__(self, input: ListDocumentsRequest, **kwargs) -> ListDocumentsOperationResponses:
        ...

ListDocumentsInterceptor = Callable[[ListDocumentsChainedRequest], ListDocumentsOperationResponses]

def list_documents_handler(_handler: ListDocumentsHandlerFunction = None, interceptors: List[ListDocumentsInterceptor] = []):
    """
    Decorator for an api handler for the list_documents operation, providing a typed interface for inputs and outputs
    """
    def _handler_wrapper(handler: ListDocumentsHandlerFunction):
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

            interceptor_context = {}

            chain = _build_handler_chain(interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)
            return {
                'statusCode': response.status_code,
                'headers': response.headers,
                'body': json.dumps(JSONEncoder().default(response.body)) if response.body is not None else '',
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by list_documents_handler.")

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

ListFormReviewWorkflowTags200OperationResponse = ApiResponse[Literal[200], ListFormReviewWorkflowTagsResponse]
ListFormReviewWorkflowTagsOperationResponses = Union[ListFormReviewWorkflowTags200OperationResponse, ]

# Request type for list_form_review_workflow_tags
ListFormReviewWorkflowTagsRequest = ApiRequest[ListFormReviewWorkflowTagsRequestParameters, ListFormReviewWorkflowTagsRequestArrayParameters, ListFormReviewWorkflowTagsRequestBody]
ListFormReviewWorkflowTagsChainedRequest = ChainedApiRequest[ListFormReviewWorkflowTagsRequestParameters, ListFormReviewWorkflowTagsRequestArrayParameters, ListFormReviewWorkflowTagsRequestBody]

class ListFormReviewWorkflowTagsHandlerFunction(Protocol):
    def __call__(self, input: ListFormReviewWorkflowTagsRequest, **kwargs) -> ListFormReviewWorkflowTagsOperationResponses:
        ...

ListFormReviewWorkflowTagsInterceptor = Callable[[ListFormReviewWorkflowTagsChainedRequest], ListFormReviewWorkflowTagsOperationResponses]

def list_form_review_workflow_tags_handler(_handler: ListFormReviewWorkflowTagsHandlerFunction = None, interceptors: List[ListFormReviewWorkflowTagsInterceptor] = []):
    """
    Decorator for an api handler for the list_form_review_workflow_tags operation, providing a typed interface for inputs and outputs
    """
    def _handler_wrapper(handler: ListFormReviewWorkflowTagsHandlerFunction):
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

            interceptor_context = {}

            chain = _build_handler_chain(interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)
            return {
                'statusCode': response.status_code,
                'headers': response.headers,
                'body': json.dumps(JSONEncoder().default(response.body)) if response.body is not None else '',
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by list_form_review_workflow_tags_handler.")

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

ListFormSchemas200OperationResponse = ApiResponse[Literal[200], ListFormSchemasResponse]
ListFormSchemasOperationResponses = Union[ListFormSchemas200OperationResponse, ]

# Request type for list_form_schemas
ListFormSchemasRequest = ApiRequest[ListFormSchemasRequestParameters, ListFormSchemasRequestArrayParameters, ListFormSchemasRequestBody]
ListFormSchemasChainedRequest = ChainedApiRequest[ListFormSchemasRequestParameters, ListFormSchemasRequestArrayParameters, ListFormSchemasRequestBody]

class ListFormSchemasHandlerFunction(Protocol):
    def __call__(self, input: ListFormSchemasRequest, **kwargs) -> ListFormSchemasOperationResponses:
        ...

ListFormSchemasInterceptor = Callable[[ListFormSchemasChainedRequest], ListFormSchemasOperationResponses]

def list_form_schemas_handler(_handler: ListFormSchemasHandlerFunction = None, interceptors: List[ListFormSchemasInterceptor] = []):
    """
    Decorator for an api handler for the list_form_schemas operation, providing a typed interface for inputs and outputs
    """
    def _handler_wrapper(handler: ListFormSchemasHandlerFunction):
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

            interceptor_context = {}

            chain = _build_handler_chain(interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)
            return {
                'statusCode': response.status_code,
                'headers': response.headers,
                'body': json.dumps(JSONEncoder().default(response.body)) if response.body is not None else '',
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by list_form_schemas_handler.")

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

ListForms200OperationResponse = ApiResponse[Literal[200], ListFormsResponse]
ListFormsOperationResponses = Union[ListForms200OperationResponse, ]

# Request type for list_forms
ListFormsRequest = ApiRequest[ListFormsRequestParameters, ListFormsRequestArrayParameters, ListFormsRequestBody]
ListFormsChainedRequest = ChainedApiRequest[ListFormsRequestParameters, ListFormsRequestArrayParameters, ListFormsRequestBody]

class ListFormsHandlerFunction(Protocol):
    def __call__(self, input: ListFormsRequest, **kwargs) -> ListFormsOperationResponses:
        ...

ListFormsInterceptor = Callable[[ListFormsChainedRequest], ListFormsOperationResponses]

def list_forms_handler(_handler: ListFormsHandlerFunction = None, interceptors: List[ListFormsInterceptor] = []):
    """
    Decorator for an api handler for the list_forms operation, providing a typed interface for inputs and outputs
    """
    def _handler_wrapper(handler: ListFormsHandlerFunction):
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

            interceptor_context = {}

            chain = _build_handler_chain(interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)
            return {
                'statusCode': response.status_code,
                'headers': response.headers,
                'body': json.dumps(JSONEncoder().default(response.body)) if response.body is not None else '',
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by list_forms_handler.")

# Request parameters are single value query params or path params
class SubmitSourceDocumentRequestParameters(TypedDict):
    ...

# Request array parameters are multi-value query params
class SubmitSourceDocumentRequestArrayParameters(TypedDict):
    ...

# Request body type (default to Any when no body parameters exist)
SubmitSourceDocumentRequestBody = SubmitSourceDocumentInput

SubmitSourceDocument200OperationResponse = ApiResponse[Literal[200], DocumentMetadata]
SubmitSourceDocumentOperationResponses = Union[SubmitSourceDocument200OperationResponse, ]

# Request type for submit_source_document
SubmitSourceDocumentRequest = ApiRequest[SubmitSourceDocumentRequestParameters, SubmitSourceDocumentRequestArrayParameters, SubmitSourceDocumentRequestBody]
SubmitSourceDocumentChainedRequest = ChainedApiRequest[SubmitSourceDocumentRequestParameters, SubmitSourceDocumentRequestArrayParameters, SubmitSourceDocumentRequestBody]

class SubmitSourceDocumentHandlerFunction(Protocol):
    def __call__(self, input: SubmitSourceDocumentRequest, **kwargs) -> SubmitSourceDocumentOperationResponses:
        ...

SubmitSourceDocumentInterceptor = Callable[[SubmitSourceDocumentChainedRequest], SubmitSourceDocumentOperationResponses]

def submit_source_document_handler(_handler: SubmitSourceDocumentHandlerFunction = None, interceptors: List[SubmitSourceDocumentInterceptor] = []):
    """
    Decorator for an api handler for the submit_source_document operation, providing a typed interface for inputs and outputs
    """
    def _handler_wrapper(handler: SubmitSourceDocumentHandlerFunction):
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

            interceptor_context = {}

            chain = _build_handler_chain(interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)
            return {
                'statusCode': response.status_code,
                'headers': response.headers,
                'body': json.dumps(JSONEncoder().default(response.body)) if response.body is not None else '',
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by submit_source_document_handler.")

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

UpdateFormReview200OperationResponse = ApiResponse[Literal[200], FormMetadata]
UpdateFormReview404OperationResponse = ApiResponse[Literal[404], ApiError]
UpdateFormReviewOperationResponses = Union[UpdateFormReview200OperationResponse, UpdateFormReview404OperationResponse, ]

# Request type for update_form_review
UpdateFormReviewRequest = ApiRequest[UpdateFormReviewRequestParameters, UpdateFormReviewRequestArrayParameters, UpdateFormReviewRequestBody]
UpdateFormReviewChainedRequest = ChainedApiRequest[UpdateFormReviewRequestParameters, UpdateFormReviewRequestArrayParameters, UpdateFormReviewRequestBody]

class UpdateFormReviewHandlerFunction(Protocol):
    def __call__(self, input: UpdateFormReviewRequest, **kwargs) -> UpdateFormReviewOperationResponses:
        ...

UpdateFormReviewInterceptor = Callable[[UpdateFormReviewChainedRequest], UpdateFormReviewOperationResponses]

def update_form_review_handler(_handler: UpdateFormReviewHandlerFunction = None, interceptors: List[UpdateFormReviewInterceptor] = []):
    """
    Decorator for an api handler for the update_form_review operation, providing a typed interface for inputs and outputs
    """
    def _handler_wrapper(handler: UpdateFormReviewHandlerFunction):
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

            interceptor_context = {}

            chain = _build_handler_chain(interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)
            return {
                'statusCode': response.status_code,
                'headers': response.headers,
                'body': json.dumps(JSONEncoder().default(response.body)) if response.body is not None else '',
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by update_form_review_handler.")

# Request parameters are single value query params or path params
class UpdateFormSchemaRequestParameters(TypedDict):
    schemaId: str
    ...

# Request array parameters are multi-value query params
class UpdateFormSchemaRequestArrayParameters(TypedDict):
    ...

# Request body type (default to Any when no body parameters exist)
UpdateFormSchemaRequestBody = FormSchema

UpdateFormSchema200OperationResponse = ApiResponse[Literal[200], FormSchema]
UpdateFormSchemaOperationResponses = Union[UpdateFormSchema200OperationResponse, ]

# Request type for update_form_schema
UpdateFormSchemaRequest = ApiRequest[UpdateFormSchemaRequestParameters, UpdateFormSchemaRequestArrayParameters, UpdateFormSchemaRequestBody]
UpdateFormSchemaChainedRequest = ChainedApiRequest[UpdateFormSchemaRequestParameters, UpdateFormSchemaRequestArrayParameters, UpdateFormSchemaRequestBody]

class UpdateFormSchemaHandlerFunction(Protocol):
    def __call__(self, input: UpdateFormSchemaRequest, **kwargs) -> UpdateFormSchemaOperationResponses:
        ...

UpdateFormSchemaInterceptor = Callable[[UpdateFormSchemaChainedRequest], UpdateFormSchemaOperationResponses]

def update_form_schema_handler(_handler: UpdateFormSchemaHandlerFunction = None, interceptors: List[UpdateFormSchemaInterceptor] = []):
    """
    Decorator for an api handler for the update_form_schema operation, providing a typed interface for inputs and outputs
    """
    def _handler_wrapper(handler: UpdateFormSchemaHandlerFunction):
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

            interceptor_context = {}

            chain = _build_handler_chain(interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)
            return {
                'statusCode': response.status_code,
                'headers': response.headers,
                'body': json.dumps(JSONEncoder().default(response.body)) if response.body is not None else '',
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by update_form_schema_handler.")

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

UpdateStatus200OperationResponse = ApiResponse[Literal[200], FormMetadata]
UpdateStatusOperationResponses = Union[UpdateStatus200OperationResponse, ]

# Request type for update_status
UpdateStatusRequest = ApiRequest[UpdateStatusRequestParameters, UpdateStatusRequestArrayParameters, UpdateStatusRequestBody]
UpdateStatusChainedRequest = ChainedApiRequest[UpdateStatusRequestParameters, UpdateStatusRequestArrayParameters, UpdateStatusRequestBody]

class UpdateStatusHandlerFunction(Protocol):
    def __call__(self, input: UpdateStatusRequest, **kwargs) -> UpdateStatusOperationResponses:
        ...

UpdateStatusInterceptor = Callable[[UpdateStatusChainedRequest], UpdateStatusOperationResponses]

def update_status_handler(_handler: UpdateStatusHandlerFunction = None, interceptors: List[UpdateStatusInterceptor] = []):
    """
    Decorator for an api handler for the update_status operation, providing a typed interface for inputs and outputs
    """
    def _handler_wrapper(handler: UpdateStatusHandlerFunction):
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

            interceptor_context = {}

            chain = _build_handler_chain(interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)
            return {
                'statusCode': response.status_code,
                'headers': response.headers,
                'body': json.dumps(JSONEncoder().default(response.body)) if response.body is not None else '',
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by update_status_handler.")
