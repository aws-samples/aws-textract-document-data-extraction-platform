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
    delete_form_schema_handler,
    DeleteFormSchemaRequest,
    DeleteFormSchemaOperationResponses,
)


def delete_form_schema(
    input: DeleteFormSchemaRequest, **kwargs
) -> DeleteFormSchemaOperationResponses:
    """
    Type-safe handler for the DeleteFormSchema operation
    """
    LoggingInterceptor.get_logger(input).info("Start DeleteFormSchema Operation")

    schema_id = input.request_parameters.schema_id

    schema = FormSchemaStore().delete_form_schema_if_exists(schema_id)
    if schema is None:
        return Response.not_found(
            ApiError(message="No form schema found with id {}".format(schema_id))
        )
    return Response.success(schema)


# Entry point for the AWS Lambda handler for the DeleteFormSchema operation.
# The delete_form_schema_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = delete_form_schema_handler(interceptors=DEFAULT_INTERCEPTORS)(
    delete_form_schema
)
