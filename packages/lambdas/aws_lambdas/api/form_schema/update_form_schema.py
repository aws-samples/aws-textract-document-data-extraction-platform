#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from api_python_client.api.default_api_operation_config import (
    update_form_schema_handler,
    UpdateFormSchemaRequest,
)
from api_python_client.model.form_schema import FormSchema
from api_python_client.model.api_error import ApiError

from aws_lambdas.api.utils.api import api, CallingUser, DefaultCallingUser
from aws_lambdas.api.utils.response import Response, ApiResponse
from aws_lambdas.utils.ddb.form_schema_store import FormSchemaStore


@api
@update_form_schema_handler
def handler(
    input: UpdateFormSchemaRequest,
    caller: CallingUser = DefaultCallingUser,
    **kwargs,
) -> ApiResponse[FormSchema]:
    """
    Handler for updating a form schema
    """
    schema_id = input.request_parameters["schemaId"]
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
