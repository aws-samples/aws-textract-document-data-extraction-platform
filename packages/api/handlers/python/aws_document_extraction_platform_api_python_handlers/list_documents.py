from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_api_python_runtime.interceptors import INTERCEPTORS
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import LoggingInterceptor
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    list_documents_handler, ListDocumentsRequest, ListDocumentsOperationResponses
)


def list_documents(input: ListDocumentsRequest, **kwargs) -> ListDocumentsOperationResponses:
    """
    Type-safe handler for the ListDocuments operation
    """
    LoggingInterceptor.get_logger(input).info("Start ListDocuments Operation")

    # TODO: Implement ListDocuments Operation. `input` contains the request input

    return Response.internal_failure(InternalFailureErrorResponseContent(
        message="Not Implemented!"
    ))


# Entry point for the AWS Lambda handler for the ListDocuments operation.
# The list_documents_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = list_documents_handler(interceptors=INTERCEPTORS)(list_documents)

