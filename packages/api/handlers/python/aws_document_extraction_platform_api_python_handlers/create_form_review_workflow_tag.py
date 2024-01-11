from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_api_python_handlers.interceptors import DEFAULT_INTERCEPTORS
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import LoggingInterceptor
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    create_form_review_workflow_tag_handler, CreateFormReviewWorkflowTagRequest, CreateFormReviewWorkflowTagOperationResponses
)


def create_form_review_workflow_tag(input: CreateFormReviewWorkflowTagRequest, **kwargs) -> CreateFormReviewWorkflowTagOperationResponses:
    """
    Type-safe handler for the CreateFormReviewWorkflowTag operation
    """
    LoggingInterceptor.get_logger(input).info("Start CreateFormReviewWorkflowTag Operation")

    # TODO: Implement CreateFormReviewWorkflowTag Operation. `input` contains the request input

    return Response.internal_failure(InternalFailureErrorResponseContent(
        message="Not Implemented!"
    ))


# Entry point for the AWS Lambda handler for the CreateFormReviewWorkflowTag operation.
# The create_form_review_workflow_tag_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = create_form_review_workflow_tag_handler(interceptors=DEFAULT_INTERCEPTORS)(create_form_review_workflow_tag)

