#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from typing import TypedDict, Dict

from aws_document_extraction_platform_api_python_runtime.models.status_transition import (
    StatusTransition,
)
from aws_document_extraction_platform_api_python_runtime.models.form_metadata import (
    FormMetadata,
)

from aws_document_extraction_platform_lib.utils.sfn.errors import (
    SfnErrorDetails,
    get_sfn_error_message,
)
from aws_document_extraction_platform_lib.utils.ddb.form_metadata_store import (
    FormMetadataStore,
)
from aws_document_extraction_platform_lib.utils.time import utc_now
from aws_document_extraction_platform_lib.utils.metrics.metrics import metric_publisher
from aws_document_extraction_platform_lib.utils.logger import get_logger

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

    # Mark the document execution as failed
    form.extraction_execution.status = "FAILED"
    form.extraction_execution.status_reason = get_sfn_error_message(
        event["error_details"]
    )
    status_transition_log = list(form.status_transition_log)
    status_transition_log.append(
        StatusTransition(
            timestamp=utc_now(),
            status="EXTRACTION_FAILED",
            actingUser=form.updated_by,
        )
    )
    form.status_transition_log = status_transition_log

    form_store.put_form_metadata(form.updated_by, form)

    with metric_publisher() as m:
        m.add_form_count(form)

    return {}
