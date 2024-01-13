#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_lib.utils.ddb.document_metadata_store import (
    DocumentMetadataStore,
)
from aws_document_extraction_platform_lib.utils.ddb.form_metadata_store import (
    FormMetadataStore,
)
from aws_document_extraction_platform_lib.utils.metrics.accuracy import (
    compute_extraction_accuracy_percentage,
)
from aws_document_extraction_platform_lib.utils.metrics.metrics import metric_publisher
from aws_document_extraction_platform_lib.utils.time import utc_now
from aws_document_extraction_platform_api_python_handlers.interceptors import (
    DEFAULT_INTERCEPTORS,
)
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import (
    LoggingInterceptor,
)
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    update_status_handler,
    UpdateStatusRequest,
    UpdateStatusOperationResponses,
)


def update_status(
    input: UpdateStatusRequest, **kwargs
) -> UpdateStatusOperationResponses:
    """
    Type-safe handler for the UpdateStatus operation
    """
    LoggingInterceptor.get_logger(input).info("Start UpdateStatus Operation")

    caller = input.interceptor_context["AuthenticatedUser"]
    document_id = input.request_parameters.document_id
    form_id = input.request_parameters.form_id
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

    if new_status == document_form.extraction_execution.status:
        return Response.bad_request(
            ApiError(message="Cannot update status to the same status")
        )
    status_transition_log = list(document_form.status_transition_log)
    status_transition_log.append(
        StatusTransition(
            timestamp=utc_now(),
            status=new_status,
            actingUser=caller.username,
        )
    )
    document_form.status_transition_log = status_transition_log
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


# Entry point for the AWS Lambda handler for the UpdateStatus operation.
# The update_status_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = update_status_handler(interceptors=DEFAULT_INTERCEPTORS)(update_status)
