from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_api_python_runtime.interceptors import INTERCEPTORS
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import LoggingInterceptor
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    delete_form_schema_handler, DeleteFormSchemaRequest, DeleteFormSchemaOperationResponses
)


def delete_form_schema(input: DeleteFormSchemaRequest, **kwargs) -> DeleteFormSchemaOperationResponses:
    """
    Type-safe handler for the DeleteFormSchema operation
    """
    LoggingInterceptor.get_logger(input).info("Start DeleteFormSchema Operation")

    # TODO: Implement DeleteFormSchema Operation. `input` contains the request input

    return Response.internal_failure(InternalFailureErrorResponseContent(
        message="Not Implemented!"
    ))


# Entry point for the AWS Lambda handler for the DeleteFormSchema operation.
# The delete_form_schema_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = delete_form_schema_handler(interceptors=INTERCEPTORS)(delete_form_schema)

