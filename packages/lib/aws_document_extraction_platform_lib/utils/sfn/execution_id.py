#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from aws_document_extraction_platform_lib.utils.base64 import (
    base64_decode,
    base64_encode,
)


def arn_to_execution_id(execution_arn: str) -> str:
    return base64_encode(execution_arn)


def execution_id_to_arn(execution_id: str) -> str:
    return base64_decode(execution_id)
