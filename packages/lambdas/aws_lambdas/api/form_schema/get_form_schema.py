#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#

from api_python_client.model.form_schema import FormSchema
from api_python_client.api.default_api_operation_config import (
    get_form_schema_handler,
    GetFormSchemaRequest,
)
from api_python_client.model.api_error import ApiError

from aws_lambdas.api.utils.api import api
from aws_lambdas.api.utils.response import Response, ApiResponse
from aws_lambdas.utils.ddb.form_schema_store import FormSchemaStore


@api
@get_form_schema_handler
def handler(input: GetFormSchemaRequest, **kwargs) -> ApiResponse[FormSchema]:
    """
    Handler for retrieving a form schema
    """
    schema_id = input.request_parameters["schemaId"]

    schema = FormSchemaStore().get_form_schema(schema_id)
    if schema is None:
        return Response.not_found(
            ApiError(message="No form schema found with id {}".format(schema_id))
        )
    return Response.success(schema)
