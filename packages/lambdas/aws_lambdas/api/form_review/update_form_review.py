#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from api_python_client.apis.tags.default_api_operation_config import (
    update_form_review_handler,
    UpdateFormReviewRequest,
)
from api_python_client.model.form_metadata import FormMetadata
from api_python_client.model.api_error import ApiError
from api_python_client.api_client import JSONEncoder

from aws_lambdas.api.utils.api import (
    identity_interceptor,
)
from aws_lambdas.api.utils.response import Response, ApiResponse
from aws_lambdas.utils.ddb.form_metadata_store import FormMetadataStore


@update_form_review_handler(interceptors=[identity_interceptor])
def handler(
    input: UpdateFormReviewRequest,
    **kwargs,
) -> ApiResponse[FormMetadata]:
    """
    Handler for updating a form review
    """
    caller = input.interceptor_context["AuthenticatedUser"]
    document_id = input.request_parameters["documentId"]
    form_id = input.request_parameters["formId"]

    extracted_data_update = input.body["extractedData"]

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

    new_document_form = JSONEncoder().default(document_form)

    if "tags" in input.body:
        new_document_form["tags"] = input.body["tags"]
    if "notes" in input.body:
        new_document_form["notes"] = input.body["notes"]

    new_document_form["extractedData"] = extracted_data_update

    new_document_form = FormMetadata(**new_document_form)
    print("Document: {}".format(new_document_form))

    updated_form_review = store.put_form_metadata(caller.username, new_document_form)

    return Response.success(updated_form_review)
