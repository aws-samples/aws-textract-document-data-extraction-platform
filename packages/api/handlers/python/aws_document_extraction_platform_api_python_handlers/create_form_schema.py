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
    create_form_schema_handler,
    CreateFormSchemaRequest,
    CreateFormSchemaOperationResponses,
)


def create_form_schema(
    input: CreateFormSchemaRequest, **kwargs
) -> CreateFormSchemaOperationResponses:
    """
    Type-safe handler for the CreateFormSchema operation
    """
    LoggingInterceptor.get_logger(input).info("Start CreateFormSchema Operation")

    # Lowercase form title is used as the schema id. This allows for a fast lookup for potential matching schemas during
    # the form classification phase
    caller = input.interceptor_context["AuthenticatedUser"]
    schema_id = input.body.title.lower()

    store = FormSchemaStore()
    existing_schema = store.get_form_schema(schema_id)
    if existing_schema is not None:
        return Response.bad_request(
            ApiError(message="Schema already exists with id {}".format(schema_id))
        )

    schema = FormSchemaStore().put_form_schema(
        caller.username,
        FormSchema(
            schemaId=schema_id,
            schema=input.body.var_schema,
            title=input.body.title,
            description=input.body.description,
        ),
    )

    return Response.success(schema)


# Entry point for the AWS Lambda handler for the CreateFormSchema operation.
# The create_form_schema_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = create_form_schema_handler(interceptors=DEFAULT_INTERCEPTORS)(
    create_form_schema
)
