#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from typing import TypedDict, Dict

from aws_document_extraction_platform_api_python_runtime.models.status_transition import (
    StatusTransition,
)

from aws_document_extraction_platform_lib.utils.sfn.errors import (
    SfnErrorDetails,
    get_sfn_error_message,
)
from aws_document_extraction_platform_lib.utils.ddb.document_metadata_store import (
    DocumentMetadataStore,
)
from aws_document_extraction_platform_lib.utils.time import utc_now
from aws_document_extraction_platform_lib.utils.metrics.metrics import metric_publisher
from aws_document_extraction_platform_lib.utils.logger import get_logger

log = get_logger(__name__)


class OnErrorInput(TypedDict):
    # Payload may have varying properties based on which step failed
    payload: Dict
    document_id: str
    error_details: SfnErrorDetails


def handler(event: OnErrorInput, context):
    """
    Handler called when an error is thrown in a document ingestion state machine step
    """
    log.info("Received error event %s", event)

    document_id = event["document_id"]

    document_store = DocumentMetadataStore()
    document = document_store.get_document_metadata(document_id)

    if document is None:
        raise Exception("No document found with id {}".format(document_id))

    # Mark the document execution as failed
    document.ingestion_execution.status = "FAILED"
    document.ingestion_execution.status_reason = get_sfn_error_message(
        event["error_details"]
    )
    status_transition_log = list(document.status_transition_log)
    status_transition_log.append(
        StatusTransition(
            timestamp=utc_now(),
            status="CLASSIFICATION_FAILED",
            actingUser=document.updated_by,
        )
    )
    document.status_transition_log = status_transition_log

    document_store.put_document_metadata(document.updated_by, document)

    with metric_publisher() as m:
        # Publish document count metrics for this failed document, but no timing metrics
        m.add_document_count(document)

    return {}
