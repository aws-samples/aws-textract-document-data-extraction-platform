#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#

from api_python_client.model.document_metadata import DocumentMetadata
from api_python_client.apis.tags.default_api_operation_config import (
    get_document_handler,
    GetDocumentRequest,
)
from api_python_client.model.api_error import ApiError
from api_python_client.api_client import JSONEncoder
from aws_lambdas.api.utils.api import api, identity_interceptor
from aws_lambdas.api.utils.response import Response, ApiResponse
from aws_lambdas.utils.ddb.document_metadata_store import DocumentMetadataStore
from aws_lambdas.utils.s3.location import get_presigned_get_url_for_pdf


@get_document_handler(interceptors=[identity_interceptor])
def handler(input: GetDocumentRequest, **kwargs) -> ApiResponse[DocumentMetadata]:
    """
    Handler for retrieving document metadata
    """
    document_id = input.request_parameters["documentId"]
    document = DocumentMetadataStore().get_document_metadata(document_id)
    if document is None:
        return Response.not_found(
            ApiError(message="No document found with id {}".format(document_id))
        )

    document = JSONEncoder().default(document)
    # Add a presigned GET url
    document["url"] = get_presigned_get_url_for_pdf(document["location"])
    document = DocumentMetadata(**document)
    return Response.success(document)
