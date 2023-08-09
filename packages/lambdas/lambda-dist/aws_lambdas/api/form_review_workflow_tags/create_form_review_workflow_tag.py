#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from aws_api_python_runtime.apis.tags.default_api_operation_config import (
    create_form_review_workflow_tag_handler,
    CreateFormReviewWorkflowTagRequest,
)
from aws_api_python_runtime.model.form_review_workflow_tag import FormReviewWorkflowTag

from aws_lambdas.api.utils.api import identity_interceptor
from aws_lambdas.api.utils.response import Response, ApiResponse
from aws_lambdas.utils.ddb.form_review_workflow_tag_store import (
    FormReviewWorkflowTagStore,
)

from hashlib import sha256


@create_form_review_workflow_tag_handler(interceptors=[identity_interceptor])
def handler(
    input: CreateFormReviewWorkflowTagRequest,
    **kwargs,
) -> ApiResponse[FormReviewWorkflowTag]:
    """
    Handler for creating a form review workflow tag
    """

    # creating a new tag with a value that matches an existing entry should not
    # create multiple entries for that value, so use the hash of the value to
    # avoid this (doing a put on the an existing matching key by definition
    # means that the new tag value is the same, so it's effectively a no-op, so
    # we don't need to do a get to check for a pre-existing matching entry)
    caller = input.interceptor_context["AuthenticatedUser"]
    tag_id = sha256(input.body["tagText"].encode("utf-8")).hexdigest()[0:32]

    new_tag = FormReviewWorkflowTagStore().put_form_review_workflow_tag(
        caller.username,
        FormReviewWorkflowTag(
            tagId=tag_id,
            tagText=input.body["tagText"],
        ),
    )

    return Response.success(new_tag)
