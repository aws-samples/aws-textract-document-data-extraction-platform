#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from api_python_client.apis.tags.default_api_operation_config import (
    create_form_review_workflow_tag_handler,
    CreateFormReviewWorkflowTagRequest,
)
from api_python_client.model.form_review_workflow_tag import FormReviewWorkflowTag
from api_python_client.model.api_error import ApiError

from aws_lambdas.api.utils.api import api, CallingUser, DefaultCallingUser
from aws_lambdas.api.utils.response import Response, ApiResponse
from aws_lambdas.utils.ddb.form_review_workflow_tag_store import (
    FormReviewWorkflowTagStore,
    PaginationParameters,
)

from hashlib import sha256


@api
@create_form_review_workflow_tag_handler
def handler(
    input: CreateFormReviewWorkflowTagRequest,
    caller: CallingUser = DefaultCallingUser,
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

    tag_id = sha256(input.body.tag_text.encode("utf-8")).hexdigest()[0:32]

    new_tag = FormReviewWorkflowTagStore().put_form_review_workflow_tag(
        caller.username,
        FormReviewWorkflowTag(
            tag_id=tag_id,
            tag_text=input.body.tag_text,
        ),
    )

    return Response.success(new_tag)
