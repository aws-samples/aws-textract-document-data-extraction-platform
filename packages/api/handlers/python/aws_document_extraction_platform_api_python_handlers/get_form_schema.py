from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_api_python_runtime.interceptors import INTERCEPTORS
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import LoggingInterceptor
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    get_form_schema_handler, GetFormSchemaRequest, GetFormSchemaOperationResponses
)


def get_form_schema(input: GetFormSchemaRequest, **kwargs) -> GetFormSchemaOperationResponses:
    """
    Type-safe handler for the GetFormSchema operation
    """
    LoggingInterceptor.get_logger(input).info("Start GetFormSchema Operation")

    # TODO: Implement GetFormSchema Operation. `input` contains the request input

    return Response.internal_failure(InternalFailureErrorResponseContent(
        message="Not Implemented!"
    ))


# Entry point for the AWS Lambda handler for the GetFormSchema operation.
# The get_form_schema_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = get_form_schema_handler(interceptors=INTERCEPTORS)(get_form_schema)

