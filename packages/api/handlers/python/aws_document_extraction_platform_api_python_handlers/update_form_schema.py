#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from typing import Any
import aws_document_extraction_platform_api_python_runtime
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
    update_form_schema_handler,
    UpdateFormSchemaRequest,
    UpdateFormSchemaOperationResponses,
)
import json

# HACK! Patch body parser since "schemaId" is not included in FormSchema.from_dict
def patched_parse_body(body, content_types, model):
    """
    Parse the body of an api request into the given model if present
    """
    if len([c for c in content_types if c != "application/json"]) == 0:
        if model != Any:
            body = model.model_validate(json.loads(body))
        else:
            body = json.loads(body or "{}")
    return body


aws_document_extraction_platform_api_python_runtime.api.operation_config.parse_body = (
    patched_parse_body
)


def update_form_schema(
    input: UpdateFormSchemaRequest, **kwargs
) -> UpdateFormSchemaOperationResponses:
    """
    Type-safe handler for the UpdateFormSchema operation
    """
    LoggingInterceptor.get_logger(input).info("Start UpdateFormSchema Operation")

    caller = input.interceptor_context["AuthenticatedUser"]
    schema_id = input.request_parameters.schema_id
    input_schema = input.body

    if input_schema.schema_id != schema_id:
        return Response.bad_request(
            ApiError("Schema id in path and payload must match!")
        )

    store = FormSchemaStore()
    existing_schema = store.get_form_schema(schema_id)

    if existing_schema is None:
        return Response.bad_request(
            ApiError(message="No schema found with id {}".format(schema_id))
        )

    schema = FormSchemaStore().put_form_schema(caller.username, input_schema)

    return Response.success(schema)


# Entry point for the AWS Lambda handler for the UpdateFormSchema operation.
# The update_form_schema_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = update_form_schema_handler(interceptors=DEFAULT_INTERCEPTORS)(
    update_form_schema
)
