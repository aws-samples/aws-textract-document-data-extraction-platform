#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
import json
from multiprocessing import process
from typing import TypedDict, List, Dict, no_type_check

from aws_document_extraction_platform_api_python_runtime.models.execution_status import ExecutionStatus
from aws_document_extraction_platform_api_python_runtime.models.form_metadata import FormMetadata
from aws_document_extraction_platform_api_python_runtime.models.form_schema import FormSchema
from aws_document_extraction_platform_api_python_runtime.models.s3_location import S3Location
from aws_document_extraction_platform_api_python_runtime.models.extraction_execution import ExtractionExecution
from aws_document_extraction_platform_api_python_runtime.models.extraction_execution_status import (
    ExtractionExecutionStatus,
)
from aws_document_extraction_platform_api_python_runtime.models.status_transition import StatusTransition
from aws_document_extraction_platform_api_python_runtime.models.document_metadata import DocumentMetadata

from aws_document_extraction_platform_lib.api.utils.api import CallingUserDict, _get_caller
from aws_document_extraction_platform_lib.ingestion_state_machine.classify_forms import ClassifiedForm
from aws_document_extraction_platform_lib.ingestion_state_machine.split_document import (
    ClassifiedSplitForm,
)
from aws_document_extraction_platform_lib.utils.ddb.form_metadata_store import FormMetadataStore
from aws_document_extraction_platform_lib.utils.ddb.document_metadata_store import DocumentMetadataStore
from aws_document_extraction_platform_lib.utils.ddb.form_schema_store import FormSchemaStore
from aws_document_extraction_platform_lib.utils.logger import get_logger
from aws_document_extraction_platform_lib.utils.s3.location import (
    get_document_key,
    get_file_name_from_document_key,
)
from aws_document_extraction_platform_lib.utils.time import utc_now
from aws_document_extraction_platform_lib.utils.metrics.metrics import metric_publisher
from aws_document_extraction_platform_api_python_runtime.api_client import JSONEncoder
from aws_document_extraction_platform_lib.utils.pdf import read_pdf_from_s3


class SaveClassifiedFormsInput(TypedDict):
    document_id: str
    schema_id: str
    document_location: S3Location
    caller: CallingUserDict


# https://github.com/python/mypy/issues/6462 - mypy doesn't follow the types for 'update' which is used in the ** below...
@no_type_check
def _handle_processed_form(
    document_id: str,
    form_id: str,
    document_location: S3Location,
    form: ClassifiedForm,
) -> ClassifiedSplitForm:
    """
    Take the pages from the document that were classified as the given form, and write to s3 as a new pdf
    """
    form_location: S3Location = {
        "bucket": document_location["bucket"],
        "objectKey": get_document_key(
            document_id,
            get_file_name_from_document_key(document_location["objectKey"]),
        ),
    }

    return {
        **form,
        "document_id": document_id,
        "form_id": form_id,
        "location": form_location,
    }


def handler(event: SaveClassifiedFormsInput, context):
    """
    Handler for saving the classified forms metadata information to dynamodb
    """
    form_store = FormMetadataStore()
    document_store = DocumentMetadataStore()
    schema_store = FormSchemaStore()

    document_id = event["document_id"]
    schema_id = event["schema_id"]
    caller = _get_caller(event)
    username = caller.username

    document = document_store.get_document_metadata(document_id)

    if document is None:
        raise Exception("No document found with id {}".format(document_id))

    document_dict = JSONEncoder().default(document)

    schemas: Dict[str, FormSchema] = {}

    document_location = event["document_location"]

    document_pdf = read_pdf_from_s3(
        document_location["bucket"], document_location["objectKey"]
    )

    document_dict["numberOfPages"] = document_pdf.numPages

    classified_forms: List[ClassifiedSplitForm] = []
    processed_forms: List[ClassifiedSplitForm] = []

    classified_forms.append(
        ClassifiedSplitForm(
            document_id=document_id,
            form_id="{}_{}".format(schema_id.replace(" ", "_"), 0),
            location=S3Location(
                bucket=event["document_location"]["bucket"],
                objectKey=event["document_location"]["objectKey"],
            ),
            start_page=0,
            end_page=document_pdf.numPages - 1,
            schema_id=schema_id,
        )
    )

    for i in range(0, len(classified_forms)):
        form = classified_forms[i]

        schema = (
            schemas[form["schema_id"]]
            if form["schema_id"] in schemas
            else schema_store.get_form_schema(form["schema_id"])
        )
        if schema is None:
            raise Exception("No schema found with id {}".format(form["schema_id"]))
        schemas[form["schema_id"]] = schema

        form_store.put_form_metadata(
            username,
            FormMetadata(
                documentId=document_id,
                documentName=document_dict["name"],
                formId=form["form_id"],
                schemaId=form["schema_id"],
                startPageIndex=form["start_page"],
                endPageIndex=form["end_page"],
                numberOfPages=form["end_page"]
                - form["start_page"]
                + 1,  # Start/end page indices are inclusive so add 1 for total pages
                location=S3Location(
                    bucket=form["location"]["bucket"],
                    objectKey=form["location"]["objectKey"],
                ),
                extractionExecution=ExtractionExecution(
                    status=ExtractionExecutionStatus("NOT_STARTED"),
                    executionId="not_started_yet",
                ),
                # Store a snapshot of the schema at the time of extraction, since these may evolve over time
                schemaSnapshot=schema["schema"],
                statusTransitionLog=[
                    StatusTransition(
                        timestamp=utc_now(),
                        status="CLASSIFICATION_SUCCEEDED",
                        actingUser=username,
                    )
                ],
            ),
        )

        processed_forms.append(
            _handle_processed_form(document_id, form["form_id"], form["location"], form)
        )

    # Update the ingestion status to success
    document_dict["ingestionExecutionStatus"] = ExecutionStatus("SUCCEEDED")
    document_dict["numberOfClassifiedForms"] = len(classified_forms)

    status_transition_log = list(document_dict["statusTransitionLog"])
    status_transition_log.append(
        StatusTransition(
            timestamp=utc_now(),
            status="CLASSIFICATION_SUCCEEDED",
            actingUser=username,
        )
    )
    document_dict["statusTransitionLog"] = status_transition_log

    new_document = DocumentMetadata(**document_dict)

    document_store.put_document_metadata(username, new_document)

    # Write the classification time metrics
    with metric_publisher() as m:
        m.add_classification_time(new_document)
        m.add_document_count(new_document)

    return {"forms": processed_forms}
