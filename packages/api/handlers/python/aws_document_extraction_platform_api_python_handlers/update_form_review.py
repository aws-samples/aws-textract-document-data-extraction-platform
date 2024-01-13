#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_lib.utils.ddb.form_metadata_store import (
    FormMetadataStore,
)
from aws_document_extraction_platform_api_python_handlers.interceptors import (
    DEFAULT_INTERCEPTORS,
)
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import (
    LoggingInterceptor,
)
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    update_form_review_handler,
    UpdateFormReviewRequest,
    UpdateFormReviewOperationResponses,
)


def update_form_review(
    input: UpdateFormReviewRequest, **kwargs
) -> UpdateFormReviewOperationResponses:
    """
    Type-safe handler for the UpdateFormReview operation
    """
    LoggingInterceptor.get_logger(input).info("Start UpdateFormReview Operation")

    caller = input.interceptor_context["AuthenticatedUser"]
    document_id = input.request_parameters.document_id
    form_id = input.request_parameters.form_id

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

    if input.body.tags is not None:
        document_form.tags = input.body.tags
    if input.body.notes is not None:
        document_form.notes = input.body.notes

    document_form.extracted_data = extracted_data_update

    updated_form_review = store.put_form_metadata(caller.username, document_form)

    return Response.success(updated_form_review)


# Entry point for the AWS Lambda handler for the UpdateFormReview operation.
# The update_form_review_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = update_form_review_handler(interceptors=DEFAULT_INTERCEPTORS)(
    update_form_review
)
