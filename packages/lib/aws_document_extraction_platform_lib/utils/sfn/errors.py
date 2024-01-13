#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from typing import TypedDict
import json


class SfnErrorDetails(TypedDict):
    Error: str
    Cause: str


def _error_message_from_error(error: SfnErrorDetails) -> str:
    return error.get("Error", "An unexpected error occurred")


def get_sfn_error_message(error: SfnErrorDetails) -> str:
    """
    Retrieve the most specific error message available in step function error details
    """
    try:
        cause = json.loads(error["Cause"])
        return cause.get(
            "errorMessage", cause.get("ErrorMessage", _error_message_from_error(error))
        )
    except Exception:
        return _error_message_from_error(error)
