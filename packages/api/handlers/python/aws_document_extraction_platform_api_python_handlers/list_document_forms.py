#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_lib.utils.ddb.document_metadata_store import (
    DocumentMetadataStore,
)
from aws_document_extraction_platform_lib.utils.ddb.form_metadata_store import (
    FormMetadataStore,
)
from aws_document_extraction_platform_lib.utils.ddb.store import PaginationParameters
from aws_document_extraction_platform_api_python_handlers.interceptors import (
    DEFAULT_INTERCEPTORS,
)
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import (
    LoggingInterceptor,
)
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    list_document_forms_handler,
    ListDocumentFormsRequest,
    ListDocumentFormsOperationResponses,
)


def list_document_forms(
    input: ListDocumentFormsRequest, **kwargs
) -> ListDocumentFormsOperationResponses:
    """
    Type-safe handler for the ListDocumentForms operation
    """
    LoggingInterceptor.get_logger(input).info("Start ListDocumentForms Operation")

    document_id = input.request_parameters.document_id
    document = DocumentMetadataStore().get_document_metadata(document_id)

    if document is None:
        return Response.not_found(
            ApiError(message="No document found with id {}".format(document_id))
        )

    if document.ingestion_execution.status != ExecutionStatus("SUCCEEDED"):
        return Response.bad_request(
            ApiError(
                message="Cannot retrieve forms for document with ingestion status {}".format(
                    document.ingestion_execution.status
                )
            )
        )

    response = FormMetadataStore().list_forms_in_document(
        document_id,
        PaginationParameters(
            page_size=input.request_parameters.page_size,
            next_token=input.request_parameters.next_token,
        ),
    )
    if response.error is not None:
        return Response.bad_request(ApiError(message=response.error))

    return Response.success(
        ListFormsResponse(forms=response.items, next_token=response.next_token)
    )


# Entry point for the AWS Lambda handler for the ListDocumentForms operation.
# The list_document_forms_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = list_document_forms_handler(interceptors=DEFAULT_INTERCEPTORS)(
    list_document_forms
)
