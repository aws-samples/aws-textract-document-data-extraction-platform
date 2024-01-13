#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_api_python_handlers.interceptors import (
    DEFAULT_INTERCEPTORS,
)
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import (
    LoggingInterceptor,
)
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    create_form_review_workflow_tag_handler,
    CreateFormReviewWorkflowTagRequest,
    CreateFormReviewWorkflowTagOperationResponses,
)

from aws_document_extraction_platform_lib.utils.ddb.form_review_workflow_tag_store import (
    FormReviewWorkflowTagStore,
)

from hashlib import sha256


def create_form_review_workflow_tag(
    input: CreateFormReviewWorkflowTagRequest, **kwargs
) -> CreateFormReviewWorkflowTagOperationResponses:
    """
    Type-safe handler for the CreateFormReviewWorkflowTag operation
    """
    LoggingInterceptor.get_logger(input).info(
        "Start CreateFormReviewWorkflowTag Operation"
    )

    # creating a new tag with a value that matches an existing entry should not
    # create multiple entries for that value, so use the hash of the value to
    # avoid this (doing a put on the an existing matching key by definition
    # means that the new tag value is the same, so it's effectively a no-op, so
    # we don't need to do a get to check for a pre-existing matching entry)
    caller = input.interceptor_context["AuthenticatedUser"]
    tag_id = sha256(input.body.tag_text.encode("utf-8")).hexdigest()[0:32]

    new_tag = FormReviewWorkflowTagStore().put_form_review_workflow_tag(
        caller.username,
        FormReviewWorkflowTag(
            tagId=tag_id,
            tagText=input.body.tag_text,
        ),
    )

    return Response.success(new_tag)


# Entry point for the AWS Lambda handler for the CreateFormReviewWorkflowTag operation.
# The create_form_review_workflow_tag_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = create_form_review_workflow_tag_handler(interceptors=DEFAULT_INTERCEPTORS)(
    create_form_review_workflow_tag
)
