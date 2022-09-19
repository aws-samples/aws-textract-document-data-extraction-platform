#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from typing import Dict, Union, Generic, TypeVar

from api_python_client.apis.tags.default_api_operation_config import (
    ApiResponse as LambdaApiResponse,
)
from api_python_client.model.api_error import ApiError

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "*",
}

ResponseBody = TypeVar("ResponseBody")

# All api responses should conform to the same error type, ApiError.
# mypy: ignore-errors
ApiResponse = LambdaApiResponse[ResponseBody, ApiError]


class Response(Generic[ResponseBody]):
    """
    A collection of helper methods to build api responses
    """

    @staticmethod
    def respond(
        status_code: int,
        body: Union[ResponseBody, ApiError],
        headers: Dict[str, str] = {},
    ) -> ApiResponse[ResponseBody]:
        return LambdaApiResponse(
            status_code=status_code, body=body, headers={**CORS_HEADERS, **headers}
        )

    @staticmethod
    def success(body: ResponseBody) -> ApiResponse[ResponseBody]:
        return Response.respond(200, body)

    @staticmethod
    def bad_request(error: ApiError) -> ApiResponse[ResponseBody]:
        return Response.respond(400, error)

    @staticmethod
    def not_authorized(error: ApiError) -> ApiResponse[ResponseBody]:
        return Response.respond(403, error)

    @staticmethod
    def not_found(error: ApiError) -> ApiResponse[ResponseBody]:
        return Response.respond(404, error)

    @staticmethod
    def internal_server_error(error: ApiError) -> ApiResponse[ResponseBody]:
        return Response.respond(500, error)
