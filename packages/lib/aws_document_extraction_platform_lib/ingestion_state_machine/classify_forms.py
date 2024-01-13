#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from typing import Any, TypedDict, List

from trp import Document

from aws_document_extraction_platform_lib.utils.textract.analysis import (
    get_full_textract_document_analysis,
    BoundingBox,
)
from aws_document_extraction_platform_lib.utils.logger import get_logger

log = get_logger(__name__)


class ClassifyFormsInput(TypedDict):
    JobId: str
    SchemaId: str


class ClassifiedForm(TypedDict):
    schema_id: str
    start_page: int
    end_page: int


class ClassifyFormsOutput(TypedDict):
    forms: List[ClassifiedForm]
    total_document_pages: int


# The title hitbox is a bounding box in which we look for title text in a document
TITLE_HITBOX: BoundingBox = {
    "Top": 0.1,  # 10% from top of document
    "Height": 0.1,  # 10% of document height
    "Left": 0.3,  # 30% from left of document
    "Width": 0.4,  # 40% of document width
}


def handler(event: ClassifyFormsInput, context: Any) -> ClassifyFormsOutput:
    """
    Handler for classifying the document type
    """
    # Get the textract results for the completed job
    result = get_full_textract_document_analysis(event["JobId"])

    # Parse the textract results using amazon textract response parser for easier inspection
    document = Document(result)

    classified_forms: List[ClassifiedForm] = []
    current_page_number = 0
    total_document_pages = len(document.pages)

    classified_forms.append(
        {
            "schema_id": event["SchemaId"],
            "start_page": current_page_number,
            "end_page": total_document_pages,
        }
    )
    return {"forms": classified_forms, "total_document_pages": total_document_pages}
