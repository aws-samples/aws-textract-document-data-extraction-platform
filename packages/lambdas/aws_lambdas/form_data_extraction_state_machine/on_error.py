#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from api_python_client.api_client import JSONEncoder
from typing import TypedDict, Dict

from api_python_client.model.extraction_execution_status import (
    ExtractionExecutionStatus,
)
from api_python_client.model.status_transition import StatusTransition
from api_python_client.model.form_metadata import FormMetadata

from aws_lambdas.utils.sfn.errors import SfnErrorDetails, get_sfn_error_message
from aws_lambdas.utils.ddb.form_metadata_store import FormMetadataStore
from aws_lambdas.utils.time import utc_now
from aws_lambdas.utils.metrics.metrics import metric_publisher
from aws_lambdas.utils.logger import get_logger

log = get_logger(__name__)


class OnErrorInput(TypedDict):
    # Payload may have varying properties based on which step failed
    payload: Dict
    document_id: str
    form_id: str
    error_details: SfnErrorDetails


def handler(event: OnErrorInput, context):
    """
    Handler called when an error is thrown in a form data extraction state machine step
    """
    log.info("Received error event %s", event)

    document_id = event["document_id"]
    form_id = event["form_id"]

    form_store = FormMetadataStore()
    form = form_store.get_form_metadata(document_id, form_id)

    if form is None:
        raise Exception(
            "No form found in document {} with id {}".format(document_id, form_id)
        )
    form_dict = JSONEncoder().default(obj=form)

    # Mark the document execution as failed
    form_dict["extractionExecution"]["status"] = ExtractionExecutionStatus("FAILED")
    form_dict["extractionExecution"]["statusReason"] = get_sfn_error_message(
        event["error_details"]
    )
    status_transition_log = list(form_dict["statusTransitionLog"])
    status_transition_log.append(
        StatusTransition(
            timestamp=utc_now(),
            status="EXTRACTION_FAILED",
            actingUser=form_dict["updatedBy"],
        )
    )
    form_dict["statusTransitionLog"] = status_transition_log

    form_dict = FormMetadata(**form_dict)
    form_store.put_form_metadata(form_dict["updatedBy"], form_dict)

    with metric_publisher() as m:
        m.add_form_count(form_dict)

    return {}
