from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_api_python_runtime.interceptors import INTERCEPTORS
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import LoggingInterceptor
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    say_hello_handler, SayHelloRequest, SayHelloOperationResponses
)


def say_hello(input: SayHelloRequest, **kwargs) -> SayHelloOperationResponses:
    """
    Type-safe handler for the SayHello operation
    """
    LoggingInterceptor.get_logger(input).info("Start SayHello Operation")

    # TODO: Implement SayHello Operation. `input` contains the request input

    return Response.internal_failure(InternalFailureErrorResponseContent(
        message="Not Implemented!"
    ))


# Entry point for the AWS Lambda handler for the SayHello operation.
# The say_hello_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = say_hello_handler(interceptors=INTERCEPTORS)(say_hello)