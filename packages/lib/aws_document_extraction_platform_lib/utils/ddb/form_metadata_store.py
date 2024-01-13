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
    fetch_page_with_query_for_key_equals,
)
from aws_document_extraction_platform_api_python_runtime.models.form_metadata import (
    FormMetadata,
)


class FormMetadataStore(Store):
    """
    Dynamodb store for form metadata
    """

    def __init__(self):
        super().__init__(
            boto3.resource("dynamodb").Table(os.environ["FORM_METADATA_TABLE_NAME"]),
            FormMetadata,
        )

    def _key(self, document_id: str, form_id: str) -> Dict:
        return {"documentId": document_id, "formId": form_id}

    def put_form_metadata(self, user: str, form: FormMetadata) -> FormMetadata:
        return super().put(self._key(form.document_id, form.form_id), user, form)

    def get_form_metadata(
        self, document_id: str, form_id: str
    ) -> Optional[FormMetadata]:
        return super().get(self._key(document_id, form_id))

    def list_all(
        self, pagination_params: PaginationParameters
    ) -> PaginatedItemsResponse[FormMetadata]:
        return super().list(pagination_params)

    def list_forms_in_document(
        self, document_id: str, pagination_params: PaginationParameters
    ) -> PaginatedItemsResponse[FormMetadata]:
        return super().list(
            pagination_params,
            fetch_page=fetch_page_with_query_for_key_equals("documentId", document_id),
        )
