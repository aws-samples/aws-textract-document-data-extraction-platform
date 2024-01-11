from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_api_python_runtime.interceptors import INTERCEPTORS
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import LoggingInterceptor
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    list_form_schemas_handler, ListFormSchemasRequest, ListFormSchemasOperationResponses
)


def list_form_schemas(input: ListFormSchemasRequest, **kwargs) -> ListFormSchemasOperationResponses:
    """
    Type-safe handler for the ListFormSchemas operation
    """
    LoggingInterceptor.get_logger(input).info("Start ListFormSchemas Operation")

    # TODO: Implement ListFormSchemas Operation. `input` contains the request input

    return Response.internal_failure(InternalFailureErrorResponseContent(
        message="Not Implemented!"
    ))


# Entry point for the AWS Lambda handler for the ListFormSchemas operation.
# The list_form_schemas_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = list_form_schemas_handler(interceptors=INTERCEPTORS)(list_form_schemas)

