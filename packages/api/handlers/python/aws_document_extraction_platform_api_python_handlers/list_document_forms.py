from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_api_python_handlers.interceptors import DEFAULT_INTERCEPTORS
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import LoggingInterceptor
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    list_document_forms_handler, ListDocumentFormsRequest, ListDocumentFormsOperationResponses
)


def list_document_forms(input: ListDocumentFormsRequest, **kwargs) -> ListDocumentFormsOperationResponses:
    """
    Type-safe handler for the ListDocumentForms operation
    """
    LoggingInterceptor.get_logger(input).info("Start ListDocumentForms Operation")

    # TODO: Implement ListDocumentForms Operation. `input` contains the request input

    return Response.internal_failure(InternalFailureErrorResponseContent(
        message="Not Implemented!"
    ))


# Entry point for the AWS Lambda handler for the ListDocumentForms operation.
# The list_document_forms_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = list_document_forms_handler(interceptors=DEFAULT_INTERCEPTORS)(list_document_forms)

