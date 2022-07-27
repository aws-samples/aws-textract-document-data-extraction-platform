#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
import boto3
import json
from typing import TypedDict

from api_python_client.model.extraction_execution_status import (
    ExtractionExecutionStatus,
)
from api_python_client.model.s3_location import S3Location
from api_python_client.model.status_transition import StatusTransition

from aws_lambdas.ingestion_state_machine.split_document import ClassifiedSplitForm
from aws_lambdas.utils.textract.analysis import get_full_textract_document_analysis
from aws_lambdas.utils.ddb.form_metadata_store import FormMetadataStore
from aws_lambdas.utils.ddb.document_metadata_store import DocumentMetadataStore
from aws_lambdas.utils.textract.extraction import extract_schema_fields_from_document
from aws_lambdas.utils.s3.location import remove_extension
from aws_lambdas.utils.time import utc_now
from aws_lambdas.utils.metrics.metrics import metric_publisher
from aws_lambdas.utils.logger import get_logger

log = get_logger(__name__)


class TextractJob(TypedDict):
    JobId: str


class ExtractFormDataInput(TypedDict):
    form: ClassifiedSplitForm
    textract_job: TextractJob


def handler(event: ExtractFormDataInput, context):
    """
    Handler for extracting data from a form, given a completed textract run
    """
    # Get the textract results for the completed job
    textract_result = get_full_textract_document_analysis(
        event["textract_job"]["JobId"]
    )

    document_id = event["form"]["document_id"]
    form_id = event["form"]["form_id"]

    form_store = FormMetadataStore()
    document_store = DocumentMetadataStore()

    # Read relevant form and schema from dynamodb
    form_metadata = form_store.get_form_metadata(document_id, form_id)
    document_metadata = document_store.get_document_metadata(document_id)

    if form_metadata is None:
        raise Exception("No form found with id {}".format(form_id))
    if document_metadata is None:
        raise Exception("No document found with id {}".format(document_id))

    # Store the full textract result in s3. This is not used in the prototype but may be useful for implementing
    # "re-run" apis or testing changes to extraction logic
    form_metadata.textract_output_location = S3Location(
        bucket=form_metadata.location.bucket,
        key="{}/textract_output.json".format(
            remove_extension(form_metadata.location.key)
        ),
    )
    boto3.client("s3").put_object(
        Bucket=form_metadata.textract_output_location.bucket,
        Key=form_metadata.textract_output_location.key,
        Body=json.dumps(textract_result),
    )

    # Extract data from the document, conforming to the given schema
    extracted_data = extract_schema_fields_from_document(
        textract_result, form_metadata.schema_snapshot
    )

    log.info("Schema for extraction: %s", form_metadata.schema_snapshot.to_dict())
    log.info("Extracted data: %s", extracted_data)

    # Write the extracted data to the form table
    form_metadata.extracted_data = extracted_data.data
    form_metadata.original_extracted_data = extracted_data.data
    form_metadata.extracted_data_metadata = extracted_data.metadata
    form_metadata.average_confidence = extracted_data.average_confidence
    form_metadata.extraction_execution.status = ExtractionExecutionStatus(
        "READY_FOR_REVIEW"
    )
    form_metadata.status_transition_log.append(
        StatusTransition(
            timestamp=utc_now(),
            status="READY_FOR_REVIEW",
            acting_user=form_metadata.updated_by,
        )
    )
    form_store.put_form_metadata(form_metadata.updated_by, form_metadata)

    # Add metrics since processing has completed
    with metric_publisher() as m:
        m.add_extraction_time(form_metadata)
        m.add_processing_time(document_metadata, form_metadata)
        m.add_form_count(form_metadata)
        m.add_average_confidence(form_metadata)

    return {}
