from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_api_python_runtime.interceptors import INTERCEPTORS
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import LoggingInterceptor
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    update_form_schema_handler, UpdateFormSchemaRequest, UpdateFormSchemaOperationResponses
)


def update_form_schema(input: UpdateFormSchemaRequest, **kwargs) -> UpdateFormSchemaOperationResponses:
    """
    Type-safe handler for the UpdateFormSchema operation
    """
    LoggingInterceptor.get_logger(input).info("Start UpdateFormSchema Operation")

    # TODO: Implement UpdateFormSchema Operation. `input` contains the request input

    return Response.internal_failure(InternalFailureErrorResponseContent(
        message="Not Implemented!"
    ))


# Entry point for the AWS Lambda handler for the UpdateFormSchema operation.
# The update_form_schema_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = update_form_schema_handler(interceptors=INTERCEPTORS)(update_form_schema)

