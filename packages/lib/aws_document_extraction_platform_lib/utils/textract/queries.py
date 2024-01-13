#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from typing import TypedDict, List

from aws_document_extraction_platform_api_python_runtime.models.form_json_schema import (
    FormJSONSchema,
)
from aws_document_extraction_platform_lib.utils.textract.extraction import (
    ordered_object_schema_property_keys,
)


class TextractQuery(TypedDict):
    Alias: str
    Pages: List[str]
    Text: str


def get_queries_from_schema(
    schema: FormJSONSchema, alias: str = ""
) -> List[TextractQuery]:
    """
    Given a document schema, find all optional textract queries specified and return as a flat list to be passed in the
    query configuration for textract.
    """

    if schema.type_of == "object":
        queries = []
        for property_key in ordered_object_schema_property_keys(schema):
            queries += get_queries_from_schema(
                schema.properties[property_key],
                alias + ("" if len(alias) == 0 else ".") + property_key,
            )
        return queries
    elif schema.type_of == "array":
        # Ignore any queries specified in array types. Queries are for a single question, single answer extraction, and
        # we don't know how many items we need to query for upfront. If min/max lengths are set for the array it might
        # be possible to ask a variant of the query for each individual item.
        return []

    # Primitive types (string, integer etc)
    if (
        schema.extraction_metadata is not None
        and schema.extraction_metadata.textract_query is not None
    ):
        return [
            {
                "Alias": alias,
                "Pages": ["*"],  # all pages
                "Text": schema.extraction_metadata.textract_query,
            }
        ]

    return []
