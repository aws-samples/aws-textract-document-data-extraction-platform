#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from aws_api_python_runtime.model.form_schema import FormSchema
from aws_api_python_runtime.apis.tags.default_api_operation_config import (
    delete_form_schema_handler,
    DeleteFormSchemaRequest,
)
from aws_api_python_runtime.model.api_error import ApiError

from aws_lambdas.api.utils.api import api, identity_interceptor
from aws_lambdas.api.utils.response import Response, ApiResponse
from aws_lambdas.utils.ddb.form_schema_store import FormSchemaStore


@delete_form_schema_handler(interceptors=[identity_interceptor])
def handler(input: DeleteFormSchemaRequest, **kwargs) -> ApiResponse[FormSchema]:
    """
    Handler for deleting a form schema
    """
    schema_id = input.request_parameters["schemaId"]

    schema = FormSchemaStore().delete_form_schema_if_exists(schema_id)
    if schema is None:
        return Response.not_found(
            ApiError(message="No form schema found with id {}".format(schema_id))
        )
    return Response.success(schema)
