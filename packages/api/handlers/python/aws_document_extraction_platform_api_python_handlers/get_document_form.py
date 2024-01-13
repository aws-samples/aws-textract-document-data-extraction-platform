#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_lib.utils.ddb.form_metadata_store import (
    FormMetadataStore,
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
    get_document_form_handler,
    GetDocumentFormRequest,
    GetDocumentFormOperationResponses,
)


def get_document_form(
    input: GetDocumentFormRequest, **kwargs
) -> GetDocumentFormOperationResponses:
    """
    Type-safe handler for the GetDocumentForm operation
    """
    LoggingInterceptor.get_logger(input).info("Start GetDocumentForm Operation")

    document_id = input.request_parameters.document_id
    form_id = input.request_parameters.form_id
    form = FormMetadataStore().get_form_metadata(document_id, form_id)
    if form is None:
        return Response.not_found(
            ApiError(
                message="No form found with id {} in document {}".format(
                    form_id, document_id
                )
            )
        )

    # Add a presigned GET url
    form.url = get_presigned_get_url_for_pdf(form.location)

    return Response.success(form)


# Entry point for the AWS Lambda handler for the GetDocumentForm operation.
# The get_document_form_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = get_document_form_handler(interceptors=DEFAULT_INTERCEPTORS)(
    get_document_form
)
