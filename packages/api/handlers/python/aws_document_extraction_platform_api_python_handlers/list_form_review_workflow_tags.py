from aws_document_extraction_platform_api_python_runtime.models import *
from aws_document_extraction_platform_api_python_runtime.response import Response
from aws_document_extraction_platform_api_python_runtime.interceptors import INTERCEPTORS
from aws_document_extraction_platform_api_python_runtime.interceptors.powertools.logger import LoggingInterceptor
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    list_form_review_workflow_tags_handler, ListFormReviewWorkflowTagsRequest, ListFormReviewWorkflowTagsOperationResponses
)


def list_form_review_workflow_tags(input: ListFormReviewWorkflowTagsRequest, **kwargs) -> ListFormReviewWorkflowTagsOperationResponses:
    """
    Type-safe handler for the ListFormReviewWorkflowTags operation
    """
    LoggingInterceptor.get_logger(input).info("Start ListFormReviewWorkflowTags Operation")

    # TODO: Implement ListFormReviewWorkflowTags Operation. `input` contains the request input

    return Response.internal_failure(InternalFailureErrorResponseContent(
        message="Not Implemented!"
    ))


# Entry point for the AWS Lambda handler for the ListFormReviewWorkflowTags operation.
# The list_form_review_workflow_tags_handler method wraps the type-safe handler and manages marshalling inputs and outputs
handler = list_form_review_workflow_tags_handler(interceptors=INTERCEPTORS)(list_form_review_workflow_tags)

