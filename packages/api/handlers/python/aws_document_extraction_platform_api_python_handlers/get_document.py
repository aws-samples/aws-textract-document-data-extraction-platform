from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_api_python_handlers.interceptors import DEFAULT_INTERCEPTORS
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import LoggingInterceptor
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    get_document_handler, GetDocumentRequest, GetDocumentOperationResponses
)


def get_document(input: GetDocumentRequest, **kwargs) -> GetDocumentOperationResponses:
    """
    Type-safe handler for the GetDocument operation
    """
    LoggingInterceptor.get_logger(input).info("Start GetDocument Operation")

    # TODO: Implement GetDocument Operation. `input` contains the request input

    return Response.internal_failure(InternalFailureErrorResponseContent(
        message="Not Implemented!"
    ))


# Entry point for the AWS Lambda handler for the GetDocument operation.
# The get_document_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = get_document_handler(interceptors=DEFAULT_INTERCEPTORS)(get_document)

