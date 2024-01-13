#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
import os
import boto3
from botocore.config import Config
from uuid import uuid4
from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_lib.utils.s3.location import get_document_key
from aws_document_extraction_platform_api_python_handlers.interceptors import (
    DEFAULT_INTERCEPTORS,
)
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import (
    LoggingInterceptor,
)
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    get_document_upload_url_handler,
    GetDocumentUploadUrlRequest,
    GetDocumentUploadUrlOperationResponses,
)


def get_document_upload_url(
    input: GetDocumentUploadUrlRequest, **kwargs
) -> GetDocumentUploadUrlOperationResponses:
    """
    Type-safe handler for the GetDocumentUploadUrl operation
    """
    LoggingInterceptor.get_logger(input).info("Start GetDocumentUploadUrl Operation")

    document_id = str(uuid4())
    bucket = os.environ["SOURCE_DOCUMENT_BUCKET"]
    document_key = get_document_key(document_id, input.request_parameters.file_name)

    # Other content types can be considered in the future, however splitting logic for such formats must be implemented
    if input.request_parameters.content_type != "application/pdf":
        return Response.bad_request(
            ApiError(message="Submitted documents must be of the PDF format")
        )

    signed_url = boto3.client(
        "s3",
        config=Config(s3={"addressing_style": "virtual"}, signature_version="s3v4"),
    ).generate_presigned_url(
        "put_object",
        Params={
            "Bucket": bucket,
            "Key": document_key,
            "ContentType": input.request_parameters.content_type,
        },
    )

    return Response.success(
        GetDocumentUploadUrlResponse(
            documentId=document_id,
            url=signed_url,
            location=S3Location(bucket=bucket, objectKey=document_key),
        )
    )


# Entry point for the AWS Lambda handler for the GetDocumentUploadUrl operation.
# The get_document_upload_url_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = get_document_upload_url_handler(interceptors=DEFAULT_INTERCEPTORS)(
    get_document_upload_url
)
