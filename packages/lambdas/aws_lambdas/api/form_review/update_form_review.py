#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from api_python_client.api.default_api_operation_config import (
    update_form_review_handler,
    UpdateFormReviewRequest,
)
from api_python_client.model.form_metadata import FormMetadata
from api_python_client.model.api_error import ApiError

from aws_lambdas.api.utils.api import api, CallingUser, DefaultCallingUser
from aws_lambdas.api.utils.response import Response, ApiResponse
from aws_lambdas.utils.ddb.form_metadata_store import FormMetadataStore


@api
@update_form_review_handler
def handler(
    input: UpdateFormReviewRequest,
    caller: CallingUser = DefaultCallingUser,
    **kwargs,
) -> ApiResponse[FormMetadata]:
    """
    Handler for updating a form review
    """
    document_id = input.request_parameters["documentId"]
    form_id = input.request_parameters["formId"]

    extracted_data_update = input.body.extracted_data

    store = FormMetadataStore()
    document_form = store.get_form_metadata(document_id, form_id)

    if document_form is None:
        return Response.bad_request(
            ApiError(
                message="No document form found with document id {} and form id {}".format(
                    document_id, form_id
                )
            )
        )

    if "tags" in input.body:
        document_form.tags = input.body.tags
    if "notes" in input.body:
        document_form.notes = input.body.notes

    document_form.extractedData = extracted_data_update

    updated_form_review = store.put_form_metadata(caller.username, document_form)

    return Response.success(updated_form_review)
