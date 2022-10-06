#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#

from api_python_client.model.form_metadata import FormMetadata
from api_python_client.apis.tags.default_api_operation_config import (
    get_document_form_handler,
    GetDocumentFormRequest,
)
from api_python_client.model.api_error import ApiError
from api_python_client.api_client import JSONEncoder

from aws_lambdas.api.utils.api import api, identity_interceptor
from aws_lambdas.api.utils.response import Response, ApiResponse
from aws_lambdas.utils.ddb.form_metadata_store import FormMetadataStore
from aws_lambdas.utils.s3.location import get_presigned_get_url_for_pdf


@get_document_form_handler(interceptors=[identity_interceptor])
def handler(input: GetDocumentFormRequest, **kwargs) -> ApiResponse[FormMetadata]:
    """
    Handler for retrieving form metadata
    """
    document_id = input.request_parameters["documentId"]
    form_id = input.request_parameters["formId"]
    form = FormMetadataStore().get_form_metadata(document_id, form_id)
    if form is None:
        return Response.not_found(
            ApiError(
                message="No form found with id {} in document {}".format(
                    form_id, document_id
                )
            )
        )

    form_dict = JSONEncoder().default(form)
    # Add a presigned GET url
    form_dict["url"] = get_presigned_get_url_for_pdf(form["location"])
    form_dict = FormMetadata(**form_dict)
    print("form: {}".format(form_dict))
    return Response.success(form_dict)
