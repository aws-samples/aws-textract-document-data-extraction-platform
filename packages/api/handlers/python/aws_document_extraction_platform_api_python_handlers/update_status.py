from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_api_python_runtime.interceptors import INTERCEPTORS
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import LoggingInterceptor
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    update_status_handler, UpdateStatusRequest, UpdateStatusOperationResponses
)


def update_status(input: UpdateStatusRequest, **kwargs) -> UpdateStatusOperationResponses:
    """
    Type-safe handler for the UpdateStatus operation
    """
    LoggingInterceptor.get_logger(input).info("Start UpdateStatus Operation")

    # TODO: Implement UpdateStatus Operation. `input` contains the request input

    return Response.internal_failure(InternalFailureErrorResponseContent(
        message="Not Implemented!"
    ))


# Entry point for the AWS Lambda handler for the UpdateStatus operation.
# The update_status_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = update_status_handler(interceptors=INTERCEPTORS)(update_status)