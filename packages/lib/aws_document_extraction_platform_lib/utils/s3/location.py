#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
import boto3
from botocore.config import Config
from typing import TypedDict
from aws_document_extraction_platform_api_python_runtime.models.s3_location import (
    S3Location as S3LocationModel,
)


class S3Location(TypedDict):
    bucket: str
    objectKey: str


def get_document_folder_key(document_id: str) -> str:
    """
    Return the s3 key for a document folder
    """
    return "documents/{}".format(document_id)


def get_document_key(document_id: str, file_name: str) -> str:
    """
    Return the s3 key for a document
    """
    return "{}/{}".format(get_document_folder_key(document_id), file_name)


def get_file_name_from_document_key(document_key: str) -> str:
    """
    Return the file name of a document given the document s3 key
    """
    return document_key.split("/")[-1]


def remove_extension(file_name: str) -> str:
    """
    Remove the file extension from a file name
    """
    return file_name.split(".")[0]


def get_form_key(document_id: str, document_file_name: str, form_id: str) -> str:
    """
    Return the s3 key for a split form within a document
    """
    return "{}/forms/{}_{}.pdf".format(
        get_document_folder_key(document_id),
        remove_extension(document_file_name),
        form_id,
    )


def get_presigned_get_url_for_pdf(location: S3LocationModel) -> str:
    """
    Return a presigned url for getting a pdf from s3
    """
    return boto3.client(
        "s3",
        config=Config(s3={"addressing_style": "virtual"}, signature_version="s3v4"),
    ).generate_presigned_url(
        "get_object",
        Params={
            "Bucket": location.bucket,
            "Key": location.object_key,
            "ResponseContentType": "application/pdf",
        },
    )
