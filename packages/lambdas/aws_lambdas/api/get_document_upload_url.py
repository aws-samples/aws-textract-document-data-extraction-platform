#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
import os
from uuid import uuid4

import boto3
from botocore.config import Config
from api_python_client.apis.tags.default_api_operation_config import (
    get_document_upload_url_handler,
    GetDocumentUploadUrlRequest,
)
from api_python_client.model.s3_location import S3Location
from api_python_client.model.api_error import ApiError
from api_python_client.model.get_document_upload_url_response import (
    GetDocumentUploadUrlResponse,
)

from aws_lambdas.api.utils.api import api
from aws_lambdas.api.utils.response import Response, ApiResponse
from aws_lambdas.utils.s3.location import get_document_key


@api
@get_document_upload_url_handler
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
        "s3", config=Config(signature_version="s3v4")
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
            document_id=document_id,
            url=signed_url,
            location=S3Location(bucket=bucket, key=document_key),
        )
    )
