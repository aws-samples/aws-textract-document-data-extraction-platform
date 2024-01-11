#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
import json
import boto3
from dataclasses import dataclass
from typing import Any, TypedDict

from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_lib.utils.logger import get_logger

log = get_logger(__name__)


class CallingUserDict(TypedDict):
    username: str


@dataclass
class CallingUser:
    username: str


DefaultCallingUser: CallingUser = CallingUser(username="unknown")


class UnauthorizedException(Exception):
    ...


def _get_cognito_authenticated_caller(
    cognito_authentication_provider: str,
) -> CallingUser:
    """
    Return the authenticated calling user given the authentication provider string from the IAM authorizer.
    See: https://serverless-stack.com/chapters/mapping-cognito-identity-id-and-user-pool-id.html
    """
    cognito_authentication_provider_parts = cognito_authentication_provider.split(":")
    user_sub = cognito_authentication_provider_parts[-1]
    user_pool_id = cognito_authentication_provider_parts[0].split("/")[-1]
    matching_users = boto3.client("cognito-idp").list_users(
        UserPoolId=user_pool_id, Limit=1, Filter='sub="{}"'.format(user_sub)
    )["Users"]

    if len(matching_users) == 1:
        return CallingUser(username=matching_users[0]["Username"])

    raise UnauthorizedException(
        "No user found with sub {} in pool {}".format(user_sub, user_pool_id)
    )


def _get_caller(event: Any) -> CallingUser:
    """
    Return the user making the request.
    """
    # When called via the UI, the cognitoAuthenticationProvider is set by the IAM authorizer
    if (
        "requestContext" in event
        and "identity" in event["requestContext"]
        and "cognitoAuthenticationProvider" in event["requestContext"]["identity"]
        and event["requestContext"]["identity"]["cognitoAuthenticationProvider"]
        is not None
    ):
        return _get_cognito_authenticated_caller(
            event["requestContext"]["identity"]["cognitoAuthenticationProvider"]
        )

    # The API has been called by an authenticated system using IAM credentials not issued via cognito.
    # Here we assume that this system has already verified the user that originated the request, and specified it in
    # the x-username header, otherwise defaulting to an "unknown" user.
    if "headers" in event:
        if "x-username" in event["headers"]:
            return CallingUser(username=event["headers"]["x-username"])

    return DefaultCallingUser


def identity_interceptor(input: Any) -> Any:
    input.interceptor_context["AuthenticatedUser"] = _get_caller(input.event)
    return input.chain.next(input)
