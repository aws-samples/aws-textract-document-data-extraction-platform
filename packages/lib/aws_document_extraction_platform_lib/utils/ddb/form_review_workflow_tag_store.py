#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
import boto3
import os

from typing import Dict, Optional

from aws_document_extraction_platform_lib.utils.ddb.store import (
    Store,
    PaginationParameters,
    PaginatedItemsResponse,
)
from aws_document_extraction_platform_api_python_runtime.models.form_review_workflow_tag import (
    FormReviewWorkflowTag,
)


class FormReviewWorkflowTagStore(Store):
    """
    Dynamodb store for form review workflow tags
    """

    def __init__(self):
        super().__init__(
            boto3.resource("dynamodb").Table(
                os.environ["FORM_REVIEW_WORKFLOW_TAGS_TABLE_NAME"]
            ),
            FormReviewWorkflowTag,
        )

    def _key(self, tag_id: str) -> Dict:
        return {"tagId": tag_id}

    def put_form_review_workflow_tag(
        self, user: str, formReviewTag: FormReviewWorkflowTag
    ) -> FormReviewWorkflowTag:
        return super().put(self._key(formReviewTag.tag_id), user, formReviewTag)

    def get_form_review_workflow_tag(
        self, tag_id: str
    ) -> Optional[FormReviewWorkflowTag]:
        return super().get(self._key(tag_id))

    def delete_form_schema_if_exists(
        self, tag_id: str
    ) -> Optional[FormReviewWorkflowTag]:
        return super().delete_if_exists(self._key(tag_id))

    def list_all(
        self, pagination_params: PaginationParameters
    ) -> PaginatedItemsResponse[FormReviewWorkflowTag]:
        return super().list(pagination_params)
