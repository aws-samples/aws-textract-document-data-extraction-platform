#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
import os
from dataclasses import asdict
import json

import boto3
from aws_api_python_runtime.apis.tags.default_api_operation_config import (
    submit_source_document_handler,
    SubmitSourceDocumentRequest,
)
from aws_api_python_runtime.model.execution_status import ExecutionStatus
from aws_api_python_runtime.model.ingestion_execution import IngestionExecution
from aws_api_python_runtime.model.document_metadata import DocumentMetadata
from aws_api_python_runtime.model.s3_location import S3Location
from aws_api_python_runtime.model.api_error import ApiError
from aws_api_python_runtime.model.status_transition import StatusTransition

from aws_lambdas.api.utils.api import api, identity_interceptor
from aws_lambdas.api.utils.response import Response, ApiResponse
from aws_lambdas.utils.time import utc_now
from aws_lambdas.utils.sfn.execution_id import arn_to_execution_id
from aws_lambdas.utils.ddb.document_metadata_store import DocumentMetadataStore


@submit_source_document_handler(interceptors=[identity_interceptor])
def handler(
    input: SubmitSourceDocumentRequest,
    **kwargs,
) -> ApiResponse[DocumentMetadata]:
    """
    Handler for submitting a document for ingestion
    """
    caller = input.interceptor_context["AuthenticatedUser"]
    document_id = input.body["documentId"]
    bucket = input.body["location"]["bucket"]
    document_key = input.body["location"]["objectKey"]
    schema_id = input.body["schemaId"]

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
        name=input.body["name"],
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
