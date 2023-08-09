#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
import os
from uuid import uuid4

import boto3
from botocore.config import Config
from aws_api_python_runtime.apis.tags.default_api_operation_config import (
    get_document_upload_url_handler,
    GetDocumentUploadUrlRequest,
)
from aws_api_python_runtime.model.s3_location import S3Location
from aws_api_python_runtime.model.api_error import ApiError
from aws_api_python_runtime.model.get_document_upload_url_response import (
    GetDocumentUploadUrlResponse,
)

from aws_lambdas.api.utils.api import api, identity_interceptor
from aws_lambdas.api.utils.response import Response, ApiResponse
from aws_lambdas.utils.s3.location import get_document_key


@get_document_upload_url_handler(interceptors=[identity_interceptor])
def handler(
    input: GetDocumentUploadUrlRequest,
    **kwargs,
) -> ApiResponse[GetDocumentUploadUrlResponse]:
    """
    Handler for getting a signed url for a document upload
    """
    document_id = str(uuid4())
    bucket = os.environ["SOURCE_DOCUMENT_BUCKET"]
    document_key = get_document_key(document_id, input.request_parameters["fileName"])

    # Other content types can be considered in the future, however splitting logic for such formats must be implemented
    if input.request_parameters["contentType"] != "application/pdf":
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
            "ContentType": input.request_parameters["contentType"],
        },
    )

    return Response.success(
        GetDocumentUploadUrlResponse(
            documentId=document_id,
            url=signed_url,
            location=S3Location(bucket=bucket, objectKey=document_key),
        )
    )
