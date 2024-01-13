#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from typing import Any

from aws_document_extraction_platform_lib.utils.api import get_caller


def identity_interceptor(input: Any) -> Any:
    input.interceptor_context["AuthenticatedUser"] = get_caller(input.event)
    return input.chain.next(input)
