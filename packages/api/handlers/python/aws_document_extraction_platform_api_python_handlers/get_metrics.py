#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from typing import List
from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_lib.utils.ddb.form_schema_store import (
    FormSchemaStore,
)
from aws_document_extraction_platform_lib.utils.ddb.store import PaginationParameters
from aws_document_extraction_platform_lib.utils.metrics.metrics import Metrics
from aws_document_extraction_platform_api_python_handlers.interceptors import (
    DEFAULT_INTERCEPTORS,
)
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import (
    LoggingInterceptor,
)
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    get_metrics_handler,
    GetMetricsRequest,
    GetMetricsOperationResponses,
)


def _list_all_schemas() -> List[FormSchema]:
    """
    List all schemas in the store
    """
    store = FormSchemaStore()

    schemas: List[FormSchema] = []
    has_more_results = True
    next_token = None

    while has_more_results:
        response = store.list_all(
            PaginationParameters(page_size=100, next_token=next_token)
        )
        schemas += response.items
        next_token = response.next_token
        has_more_results = next_token is not None

    return schemas


def get_metrics(input: GetMetricsRequest, **kwargs) -> GetMetricsOperationResponses:
    """
    Type-safe handler for the GetMetrics operation
    """
    LoggingInterceptor.get_logger(input).info("Start GetMetrics Operation")

    start_timestamp = input.request_parameters.start_timestamp
    end_timestamp = input.request_parameters.end_timestamp

    schema_ids = [schema.schema_id for schema in _list_all_schemas()]

    return Response.success(
        Metrics().get_aggregate_metrics(start_timestamp, end_timestamp, schema_ids)
    )


# Entry point for the AWS Lambda handler for the GetMetrics operation.
# The get_metrics_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = get_metrics_handler(interceptors=DEFAULT_INTERCEPTORS)(get_metrics)
