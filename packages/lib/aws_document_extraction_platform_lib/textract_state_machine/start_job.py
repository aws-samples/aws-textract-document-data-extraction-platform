#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from typing import TypedDict, Any, List, Optional, Dict

from aws_document_extraction_platform_lib.utils.s3.location import S3Location

import boto3


class StartJobRequest(TypedDict):
    document_location: S3Location
    sns_topic_arn: str
    role_arn: str
    task_token: str
    execution_id: str
    feature_types: List[str]
    extra_textract_args: Dict


def handler(event: StartJobRequest, context: Any):
    """
    Handler for starting a textract job
    """
    textract_job = boto3.client("textract").start_document_analysis(
        DocumentLocation={
            "S3Object": {
                "Bucket": event["document_location"]["bucket"],
                "Name": event["document_location"]["objectKey"],
            },
        },
        FeatureTypes=event["feature_types"],
        NotificationChannel={
            "SNSTopicArn": event["sns_topic_arn"],
            "RoleArn": event["role_arn"],
        },
        # Tag the textract job with the state machine execution id which will be used to report completion
        # once textract notifies completion
        JobTag=event["execution_id"],
        **event.get("extra_textract_args", {}),
    )

    return textract_job
