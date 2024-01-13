#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_lib.utils.ddb.document_metadata_store import (
    DocumentMetadataStore,
)
from aws_document_extraction_platform_lib.utils.s3.location import (
    get_presigned_get_url_for_pdf,
)
from aws_document_extraction_platform_api_python_handlers.interceptors import (
    DEFAULT_INTERCEPTORS,
)
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import (
    LoggingInterceptor,
)
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    get_document_handler,
    GetDocumentRequest,
    GetDocumentOperationResponses,
)


def get_document(input: GetDocumentRequest, **kwargs) -> GetDocumentOperationResponses:
    """
    Type-safe handler for the GetDocument operation
    """
    LoggingInterceptor.get_logger(input).info("Start GetDocument Operation")

    document_id = input.request_parameters.document_id
    document = DocumentMetadataStore().get_document_metadata(document_id)
    if document is None:
        return Response.not_found(
            ApiError(message="No document found with id {}".format(document_id))
        )

    # Add a presigned GET url
    document.url = get_presigned_get_url_for_pdf(document.location)
    return Response.success(document)


# Entry point for the AWS Lambda handler for the GetDocument operation.
# The get_document_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = get_document_handler(interceptors=DEFAULT_INTERCEPTORS)(get_document)
