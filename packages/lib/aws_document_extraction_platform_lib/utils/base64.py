#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
import base64


def base64_encode(string: str) -> str:
    return base64.b64encode(bytes(string, "utf-8")).decode("utf-8")


def base64_decode(string: str) -> str:
    return base64.b64decode(bytes(string, "utf-8")).decode("utf-8")
