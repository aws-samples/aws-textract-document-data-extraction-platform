from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_api_python_runtime.interceptors import INTERCEPTORS
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import LoggingInterceptor
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    get_document_form_handler, GetDocumentFormRequest, GetDocumentFormOperationResponses
)


def get_document_form(input: GetDocumentFormRequest, **kwargs) -> GetDocumentFormOperationResponses:
    """
    Type-safe handler for the GetDocumentForm operation
    """
    LoggingInterceptor.get_logger(input).info("Start GetDocumentForm Operation")

    # TODO: Implement GetDocumentForm Operation. `input` contains the request input

    return Response.internal_failure(InternalFailureErrorResponseContent(
        message="Not Implemented!"
    ))


# Entry point for the AWS Lambda handler for the GetDocumentForm operation.
# The get_document_form_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = get_document_form_handler(interceptors=INTERCEPTORS)(get_document_form)

