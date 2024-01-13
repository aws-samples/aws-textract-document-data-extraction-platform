#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from dataclasses import asdict
from aws_document_extraction_platform_lib.utils.ddb.document_metadata_store import (
    DocumentMetadataStore,
)
from aws_document_extraction_platform_lib.utils.sfn.execution_id import (
    arn_to_execution_id,
)
from aws_document_extraction_platform_lib.utils.time import utc_now
import boto3
import os
import json

from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_api_python_handlers.interceptors import (
    DEFAULT_INTERCEPTORS,
)
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import (
    LoggingInterceptor,
)
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    submit_source_document_handler,
    SubmitSourceDocumentRequest,
    SubmitSourceDocumentOperationResponses,
)


def submit_source_document(
    input: SubmitSourceDocumentRequest, **kwargs
) -> SubmitSourceDocumentOperationResponses:
    """
    Type-safe handler for the SubmitSourceDocument operation
    """
    LoggingInterceptor.get_logger(input).info("Start SubmitSourceDocument Operation")

    caller = input.interceptor_context["AuthenticatedUser"]
    document_id = input.body.document_id
    bucket = input.body.location.bucket
    document_key = input.body.location.object_key
    schema_id = input.body.schema_id

    # Check the file exists in s3
    if "Contents" not in boto3.client("s3").list_objects_v2(
        Bucket=bucket, Prefix=document_key, MaxKeys=1
    ):
        return Response.bad_request(
            ApiError(
                message="No document found in bucket {} at key {}".format(
                    bucket, document_key
                )
            )
        )

    # Start the step function state machine for document ingestion
    execution_arn = boto3.client("stepfunctions").start_execution(
        stateMachineArn=os.environ["DOCUMENT_INGESTION_STATE_MACHINE_ARN"],
        input=json.dumps(
            {
                "Payload": {
                    "DocumentId": document_id,
                    "DocumentLocation": {
                        "bucket": bucket,
                        "objectKey": document_key,
                    },
                    "CallingUser": asdict(caller),
                    "SchemaId": schema_id,
                },
            }
        ),
    )["executionArn"]

    execution_id = arn_to_execution_id(execution_arn)
    document = DocumentMetadata(
        documentId=document_id,
        name=input.body.name,
        location=S3Location(bucket=bucket, objectKey=document_key),
        ingestionExecution=IngestionExecution(
            executionId=execution_id,
            status=ExecutionStatus("SUCCEEDED"),
        ),
        statusTransitionLog=[
            StatusTransition(
                timestamp=utc_now(),
                status="CLASSIFICATION_SUCCEEDED",
                actingUser=caller.username,
            )
        ],
    )
    document = DocumentMetadataStore().put_document_metadata(caller.username, document)

    return Response.success(document)


# Entry point for the AWS Lambda handler for the SubmitSourceDocument operation.
# The submit_source_document_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = submit_source_document_handler(interceptors=DEFAULT_INTERCEPTORS)(
    submit_source_document
)
