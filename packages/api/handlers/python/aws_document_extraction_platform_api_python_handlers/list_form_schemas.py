from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_lib.utils.ddb.form_schema_store import FormSchemaStore
from aws_document_extraction_platform_lib.utils.ddb.store import to_paginated_response_args, to_pagination_parameters
from aws_document_extraction_platform_api_python_handlers.interceptors import DEFAULT_INTERCEPTORS
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import LoggingInterceptor
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    list_form_schemas_handler, ListFormSchemasRequest, ListFormSchemasOperationResponses
)


def list_form_schemas(input: ListFormSchemasRequest, **kwargs) -> ListFormSchemasOperationResponses:
    """
    Type-safe handler for the ListFormSchemas operation
    """
    LoggingInterceptor.get_logger(input).info("Start ListFormSchemas Operation")

    response = FormSchemaStore().list_all(
        to_pagination_parameters(input.request_parameters)
    )
    if response.error is not None:
        return Response.bad_request(ApiError(message=response.error))

    return Response.success(
        ListFormSchemasResponse(
            schemas=response.items, **to_paginated_response_args(response)
        )
    )


# Entry point for the AWS Lambda handler for the ListFormSchemas operation.
# The list_form_schemas_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = list_form_schemas_handler(interceptors=DEFAULT_INTERCEPTORS)(list_form_schemas)

