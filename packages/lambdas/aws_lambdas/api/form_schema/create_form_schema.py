#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from aws_api_python_runtime.apis.tags.default_api_operation_config import (
    create_form_schema_handler,
    CreateFormSchemaRequest,
)
from aws_api_python_runtime.model.form_schema import FormSchema
from aws_api_python_runtime.model.api_error import ApiError

from aws_lambdas.api.utils.api import (
    identity_interceptor,
)
from aws_lambdas.api.utils.response import Response, ApiResponse
from aws_lambdas.utils.ddb.form_schema_store import FormSchemaStore
from aws_lambdas.utils.misc import copy_defined_keys


@create_form_schema_handler(interceptors=[identity_interceptor])
def handler(
    input: CreateFormSchemaRequest,
    **kwargs,
) -> ApiResponse[FormSchema]:
    """
    Handler for creating a form schema
    """
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
            schema=input.body.schema,
            **copy_defined_keys(input.body, ["description", "title"]),
        ),
    )

    return Response.success(schema)
