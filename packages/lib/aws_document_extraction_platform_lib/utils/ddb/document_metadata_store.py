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
from aws_document_extraction_platform_api_python_runtime.models.document_metadata import (
    DocumentMetadata,
)


class DocumentMetadataStore(Store):
    """
    Dynamodb store for document metadata
    """

    def __init__(self):
        super().__init__(
            boto3.resource("dynamodb").Table(
                os.environ["DOCUMENT_METADATA_TABLE_NAME"]
            ),
            DocumentMetadata,
        )

    def _key(self, document_id: str) -> Dict:
        return {"documentId": document_id}

    def put_document_metadata(
        self, user: str, document: DocumentMetadata
    ) -> DocumentMetadata:
        return super().put(self._key(document.document_id), user, document)

    def get_document_metadata(self, document_id: str) -> Optional[DocumentMetadata]:
        return super().get(self._key(document_id))

    def list_all(
        self, pagination_params: PaginationParameters
    ) -> PaginatedItemsResponse[DocumentMetadata]:
        return super().list(pagination_params)
