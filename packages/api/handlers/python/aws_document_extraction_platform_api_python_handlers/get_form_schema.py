#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_lib.utils.ddb.form_schema_store import (
    FormSchemaStore,
)
from aws_document_extraction_platform_api_python_handlers.interceptors import (
    DEFAULT_INTERCEPTORS,
)
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import (
    LoggingInterceptor,
)
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    get_form_schema_handler,
    GetFormSchemaRequest,
    GetFormSchemaOperationResponses,
)


def get_form_schema(
    input: GetFormSchemaRequest, **kwargs
) -> GetFormSchemaOperationResponses:
    """
    Type-safe handler for the GetFormSchema operation
    """
    LoggingInterceptor.get_logger(input).info("Start GetFormSchema Operation")

    schema_id = input.request_parameters.schema_id

    schema = FormSchemaStore().get_form_schema(schema_id)
    if schema is None:
        return Response.not_found(
            ApiError(message="No form schema found with id {}".format(schema_id))
        )
    return Response.success(schema)


# Entry point for the AWS Lambda handler for the GetFormSchema operation.
# The get_form_schema_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = get_form_schema_handler(interceptors=DEFAULT_INTERCEPTORS)(get_form_schema)
