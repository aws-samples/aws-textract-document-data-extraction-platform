#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from api_python_client.api_client import JSONEncoder
from typing import TypedDict, List, Dict

from api_python_client.model.extraction_execution import ExtractionExecution
from api_python_client.model.extraction_execution_status import (
    ExtractionExecutionStatus,
)
from api_python_client.model.status_transition import StatusTransition
from api_python_client.model.form_metadata import FormMetadata
from api_python_client.model.form_json_schema import FormJSONSchema

from aws_lambdas.ingestion_state_machine.split_document import ClassifiedSplitForm
from aws_lambdas.utils.ddb.form_metadata_store import FormMetadataStore
from aws_lambdas.utils.sfn.execution_id import arn_to_execution_id
from aws_lambdas.utils.textract.queries import get_queries_from_schema
from aws_lambdas.utils.time import utc_now


class StartDataExtractionInput(TypedDict):
    form: ClassifiedSplitForm
    sfn_execution_arn: str


class StartDataExtractionOutput(TypedDict):
    textract_feature_types: List[str]
    textract_extra_args: Dict


def handler(event: StartDataExtractionInput, context) -> StartDataExtractionOutput:
    """
    Handler for state management to indicate the beginning of the form data extraction pipeline
    """

    store = FormMetadataStore()

    form = store.get_form_metadata(
        event["form"]["document_id"], event["form"]["form_id"]
    )

    if form is None:
        raise Exception(
            "No form found in document {} with id {}".format(
                event["form"]["document_id"], event["form"]["form_id"]
            )
        )
    form = JSONEncoder().default(form)

    # Mark the form data extraction as in progress
    form["extractionExecution"] = ExtractionExecution(
        status=ExtractionExecutionStatus("IN_PROGRESS"),
        executionId=arn_to_execution_id(event["sfn_execution_arn"]),
    )
    status_transition_log = list(form["statusTransitionLog"])
    status_transition_log.append(
        StatusTransition(
            timestamp=utc_now(),
            status="STARTED_EXTRACTION",
            actingUser=form["updatedBy"],
        )
    )
    form["statusTransitionLog"] = status_transition_log
    form = FormMetadata(**form)
    store.put_form_metadata(form["updatedBy"], form)

    # Find any queries we should execute based on the schema
    newSchemaSnapshot = FormJSONSchema(**(form["schemaSnapshot"]))
    schema_queries = get_queries_from_schema(newSchemaSnapshot)
    textract_feature_types = ["FORMS", "TABLES"]
    textract_extra_args = {}

    if len(schema_queries) > 0:
        textract_feature_types.append("QUERIES")
        textract_extra_args["QueriesConfig"] = {"Queries": schema_queries}

    return {
        "textract_feature_types": textract_feature_types,
        "textract_extra_args": textract_extra_args,
    }
