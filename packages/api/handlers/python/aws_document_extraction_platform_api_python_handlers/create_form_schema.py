from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_api_python_handlers.interceptors import DEFAULT_INTERCEPTORS
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import LoggingInterceptor
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    create_form_schema_handler, CreateFormSchemaRequest, CreateFormSchemaOperationResponses
)


def create_form_schema(input: CreateFormSchemaRequest, **kwargs) -> CreateFormSchemaOperationResponses:
    """
    Type-safe handler for the CreateFormSchema operation
    """
    LoggingInterceptor.get_logger(input).info("Start CreateFormSchema Operation")

    # TODO: Implement CreateFormSchema Operation. `input` contains the request input

    return Response.internal_failure(InternalFailureErrorResponseContent(
        message="Not Implemented!"
    ))


# Entry point for the AWS Lambda handler for the CreateFormSchema operation.
# The create_form_schema_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = create_form_schema_handler(interceptors=DEFAULT_INTERCEPTORS)(create_form_schema)

