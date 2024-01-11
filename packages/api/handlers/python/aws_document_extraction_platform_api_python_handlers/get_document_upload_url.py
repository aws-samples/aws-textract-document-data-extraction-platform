from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_api_python_runtime.interceptors import INTERCEPTORS
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import LoggingInterceptor
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    get_document_upload_url_handler, GetDocumentUploadUrlRequest, GetDocumentUploadUrlOperationResponses
)


def get_document_upload_url(input: GetDocumentUploadUrlRequest, **kwargs) -> GetDocumentUploadUrlOperationResponses:
    """
    Type-safe handler for the GetDocumentUploadUrl operation
    """
    LoggingInterceptor.get_logger(input).info("Start GetDocumentUploadUrl Operation")

    # TODO: Implement GetDocumentUploadUrl Operation. `input` contains the request input

    return Response.internal_failure(InternalFailureErrorResponseContent(
        message="Not Implemented!"
    ))


# Entry point for the AWS Lambda handler for the GetDocumentUploadUrl operation.
# The get_document_upload_url_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = get_document_upload_url_handler(interceptors=INTERCEPTORS)(get_document_upload_url)

