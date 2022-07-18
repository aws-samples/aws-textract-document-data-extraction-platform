#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from api_python_client.apis.tags.default_api_operation_config import (
    update_form_schema_handler,
    UpdateFormSchemaRequest,
)
from api_python_client.model.form_schema import FormSchema
from api_python_client.model.api_error import ApiError

from aws_lambdas.api.utils.api import identity_interceptor
from aws_lambdas.api.utils.response import Response, ApiResponse
from aws_lambdas.utils.ddb.form_schema_store import FormSchemaStore


@update_form_schema_handler(interceptors=[identity_interceptor])
def handler(
    input: UpdateFormSchemaRequest,
    **kwargs,
) -> ApiResponse[FormSchema]:
    """
    Handler for updating a form schema
    """
    caller = input.interceptor_context["AuthenticatedUser"]
    schema_id = input.request_parameters["schemaId"]
    input_schema = input.body

    if input_schema.schemaId != schema_id:
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
