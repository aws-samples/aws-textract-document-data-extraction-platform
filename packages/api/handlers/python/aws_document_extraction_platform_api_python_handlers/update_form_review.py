from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_api_python_runtime.interceptors import INTERCEPTORS
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import LoggingInterceptor
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    update_form_review_handler, UpdateFormReviewRequest, UpdateFormReviewOperationResponses
)


def update_form_review(input: UpdateFormReviewRequest, **kwargs) -> UpdateFormReviewOperationResponses:
    """
    Type-safe handler for the UpdateFormReview operation
    """
    LoggingInterceptor.get_logger(input).info("Start UpdateFormReview Operation")

    # TODO: Implement UpdateFormReview Operation. `input` contains the request input

    return Response.internal_failure(InternalFailureErrorResponseContent(
        message="Not Implemented!"
    ))


# Entry point for the AWS Lambda handler for the UpdateFormReview operation.
# The update_form_review_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = update_form_review_handler(interceptors=INTERCEPTORS)(update_form_review)

