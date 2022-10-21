#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
import datetime
from dateutil import parser


def utc_now_datetime() -> datetime.datetime:
    """
    :return: The current utc time as a datetime with timezone information
    """
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)


def utc_now() -> str:
    """
    :return: The current utc time as an iso 8601 timestamp with timezone information
    """
    return utc_now_datetime().isoformat()


def to_datetime(timestamp: str) -> datetime.datetime:
    """
    Return the given iso 8601 timestamp as a datetime object
    """
    return parser.parse(timestamp)


def epoch_millis(timestamp: str) -> int:
    """
    Return the given iso 8601 timestamp as milliseconds from epoch
    """
    return int(to_datetime(timestamp).timestamp() * 1000)


def millis_between(from_timestamp: str, to_timestamp: str) -> int:
    """
    Return the number of milliseconds between the given times
    :param from_timestamp: the start timestamp
    :param to_timestamp: the end timestamp
    :return: milliseconds between
    """
    return epoch_millis(to_timestamp) - epoch_millis(from_timestamp)
