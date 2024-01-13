#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from typing import TypedDict, List, no_type_check
from PyPDF2 import PdfFileReader

from aws_document_extraction_platform_lib.ingestion_state_machine.classify_forms import (
    ClassifiedForm,
)
from aws_document_extraction_platform_lib.utils.s3.location import (
    S3Location,
    get_form_key,
    get_file_name_from_document_key,
)
from aws_document_extraction_platform_lib.utils.pdf import (
    read_pdf_from_s3,
    get_pdf_pages,
    write_pdf_to_s3,
)


class SplitDocumentInput(TypedDict):
    document_id: str
    document_location: S3Location
    classified_forms: List[ClassifiedForm]


class ClassifiedSplitForm(ClassifiedForm):
    document_id: str
    form_id: str
    location: S3Location


class SplitDocumentOutput(TypedDict):
    forms: List[ClassifiedSplitForm]


@no_type_check  # https://github.com/python/mypy/issues/6462 - mypy doesn't follow the types for 'update' which is used in the ** below...
def _write_split_form_to_s3(
    document_id: str,
    form_id: str,
    document_location: S3Location,
    document_pdf: PdfFileReader,
    form: ClassifiedForm,
) -> ClassifiedSplitForm:
    """
    Take the pages from the document that were classified as the given form, and write to s3 as a new pdf
    """
    form_location: S3Location = {
        "bucket": document_location["bucket"],
        "objectKey": get_form_key(
            document_id,
            get_file_name_from_document_key(document_location["objectKey"]),
            form_id,
        ),
    }
    pdf_form_pages = get_pdf_pages(document_pdf, form["start_page"], form["end_page"])
    write_pdf_to_s3(pdf_form_pages, form_location["bucket"], form_location["key"])

    return {
        **form,
        "document_id": document_id,
        "form_id": form_id,
        "location": form_location,
    }


def handler(event: SplitDocumentInput, context) -> SplitDocumentOutput:
    """
    Handler for saving the classified forms as separate split pdf documents in s3
    """

    split_forms = []

    document_id = event["document_id"]
    document_location = event["document_location"]
    document_pdf = read_pdf_from_s3(
        document_location["bucket"], document_location["objectKey"]
    )

    for i in range(0, len(event["classified_forms"])):
        form = event["classified_forms"][i]
        form_id = "{}_{}".format(form["schema_id"].replace(" ", "_"), i)
        split_forms.append(
            _write_split_form_to_s3(
                document_id, form_id, document_location, document_pdf, form
            )
        )

    return {"forms": split_forms}
