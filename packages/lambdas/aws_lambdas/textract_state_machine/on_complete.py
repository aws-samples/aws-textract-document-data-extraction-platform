#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from typing import TypedDict, List, Any
import json
import boto3
import os


class TextractSnsMessage(TypedDict):
    Message: str
    TopicArn: str


class TextractSnsEvent(TypedDict):
    Sns: TextractSnsMessage


class TextractSnsEvents(TypedDict):
    Records: List[TextractSnsEvent]


def get_task_token(sfn, execution_id: str, sns_topic_arn: str):
    """
    Return the task token for the textract execution that just completed
    """
    execution_arn = "{}:{}".format(
        os.environ["STATE_MACHINE_ARN"].replace(":stateMachine:", ":execution:"),
        execution_id,
    )

    events = sfn.get_execution_history(executionArn=execution_arn)["events"]

    # Find the scheduled event
    for i in range(0, len(events)):
        event = events[i]

        if event["type"] == "TaskScheduled" and "parameters" in event.get(
            "taskScheduledEventDetails", {}
        ):
            parameters = json.loads(event["taskScheduledEventDetails"]["parameters"])
            payload = parameters.get("Payload", {})

            if (
                payload.get("sns_topic_arn") == sns_topic_arn
                and "task_token" in payload
            ):
                return payload["task_token"]

    # Stop the execution to avoid indefinitely waiting if there's an unexpected error
    sfn.stop_execution(
        executionArn=execution_arn,
        error="Unable to find task token",
        cause="This indicates a problem with the code in the on_complete handler, or the cdk definition for this state machine",
    )


def handler(event: TextractSnsEvents, context: Any):
    """
    Handler called when a textract job is completed
    """
    sfn = boto3.client("stepfunctions")

    for i in range(0, len(event["Records"])):
        sns_event = event["Records"][i]["Sns"]
        textract_job_string = sns_event["Message"]
        textract_job = json.loads(textract_job_string)

        task_token = get_task_token(sfn, textract_job["JobTag"], sns_event["TopicArn"])

        # Indicate to the state machine that the textract job has succeeded or failed
        if textract_job["Status"] == "SUCCEEDED":
            sfn.send_task_success(taskToken=task_token, output=textract_job_string)
        else:
            sfn.send_task_failure(
                taskToken=task_token,
                error=textract_job.get("StatusMessage", textract_job["Status"]),
            )
