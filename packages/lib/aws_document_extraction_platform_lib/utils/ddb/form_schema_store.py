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
from aws_document_extraction_platform_api_python_runtime.models.form_schema import (
    FormSchema,
)


class FormSchemaStore(Store):
    """
    Dynamodb store for form schemas
    """

    def __init__(self):
        super().__init__(
            boto3.resource("dynamodb").Table(os.environ["FORM_SCHEMA_TABLE_NAME"]),
            FormSchema,
        )

    def _key(self, schema_id: str) -> Dict:
        return {"schemaId": schema_id}

    def put_form_schema(self, user: str, schema: FormSchema) -> FormSchema:
        return super().put(self._key(schema.schema_id), user, schema)

    def get_form_schema(self, schema_id: str) -> Optional[FormSchema]:
        return super().get(self._key(schema_id))

    def delete_form_schema_if_exists(self, schema_id: str) -> Optional[FormSchema]:
        return super().delete_if_exists(self._key(schema_id))

    def list_all(
        self, pagination_params: PaginationParameters
    ) -> PaginatedItemsResponse[FormSchema]:
        return super().list(pagination_params)
