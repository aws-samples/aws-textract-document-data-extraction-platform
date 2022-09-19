#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from api_python_client.apis.tags.default_api_operation_config import (
    list_forms_handler,
    ListFormsRequest,
    ListFormsResponse,
)
from api_python_client.model.api_error import ApiError

from aws_lambdas.api.utils.api import api
from aws_lambdas.api.utils.response import Response, ApiResponse
from aws_lambdas.utils.ddb.form_metadata_store import FormMetadataStore
from aws_lambdas.utils.ddb.store import (
    to_paginated_response_args,
    to_pagination_parameters,
)


@api
@list_forms_handler
def handler(input: ListFormsRequest, **kwargs) -> ApiResponse[ListFormsResponse]:
    """
    Handler for listing all nested forms in all documents
    """

    response = FormMetadataStore().list_all(
        to_pagination_parameters(input.request_parameters)
    )
    if response.error is not None:
        return Response.bad_request(ApiError(message=response.error))

    return Response.success(
        ListFormsResponse(forms=response.items, **to_paginated_response_args(response))
    )
