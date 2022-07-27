#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from api_python_client.api.default_api_operation_config import (
    update_status_handler,
    UpdateStatusRequest,
)
from api_python_client.model.form_metadata import FormMetadata
from api_python_client.model.api_error import ApiError
from api_python_client.model.status_transition import StatusTransition

from aws_lambdas.api.utils.api import api, CallingUser, DefaultCallingUser
from aws_lambdas.api.utils.response import Response, ApiResponse
from aws_lambdas.utils.ddb.form_metadata_store import FormMetadataStore
from aws_lambdas.utils.time import utc_now
from aws_lambdas.utils.metrics.accuracy import compute_extraction_accuracy_percentage
from aws_lambdas.utils.metrics.metrics import metric_publisher
from aws_lambdas.utils.ddb.document_metadata_store import DocumentMetadataStore


@api
@update_status_handler
def handler(
    input: UpdateStatusRequest,
    caller: CallingUser = DefaultCallingUser,
    **kwargs,
) -> ApiResponse[FormMetadata]:
    """
    Handler for updating a document form's status
    """
    document_id = input.request_parameters["documentId"]
    form_id = input.request_parameters["formId"]
    new_status = input.body.new_status

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

    if new_status == document_form.extraction_execution.status.value:
        return Response.bad_request(
            ApiError(message="Cannot update status to the same status")
        )

    document_form.status_transition_log.append(
        StatusTransition(
            timestamp=utc_now(),
            status=new_status,
            acting_user=caller.username,
        )
    )
    document_form.extraction_execution.status = new_status

    # When a review has been completed, add the accuracy and review time metrics
    if new_status == "REVIEWED":
        document_form.extraction_accuracy = compute_extraction_accuracy_percentage(
            document_form
        )
        document = DocumentMetadataStore().get_document_metadata(document_id)
        if document is None:
            return Response.not_found(
                ApiError(message="No document found with id {}".format(document_id))
            )
        with metric_publisher() as m:
            m.add_review_time(document_form)
            m.add_end_to_end_time(document, document_form)
            m.add_extraction_accuracy(document_form)

    updated_document_form = store.put_form_metadata(caller.username, document_form)
    return Response.success(updated_document_form)
