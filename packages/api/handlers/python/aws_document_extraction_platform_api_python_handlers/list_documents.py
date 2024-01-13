#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_lib.utils.ddb.document_metadata_store import (
    DocumentMetadataStore,
)
from aws_document_extraction_platform_lib.utils.ddb.store import PaginationParameters
from aws_document_extraction_platform_api_python_handlers.interceptors import (
    DEFAULT_INTERCEPTORS,
)
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import (
    LoggingInterceptor,
)
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    list_documents_handler,
    ListDocumentsRequest,
    ListDocumentsOperationResponses,
)


def list_documents(
    input: ListDocumentsRequest, **kwargs
) -> ListDocumentsOperationResponses:
    """
    Type-safe handler for the ListDocuments operation
    """
    LoggingInterceptor.get_logger(input).info("Start ListDocuments Operation")

    response = DocumentMetadataStore().list_all(
        PaginationParameters(
            page_size=input.request_parameters.page_size,
            next_token=input.request_parameters.next_token,
        )
    )
    if response.error is not None:
        return Response.bad_request(ApiError(message=response.error))

    return Response.success(
        ListDocumentsResponse(documents=response.items, next_token=response.next_token)
    )


# Entry point for the AWS Lambda handler for the ListDocuments operation.
# The list_documents_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = list_documents_handler(interceptors=DEFAULT_INTERCEPTORS)(list_documents)
