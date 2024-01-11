from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_api_python_runtime.interceptors import INTERCEPTORS
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import LoggingInterceptor
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    submit_source_document_handler, SubmitSourceDocumentRequest, SubmitSourceDocumentOperationResponses
)


def submit_source_document(input: SubmitSourceDocumentRequest, **kwargs) -> SubmitSourceDocumentOperationResponses:
    """
    Type-safe handler for the SubmitSourceDocument operation
    """
    LoggingInterceptor.get_logger(input).info("Start SubmitSourceDocument Operation")

    # TODO: Implement SubmitSourceDocument Operation. `input` contains the request input

    return Response.internal_failure(InternalFailureErrorResponseContent(
        message="Not Implemented!"
    ))


# Entry point for the AWS Lambda handler for the SubmitSourceDocument operation.
# The submit_source_document_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = submit_source_document_handler(interceptors=INTERCEPTORS)(submit_source_document)

