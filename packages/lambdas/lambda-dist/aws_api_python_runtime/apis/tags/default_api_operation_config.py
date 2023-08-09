import urllib.parse
import json
from typing import Callable, Any, Dict, List, NamedTuple, TypeVar, Generic, Union, TypedDict, Protocol, Optional, Literal
from functools import wraps
from dataclasses import dataclass, fields

from aws_api_python_runtime.model.aggregate_metrics import AggregateMetrics
from aws_api_python_runtime.model.api_error import ApiError
from aws_api_python_runtime.model.create_form_review_workflow_tag_input import CreateFormReviewWorkflowTagInput
from aws_api_python_runtime.model.document_metadata import DocumentMetadata
from aws_api_python_runtime.model.form_metadata import FormMetadata
from aws_api_python_runtime.model.form_review_workflow_tag import FormReviewWorkflowTag
from aws_api_python_runtime.model.form_schema import FormSchema
from aws_api_python_runtime.model.form_schema_input import FormSchemaInput
from aws_api_python_runtime.model.get_document_upload_url_response import GetDocumentUploadUrlResponse
from aws_api_python_runtime.model.list_documents_response import ListDocumentsResponse
from aws_api_python_runtime.model.list_form_review_workflow_tags_response import ListFormReviewWorkflowTagsResponse
from aws_api_python_runtime.model.list_form_schemas_response import ListFormSchemasResponse
from aws_api_python_runtime.model.list_forms_response import ListFormsResponse
from aws_api_python_runtime.model.submit_source_document_input import SubmitSourceDocumentInput
from aws_api_python_runtime.model.update_form_input import UpdateFormInput
from aws_api_python_runtime.model.update_status_input import UpdateStatusInput

from aws_api_python_runtime.schemas import (
    date,
    datetime,
    file_type,
    none_type,
)
from aws_api_python_runtime.api_client import JSONEncoder

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
        "contentTypes": ["application/json",]
    },
    "create_form_schema": {
        "path": "/schemas",
        "method": "post",
        "contentTypes": ["application/json",]
    },
    "delete_form_schema": {
        "path": "/schemas/{schemaId}",
        "method": "delete",
        "contentTypes": ["application/json"]
    },
    "get_document": {
        "path": "/documents/{documentId}",
        "method": "get",
        "contentTypes": ["application/json"]
    },
    "get_document_form": {
        "path": "/documents/{documentId}/forms/{formId}",
        "method": "get",
        "contentTypes": ["application/json"]
    },
    "get_document_upload_url": {
        "path": "/documents/upload-url",
        "method": "get",
        "contentTypes": ["application/json"]
    },
    "get_form_schema": {
        "path": "/schemas/{schemaId}",
        "method": "get",
        "contentTypes": ["application/json"]
    },
    "get_metrics": {
        "path": "/metrics",
        "method": "get",
        "contentTypes": ["application/json"]
    },
    "list_document_forms": {
        "path": "/documents/{documentId}/forms",
        "method": "get",
        "contentTypes": ["application/json"]
    },
    "list_documents": {
        "path": "/documents",
        "method": "get",
        "contentTypes": ["application/json"]
    },
    "list_form_review_workflow_tags": {
        "path": "/tags",
        "method": "get",
        "contentTypes": ["application/json"]
    },
    "list_form_schemas": {
        "path": "/schemas",
        "method": "get",
        "contentTypes": ["application/json"]
    },
    "list_forms": {
        "path": "/forms",
        "method": "get",
        "contentTypes": ["application/json"]
    },
    "submit_source_document": {
        "path": "/sources/document",
        "method": "post",
        "contentTypes": ["application/json",]
    },
    "update_form_review": {
        "path": "/documents/{documentId}/forms/{formId}/review",
        "method": "put",
        "contentTypes": ["application/json",]
    },
    "update_form_schema": {
        "path": "/schemas/{schemaId}",
        "method": "put",
        "contentTypes": ["application/json",]
    },
    "update_status": {
        "path": "/documents/{documentId}/forms/{formId}/status",
        "method": "put",
        "contentTypes": ["application/json",]
    },
}

class Operations:
    @staticmethod
    def all(value: T) -> OperationConfig[T]:
        """
        Returns an OperationConfig with the same value for every operation
        """
        return OperationConfig(**{ operation_id: value for operation_id, _ in OperationLookup.items() })

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
        interceptor = _interceptors[0]

        class RemainingHandlerChain(HandlerChain[RequestParameters, RequestArrayParameters, RequestBody, StatusCode, ResponseBody]):
            def next(self, request: ChainedApiRequest[RequestParameters, RequestArrayParameters, RequestBody]) -> ApiResponse[StatusCode, ResponseBody]:
                return interceptor(ChainedApiRequest(
                    request_parameters = request.request_parameters,
                    request_array_parameters = request.request_array_parameters,
                    body = request.body,
                    event = request.event,
                    context = request.context,
                    interceptor_context = request.interceptor_context,
                    chain = _build_handler_chain(_interceptors[1:len(_interceptors)], handler),
                ))
        return RemainingHandlerChain()


# Request parameters are single value query params, path params or header params
CreateFormReviewWorkflowTagRequestParameters = TypedDict(
    "CreateFormReviewWorkflowTagRequestParameters", {
    }
)

# Request array parameters are multi-value query params or header params
CreateFormReviewWorkflowTagRequestArrayParameters = TypedDict(
    "CreateFormReviewWorkflowTagRequestArrayParameters", {
    }
)

# Request body type (default to Any when no body parameters exist, or leave unchanged as str if it's a primitive type)
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
        def wrapper(event, context, additional_interceptors = [], **kwargs):
            request_parameters = decode_request_parameters({
                **(event.get('pathParameters', {}) or {}),
                **(event.get('queryStringParameters', {}) or {}),
                **(event.get('headers', {}) or {}),
            })
            request_array_parameters = decode_request_parameters({
                **(event.get('multiValueQueryStringParameters', {}) or {}),
                **(event.get('multiValueHeaders', {}) or {}),
            })
            # Non-primitive type so parse the body into the appropriate model
            body = parse_body(event['body'], ['application/json',], CreateFormReviewWorkflowTagRequestBody)
            interceptor_context = {}

            chain = _build_handler_chain(additional_interceptors + interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)

            response_headers = response.headers or {}
            response_body = ''
            if response.body is None:
                pass
            elif response.status_code == 200:
                response_body = json.dumps(JSONEncoder().default(response.body))

            return {
                'statusCode': response.status_code,
                'headers': response_headers,
                'body': response_body,
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by create_form_review_workflow_tag_handler.")

# Request parameters are single value query params, path params or header params
CreateFormSchemaRequestParameters = TypedDict(
    "CreateFormSchemaRequestParameters", {
    }
)

# Request array parameters are multi-value query params or header params
CreateFormSchemaRequestArrayParameters = TypedDict(
    "CreateFormSchemaRequestArrayParameters", {
    }
)

# Request body type (default to Any when no body parameters exist, or leave unchanged as str if it's a primitive type)
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
        def wrapper(event, context, additional_interceptors = [], **kwargs):
            request_parameters = decode_request_parameters({
                **(event.get('pathParameters', {}) or {}),
                **(event.get('queryStringParameters', {}) or {}),
                **(event.get('headers', {}) or {}),
            })
            request_array_parameters = decode_request_parameters({
                **(event.get('multiValueQueryStringParameters', {}) or {}),
                **(event.get('multiValueHeaders', {}) or {}),
            })
            # Non-primitive type so parse the body into the appropriate model
            body = parse_body(event['body'], ['application/json',], CreateFormSchemaRequestBody)
            interceptor_context = {}

            chain = _build_handler_chain(additional_interceptors + interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)

            response_headers = response.headers or {}
            response_body = ''
            if response.body is None:
                pass
            elif response.status_code == 200:
                response_body = json.dumps(JSONEncoder().default(response.body))

            return {
                'statusCode': response.status_code,
                'headers': response_headers,
                'body': response_body,
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by create_form_schema_handler.")

# Request parameters are single value query params, path params or header params
DeleteFormSchemaRequestParameters = TypedDict(
    "DeleteFormSchemaRequestParameters", {
        "schemaId": str,
    }
)

# Request array parameters are multi-value query params or header params
DeleteFormSchemaRequestArrayParameters = TypedDict(
    "DeleteFormSchemaRequestArrayParameters", {
    }
)

# Request body type (default to Any when no body parameters exist, or leave unchanged as str if it's a primitive type)
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
        def wrapper(event, context, additional_interceptors = [], **kwargs):
            request_parameters = decode_request_parameters({
                **(event.get('pathParameters', {}) or {}),
                **(event.get('queryStringParameters', {}) or {}),
                **(event.get('headers', {}) or {}),
            })
            request_array_parameters = decode_request_parameters({
                **(event.get('multiValueQueryStringParameters', {}) or {}),
                **(event.get('multiValueHeaders', {}) or {}),
            })
            body = {}
            interceptor_context = {}

            chain = _build_handler_chain(additional_interceptors + interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)

            response_headers = response.headers or {}
            response_body = ''
            if response.body is None:
                pass
            elif response.status_code == 200:
                response_body = json.dumps(JSONEncoder().default(response.body))

            return {
                'statusCode': response.status_code,
                'headers': response_headers,
                'body': response_body,
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by delete_form_schema_handler.")

# Request parameters are single value query params, path params or header params
GetDocumentRequestParameters = TypedDict(
    "GetDocumentRequestParameters", {
        "documentId": str,
    }
)

# Request array parameters are multi-value query params or header params
GetDocumentRequestArrayParameters = TypedDict(
    "GetDocumentRequestArrayParameters", {
    }
)

# Request body type (default to Any when no body parameters exist, or leave unchanged as str if it's a primitive type)
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
        def wrapper(event, context, additional_interceptors = [], **kwargs):
            request_parameters = decode_request_parameters({
                **(event.get('pathParameters', {}) or {}),
                **(event.get('queryStringParameters', {}) or {}),
                **(event.get('headers', {}) or {}),
            })
            request_array_parameters = decode_request_parameters({
                **(event.get('multiValueQueryStringParameters', {}) or {}),
                **(event.get('multiValueHeaders', {}) or {}),
            })
            body = {}
            interceptor_context = {}

            chain = _build_handler_chain(additional_interceptors + interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)

            response_headers = response.headers or {}
            response_body = ''
            if response.body is None:
                pass
            elif response.status_code == 200:
                response_body = json.dumps(JSONEncoder().default(response.body))
            elif response.status_code == 404:
                response_body = json.dumps(JSONEncoder().default(response.body))
                if "ApiError".endswith("ResponseContent"):
                    response_headers["x-amzn-errortype"] = "ApiError"[:-len("ResponseContent")]

            return {
                'statusCode': response.status_code,
                'headers': response_headers,
                'body': response_body,
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by get_document_handler.")

# Request parameters are single value query params, path params or header params
GetDocumentFormRequestParameters = TypedDict(
    "GetDocumentFormRequestParameters", {
        "documentId": str,
        "formId": str,
    }
)

# Request array parameters are multi-value query params or header params
GetDocumentFormRequestArrayParameters = TypedDict(
    "GetDocumentFormRequestArrayParameters", {
    }
)

# Request body type (default to Any when no body parameters exist, or leave unchanged as str if it's a primitive type)
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
        def wrapper(event, context, additional_interceptors = [], **kwargs):
            request_parameters = decode_request_parameters({
                **(event.get('pathParameters', {}) or {}),
                **(event.get('queryStringParameters', {}) or {}),
                **(event.get('headers', {}) or {}),
            })
            request_array_parameters = decode_request_parameters({
                **(event.get('multiValueQueryStringParameters', {}) or {}),
                **(event.get('multiValueHeaders', {}) or {}),
            })
            body = {}
            interceptor_context = {}

            chain = _build_handler_chain(additional_interceptors + interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)

            response_headers = response.headers or {}
            response_body = ''
            if response.body is None:
                pass
            elif response.status_code == 200:
                response_body = json.dumps(JSONEncoder().default(response.body))
            elif response.status_code == 404:
                response_body = json.dumps(JSONEncoder().default(response.body))
                if "ApiError".endswith("ResponseContent"):
                    response_headers["x-amzn-errortype"] = "ApiError"[:-len("ResponseContent")]

            return {
                'statusCode': response.status_code,
                'headers': response_headers,
                'body': response_body,
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by get_document_form_handler.")

# Request parameters are single value query params, path params or header params
GetDocumentUploadUrlRequestParameters = TypedDict(
    "GetDocumentUploadUrlRequestParameters", {
        "fileName": str,
        "contentType": str,
    }
)

# Request array parameters are multi-value query params or header params
GetDocumentUploadUrlRequestArrayParameters = TypedDict(
    "GetDocumentUploadUrlRequestArrayParameters", {
    }
)

# Request body type (default to Any when no body parameters exist, or leave unchanged as str if it's a primitive type)
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
        def wrapper(event, context, additional_interceptors = [], **kwargs):
            request_parameters = decode_request_parameters({
                **(event.get('pathParameters', {}) or {}),
                **(event.get('queryStringParameters', {}) or {}),
                **(event.get('headers', {}) or {}),
            })
            request_array_parameters = decode_request_parameters({
                **(event.get('multiValueQueryStringParameters', {}) or {}),
                **(event.get('multiValueHeaders', {}) or {}),
            })
            body = {}
            interceptor_context = {}

            chain = _build_handler_chain(additional_interceptors + interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)

            response_headers = response.headers or {}
            response_body = ''
            if response.body is None:
                pass
            elif response.status_code == 200:
                response_body = json.dumps(JSONEncoder().default(response.body))

            return {
                'statusCode': response.status_code,
                'headers': response_headers,
                'body': response_body,
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by get_document_upload_url_handler.")

# Request parameters are single value query params, path params or header params
GetFormSchemaRequestParameters = TypedDict(
    "GetFormSchemaRequestParameters", {
        "schemaId": str,
    }
)

# Request array parameters are multi-value query params or header params
GetFormSchemaRequestArrayParameters = TypedDict(
    "GetFormSchemaRequestArrayParameters", {
    }
)

# Request body type (default to Any when no body parameters exist, or leave unchanged as str if it's a primitive type)
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
        def wrapper(event, context, additional_interceptors = [], **kwargs):
            request_parameters = decode_request_parameters({
                **(event.get('pathParameters', {}) or {}),
                **(event.get('queryStringParameters', {}) or {}),
                **(event.get('headers', {}) or {}),
            })
            request_array_parameters = decode_request_parameters({
                **(event.get('multiValueQueryStringParameters', {}) or {}),
                **(event.get('multiValueHeaders', {}) or {}),
            })
            body = {}
            interceptor_context = {}

            chain = _build_handler_chain(additional_interceptors + interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)

            response_headers = response.headers or {}
            response_body = ''
            if response.body is None:
                pass
            elif response.status_code == 200:
                response_body = json.dumps(JSONEncoder().default(response.body))

            return {
                'statusCode': response.status_code,
                'headers': response_headers,
                'body': response_body,
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by get_form_schema_handler.")

# Request parameters are single value query params, path params or header params
GetMetricsRequestParameters = TypedDict(
    "GetMetricsRequestParameters", {
        "startTimestamp": str,
        "endTimestamp": str,
    }
)

# Request array parameters are multi-value query params or header params
GetMetricsRequestArrayParameters = TypedDict(
    "GetMetricsRequestArrayParameters", {
    }
)

# Request body type (default to Any when no body parameters exist, or leave unchanged as str if it's a primitive type)
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
        def wrapper(event, context, additional_interceptors = [], **kwargs):
            request_parameters = decode_request_parameters({
                **(event.get('pathParameters', {}) or {}),
                **(event.get('queryStringParameters', {}) or {}),
                **(event.get('headers', {}) or {}),
            })
            request_array_parameters = decode_request_parameters({
                **(event.get('multiValueQueryStringParameters', {}) or {}),
                **(event.get('multiValueHeaders', {}) or {}),
            })
            body = {}
            interceptor_context = {}

            chain = _build_handler_chain(additional_interceptors + interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)

            response_headers = response.headers or {}
            response_body = ''
            if response.body is None:
                pass
            elif response.status_code == 200:
                response_body = json.dumps(JSONEncoder().default(response.body))

            return {
                'statusCode': response.status_code,
                'headers': response_headers,
                'body': response_body,
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by get_metrics_handler.")

# Request parameters are single value query params, path params or header params
ListDocumentFormsRequestParameters = TypedDict(
    "ListDocumentFormsRequestParameters", {
        "documentId": str,
        "pageSize": str,
        "nextToken": str,
    }
)

# Request array parameters are multi-value query params or header params
ListDocumentFormsRequestArrayParameters = TypedDict(
    "ListDocumentFormsRequestArrayParameters", {
    }
)

# Request body type (default to Any when no body parameters exist, or leave unchanged as str if it's a primitive type)
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
        def wrapper(event, context, additional_interceptors = [], **kwargs):
            request_parameters = decode_request_parameters({
                **(event.get('pathParameters', {}) or {}),
                **(event.get('queryStringParameters', {}) or {}),
                **(event.get('headers', {}) or {}),
            })
            request_array_parameters = decode_request_parameters({
                **(event.get('multiValueQueryStringParameters', {}) or {}),
                **(event.get('multiValueHeaders', {}) or {}),
            })
            body = {}
            interceptor_context = {}

            chain = _build_handler_chain(additional_interceptors + interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)

            response_headers = response.headers or {}
            response_body = ''
            if response.body is None:
                pass
            elif response.status_code == 200:
                response_body = json.dumps(JSONEncoder().default(response.body))
            elif response.status_code == 404:
                response_body = json.dumps(JSONEncoder().default(response.body))
                if "ApiError".endswith("ResponseContent"):
                    response_headers["x-amzn-errortype"] = "ApiError"[:-len("ResponseContent")]

            return {
                'statusCode': response.status_code,
                'headers': response_headers,
                'body': response_body,
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by list_document_forms_handler.")

# Request parameters are single value query params, path params or header params
ListDocumentsRequestParameters = TypedDict(
    "ListDocumentsRequestParameters", {
        "pageSize": str,
        "nextToken": str,
    }
)

# Request array parameters are multi-value query params or header params
ListDocumentsRequestArrayParameters = TypedDict(
    "ListDocumentsRequestArrayParameters", {
    }
)

# Request body type (default to Any when no body parameters exist, or leave unchanged as str if it's a primitive type)
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
        def wrapper(event, context, additional_interceptors = [], **kwargs):
            request_parameters = decode_request_parameters({
                **(event.get('pathParameters', {}) or {}),
                **(event.get('queryStringParameters', {}) or {}),
                **(event.get('headers', {}) or {}),
            })
            request_array_parameters = decode_request_parameters({
                **(event.get('multiValueQueryStringParameters', {}) or {}),
                **(event.get('multiValueHeaders', {}) or {}),
            })
            body = {}
            interceptor_context = {}

            chain = _build_handler_chain(additional_interceptors + interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)

            response_headers = response.headers or {}
            response_body = ''
            if response.body is None:
                pass
            elif response.status_code == 200:
                response_body = json.dumps(JSONEncoder().default(response.body))

            return {
                'statusCode': response.status_code,
                'headers': response_headers,
                'body': response_body,
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by list_documents_handler.")

# Request parameters are single value query params, path params or header params
ListFormReviewWorkflowTagsRequestParameters = TypedDict(
    "ListFormReviewWorkflowTagsRequestParameters", {
        "pageSize": str,
        "nextToken": str,
    }
)

# Request array parameters are multi-value query params or header params
ListFormReviewWorkflowTagsRequestArrayParameters = TypedDict(
    "ListFormReviewWorkflowTagsRequestArrayParameters", {
    }
)

# Request body type (default to Any when no body parameters exist, or leave unchanged as str if it's a primitive type)
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
        def wrapper(event, context, additional_interceptors = [], **kwargs):
            request_parameters = decode_request_parameters({
                **(event.get('pathParameters', {}) or {}),
                **(event.get('queryStringParameters', {}) or {}),
                **(event.get('headers', {}) or {}),
            })
            request_array_parameters = decode_request_parameters({
                **(event.get('multiValueQueryStringParameters', {}) or {}),
                **(event.get('multiValueHeaders', {}) or {}),
            })
            body = {}
            interceptor_context = {}

            chain = _build_handler_chain(additional_interceptors + interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)

            response_headers = response.headers or {}
            response_body = ''
            if response.body is None:
                pass
            elif response.status_code == 200:
                response_body = json.dumps(JSONEncoder().default(response.body))

            return {
                'statusCode': response.status_code,
                'headers': response_headers,
                'body': response_body,
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by list_form_review_workflow_tags_handler.")

# Request parameters are single value query params, path params or header params
ListFormSchemasRequestParameters = TypedDict(
    "ListFormSchemasRequestParameters", {
        "pageSize": str,
        "nextToken": str,
    }
)

# Request array parameters are multi-value query params or header params
ListFormSchemasRequestArrayParameters = TypedDict(
    "ListFormSchemasRequestArrayParameters", {
    }
)

# Request body type (default to Any when no body parameters exist, or leave unchanged as str if it's a primitive type)
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
        def wrapper(event, context, additional_interceptors = [], **kwargs):
            request_parameters = decode_request_parameters({
                **(event.get('pathParameters', {}) or {}),
                **(event.get('queryStringParameters', {}) or {}),
                **(event.get('headers', {}) or {}),
            })
            request_array_parameters = decode_request_parameters({
                **(event.get('multiValueQueryStringParameters', {}) or {}),
                **(event.get('multiValueHeaders', {}) or {}),
            })
            body = {}
            interceptor_context = {}

            chain = _build_handler_chain(additional_interceptors + interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)

            response_headers = response.headers or {}
            response_body = ''
            if response.body is None:
                pass
            elif response.status_code == 200:
                response_body = json.dumps(JSONEncoder().default(response.body))

            return {
                'statusCode': response.status_code,
                'headers': response_headers,
                'body': response_body,
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by list_form_schemas_handler.")

# Request parameters are single value query params, path params or header params
ListFormsRequestParameters = TypedDict(
    "ListFormsRequestParameters", {
        "pageSize": str,
        "nextToken": str,
    }
)

# Request array parameters are multi-value query params or header params
ListFormsRequestArrayParameters = TypedDict(
    "ListFormsRequestArrayParameters", {
    }
)

# Request body type (default to Any when no body parameters exist, or leave unchanged as str if it's a primitive type)
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
        def wrapper(event, context, additional_interceptors = [], **kwargs):
            request_parameters = decode_request_parameters({
                **(event.get('pathParameters', {}) or {}),
                **(event.get('queryStringParameters', {}) or {}),
                **(event.get('headers', {}) or {}),
            })
            request_array_parameters = decode_request_parameters({
                **(event.get('multiValueQueryStringParameters', {}) or {}),
                **(event.get('multiValueHeaders', {}) or {}),
            })
            body = {}
            interceptor_context = {}

            chain = _build_handler_chain(additional_interceptors + interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)

            response_headers = response.headers or {}
            response_body = ''
            if response.body is None:
                pass
            elif response.status_code == 200:
                response_body = json.dumps(JSONEncoder().default(response.body))

            return {
                'statusCode': response.status_code,
                'headers': response_headers,
                'body': response_body,
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by list_forms_handler.")

# Request parameters are single value query params, path params or header params
SubmitSourceDocumentRequestParameters = TypedDict(
    "SubmitSourceDocumentRequestParameters", {
    }
)

# Request array parameters are multi-value query params or header params
SubmitSourceDocumentRequestArrayParameters = TypedDict(
    "SubmitSourceDocumentRequestArrayParameters", {
    }
)

# Request body type (default to Any when no body parameters exist, or leave unchanged as str if it's a primitive type)
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
        def wrapper(event, context, additional_interceptors = [], **kwargs):
            request_parameters = decode_request_parameters({
                **(event.get('pathParameters', {}) or {}),
                **(event.get('queryStringParameters', {}) or {}),
                **(event.get('headers', {}) or {}),
            })
            request_array_parameters = decode_request_parameters({
                **(event.get('multiValueQueryStringParameters', {}) or {}),
                **(event.get('multiValueHeaders', {}) or {}),
            })
            # Non-primitive type so parse the body into the appropriate model
            body = parse_body(event['body'], ['application/json',], SubmitSourceDocumentRequestBody)
            interceptor_context = {}

            chain = _build_handler_chain(additional_interceptors + interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)

            response_headers = response.headers or {}
            response_body = ''
            if response.body is None:
                pass
            elif response.status_code == 200:
                response_body = json.dumps(JSONEncoder().default(response.body))

            return {
                'statusCode': response.status_code,
                'headers': response_headers,
                'body': response_body,
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by submit_source_document_handler.")

# Request parameters are single value query params, path params or header params
UpdateFormReviewRequestParameters = TypedDict(
    "UpdateFormReviewRequestParameters", {
        "documentId": str,
        "formId": str,
    }
)

# Request array parameters are multi-value query params or header params
UpdateFormReviewRequestArrayParameters = TypedDict(
    "UpdateFormReviewRequestArrayParameters", {
    }
)

# Request body type (default to Any when no body parameters exist, or leave unchanged as str if it's a primitive type)
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
        def wrapper(event, context, additional_interceptors = [], **kwargs):
            request_parameters = decode_request_parameters({
                **(event.get('pathParameters', {}) or {}),
                **(event.get('queryStringParameters', {}) or {}),
                **(event.get('headers', {}) or {}),
            })
            request_array_parameters = decode_request_parameters({
                **(event.get('multiValueQueryStringParameters', {}) or {}),
                **(event.get('multiValueHeaders', {}) or {}),
            })
            # Non-primitive type so parse the body into the appropriate model
            body = parse_body(event['body'], ['application/json',], UpdateFormReviewRequestBody)
            interceptor_context = {}

            chain = _build_handler_chain(additional_interceptors + interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)

            response_headers = response.headers or {}
            response_body = ''
            if response.body is None:
                pass
            elif response.status_code == 200:
                response_body = json.dumps(JSONEncoder().default(response.body))
            elif response.status_code == 404:
                response_body = json.dumps(JSONEncoder().default(response.body))
                if "ApiError".endswith("ResponseContent"):
                    response_headers["x-amzn-errortype"] = "ApiError"[:-len("ResponseContent")]

            return {
                'statusCode': response.status_code,
                'headers': response_headers,
                'body': response_body,
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by update_form_review_handler.")

# Request parameters are single value query params, path params or header params
UpdateFormSchemaRequestParameters = TypedDict(
    "UpdateFormSchemaRequestParameters", {
        "schemaId": str,
    }
)

# Request array parameters are multi-value query params or header params
UpdateFormSchemaRequestArrayParameters = TypedDict(
    "UpdateFormSchemaRequestArrayParameters", {
    }
)

# Request body type (default to Any when no body parameters exist, or leave unchanged as str if it's a primitive type)
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
        def wrapper(event, context, additional_interceptors = [], **kwargs):
            request_parameters = decode_request_parameters({
                **(event.get('pathParameters', {}) or {}),
                **(event.get('queryStringParameters', {}) or {}),
                **(event.get('headers', {}) or {}),
            })
            request_array_parameters = decode_request_parameters({
                **(event.get('multiValueQueryStringParameters', {}) or {}),
                **(event.get('multiValueHeaders', {}) or {}),
            })
            # Non-primitive type so parse the body into the appropriate model
            body = parse_body(event['body'], ['application/json',], UpdateFormSchemaRequestBody)
            interceptor_context = {}

            chain = _build_handler_chain(additional_interceptors + interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)

            response_headers = response.headers or {}
            response_body = ''
            if response.body is None:
                pass
            elif response.status_code == 200:
                response_body = json.dumps(JSONEncoder().default(response.body))

            return {
                'statusCode': response.status_code,
                'headers': response_headers,
                'body': response_body,
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by update_form_schema_handler.")

# Request parameters are single value query params, path params or header params
UpdateStatusRequestParameters = TypedDict(
    "UpdateStatusRequestParameters", {
        "documentId": str,
        "formId": str,
    }
)

# Request array parameters are multi-value query params or header params
UpdateStatusRequestArrayParameters = TypedDict(
    "UpdateStatusRequestArrayParameters", {
    }
)

# Request body type (default to Any when no body parameters exist, or leave unchanged as str if it's a primitive type)
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
        def wrapper(event, context, additional_interceptors = [], **kwargs):
            request_parameters = decode_request_parameters({
                **(event.get('pathParameters', {}) or {}),
                **(event.get('queryStringParameters', {}) or {}),
                **(event.get('headers', {}) or {}),
            })
            request_array_parameters = decode_request_parameters({
                **(event.get('multiValueQueryStringParameters', {}) or {}),
                **(event.get('multiValueHeaders', {}) or {}),
            })
            # Non-primitive type so parse the body into the appropriate model
            body = parse_body(event['body'], ['application/json',], UpdateStatusRequestBody)
            interceptor_context = {}

            chain = _build_handler_chain(additional_interceptors + interceptors, handler)
            response = chain.next(ApiRequest(
                request_parameters,
                request_array_parameters,
                body,
                event,
                context,
                interceptor_context,
            ), **kwargs)

            response_headers = response.headers or {}
            response_body = ''
            if response.body is None:
                pass
            elif response.status_code == 200:
                response_body = json.dumps(JSONEncoder().default(response.body))

            return {
                'statusCode': response.status_code,
                'headers': response_headers,
                'body': response_body,
            }
        return wrapper

    # Support use as a decorator with no arguments, or with interceptor arguments
    if callable(_handler):
        return _handler_wrapper(_handler)
    elif _handler is None:
        return _handler_wrapper
    else:
        raise Exception("Positional arguments are not supported by update_status_handler.")

Interceptor = Callable[[ChainedApiRequest[RequestParameters, RequestArrayParameters, RequestBody]], ApiResponse[StatusCode, ResponseBody]]

def concat_method_and_path(method: str, path: str):
    return "{}||{}".format(method.lower(), path)

OperationIdByMethodAndPath = { concat_method_and_path(method_and_path["method"], method_and_path["path"]): operation for operation, method_and_path in OperationLookup.items() }

@dataclass
class HandlerRouterHandlers:
  create_form_review_workflow_tag: Callable[[Dict, Any], Dict]
  create_form_schema: Callable[[Dict, Any], Dict]
  delete_form_schema: Callable[[Dict, Any], Dict]
  get_document: Callable[[Dict, Any], Dict]
  get_document_form: Callable[[Dict, Any], Dict]
  get_document_upload_url: Callable[[Dict, Any], Dict]
  get_form_schema: Callable[[Dict, Any], Dict]
  get_metrics: Callable[[Dict, Any], Dict]
  list_document_forms: Callable[[Dict, Any], Dict]
  list_documents: Callable[[Dict, Any], Dict]
  list_form_review_workflow_tags: Callable[[Dict, Any], Dict]
  list_form_schemas: Callable[[Dict, Any], Dict]
  list_forms: Callable[[Dict, Any], Dict]
  submit_source_document: Callable[[Dict, Any], Dict]
  update_form_review: Callable[[Dict, Any], Dict]
  update_form_schema: Callable[[Dict, Any], Dict]
  update_status: Callable[[Dict, Any], Dict]

def handler_router(handlers: HandlerRouterHandlers, interceptors: List[Interceptor] = []):
    """
    Returns a lambda handler which can be used to route requests to the appropriate typed lambda handler function.
    """
    _handlers = { field.name: getattr(handlers, field.name) for field in fields(handlers) }

    def handler_wrapper(event, context):
        operation_id = OperationIdByMethodAndPath[concat_method_and_path(event['requestContext']['httpMethod'], event['requestContext']['resourcePath'])]
        handler = _handlers[operation_id]
        return handler(event, context, additional_interceptors=interceptors)
    return handler_wrapper
