#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from api_python_client.model.execution_status import ExecutionStatus
from api_python_client.apis.tags.default_api_operation_config import (
    list_document_forms_handler,
    ListDocumentFormsRequest,
    ListFormsResponse,
)
from api_python_client.model.api_error import ApiError

from aws_lambdas.api.utils.api import api, identity_interceptor
from aws_lambdas.api.utils.response import Response, ApiResponse
from aws_lambdas.utils.ddb.form_metadata_store import FormMetadataStore
from aws_lambdas.utils.ddb.document_metadata_store import DocumentMetadataStore
from aws_lambdas.utils.ddb.store import (
    to_paginated_response_args,
    to_pagination_parameters,
)


@list_document_forms_handler(interceptors=[identity_interceptor])
def handler(
    input: ListDocumentFormsRequest, **kwargs
) -> ApiResponse[ListFormsResponse]:
    """
    Handler for listing the forms in an ingested document
    """
    document_id = input.request_parameters["documentId"]
    document = DocumentMetadataStore().get_document_metadata(document_id)

    if document is None:
        return Response.not_found(
            ApiError(message="No document found with id {}".format(document_id))
        )

    if document["ingestionExecution"]["status"] != ExecutionStatus("SUCCEEDED"):
        return Response.bad_request(
            ApiError(
                message="Cannot retrieve forms for document with ingestion status {}".format(
                    document["ingestionExecution"]["status"]
                )
            )
        )

    response = FormMetadataStore().list_forms_in_document(
        document_id, to_pagination_parameters(input.request_parameters)
    )
    if response.error is not None:
        return Response.bad_request(ApiError(message=response.error))

    return Response.success(
        ListFormsResponse(forms=response.items, **to_paginated_response_args(response))
    )
