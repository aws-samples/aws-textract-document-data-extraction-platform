from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_api_python_runtime.interceptors import INTERCEPTORS
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import LoggingInterceptor
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    list_forms_handler, ListFormsRequest, ListFormsOperationResponses
)


def list_forms(input: ListFormsRequest, **kwargs) -> ListFormsOperationResponses:
    """
    Type-safe handler for the ListForms operation
    """
    LoggingInterceptor.get_logger(input).info("Start ListForms Operation")

    # TODO: Implement ListForms Operation. `input` contains the request input

    return Response.internal_failure(InternalFailureErrorResponseContent(
        message="Not Implemented!"
    ))


# Entry point for the AWS Lambda handler for the ListForms operation.
# The list_forms_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = list_forms_handler(interceptors=INTERCEPTORS)(list_forms)

