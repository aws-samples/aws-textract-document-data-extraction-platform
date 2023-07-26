#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#

from aws_api_python_runtime.apis.tags.default_api_operation_config import (
    list_documents_handler,
    ListDocumentsRequest,
)
from aws_api_python_runtime.model.api_error import ApiError
from aws_api_python_runtime.model.list_documents_response import ListDocumentsResponse

from aws_lambdas.api.utils.api import api, identity_interceptor
from aws_lambdas.api.utils.response import Response, ApiResponse
from aws_lambdas.utils.ddb.document_metadata_store import DocumentMetadataStore
from aws_lambdas.utils.ddb.store import (
    to_pagination_parameters,
    to_paginated_response_args,
)


@list_documents_handler(interceptors=[identity_interceptor])
def handler(
    input: ListDocumentsRequest, **kwargs
) -> ApiResponse[ListDocumentsResponse]:
    """
    Handler for listing all ingested documents
    """
    response = DocumentMetadataStore().list_all(
        to_pagination_parameters(input.request_parameters)
    )
    if response.error is not None:
        return Response.bad_request(ApiError(message=response.error))

    return Response.success(
        ListDocumentsResponse(
            documents=response.items, **to_paginated_response_args(response)
        )
    )
