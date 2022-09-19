#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#

from api_python_client.apis.tags.default_api_operation_config import (
    list_form_schemas_handler,
    ListFormSchemasRequest,
)
from api_python_client.model.api_error import ApiError
from api_python_client.model.list_form_schemas_response import ListFormSchemasResponse

from aws_lambdas.api.utils.api import api
from aws_lambdas.api.utils.response import Response, ApiResponse
from aws_lambdas.utils.ddb.form_schema_store import FormSchemaStore
from aws_lambdas.utils.ddb.store import (
    to_pagination_parameters,
    to_paginated_response_args,
)


@api
@list_form_schemas_handler
def handler(
    input: ListFormSchemasRequest, **kwargs
) -> ApiResponse[ListFormSchemasResponse]:
    """
    Handler for listing all form schemas
    """
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
