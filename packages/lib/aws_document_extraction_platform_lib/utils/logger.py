#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
import logging

logging.basicConfig(level=logging.INFO)


def get_logger(name: str) -> logging.Logger:
    """
    Return a logger with default config defined above
    """
    return logging.getLogger(name)
