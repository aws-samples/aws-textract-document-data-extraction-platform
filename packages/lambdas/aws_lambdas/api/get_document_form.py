#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#

from api_python_client.model.form_metadata import FormMetadata
from api_python_client.api.default_api_operation_config import (
    get_document_form_handler,
    GetDocumentFormRequest,
)
from api_python_client.model.api_error import ApiError

from aws_lambdas.api.utils.api import api
from aws_lambdas.api.utils.response import Response, ApiResponse
from aws_lambdas.utils.ddb.form_metadata_store import FormMetadataStore
from aws_lambdas.utils.s3.location import get_presigned_get_url_for_pdf


@api
@get_document_form_handler
def handler(input: GetDocumentFormRequest, **kwargs) -> ApiResponse[FormMetadata]:
    """
    Handler for retrieving form metadata
    """
    document_id = input.request_parameters["documentId"]
    form_id = input.request_parameters["formId"]
    form = FormMetadataStore().get_form_metadata(document_id, form_id)
    if form is None:
        return Response.not_found(
            ApiError(
                message="No form found with id {} in document {}".format(
                    form_id, document_id
                )
            )
        )

    # Add a presigned GET url
    form.url = get_presigned_get_url_for_pdf(form.location)

    return Response.success(form)
