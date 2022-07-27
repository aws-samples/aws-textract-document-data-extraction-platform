# coding: utf-8

"""
    ASX Docs API

    API for ASX Docs  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""

from api_python_client.api_client import ApiClient
from api_python_client.api.default_api_endpoints.create_form_review_workflow_tag import CreateFormReviewWorkflowTag
from api_python_client.api.default_api_endpoints.create_form_schema import CreateFormSchema
from api_python_client.api.default_api_endpoints.delete_form_schema import DeleteFormSchema
from api_python_client.api.default_api_endpoints.get_document import GetDocument
from api_python_client.api.default_api_endpoints.get_document_form import GetDocumentForm
from api_python_client.api.default_api_endpoints.get_document_upload_url import GetDocumentUploadUrl
from api_python_client.api.default_api_endpoints.get_form_schema import GetFormSchema
from api_python_client.api.default_api_endpoints.get_metrics import GetMetrics
from api_python_client.api.default_api_endpoints.list_document_forms import ListDocumentForms
from api_python_client.api.default_api_endpoints.list_documents import ListDocuments
from api_python_client.api.default_api_endpoints.list_form_review_workflow_tags import ListFormReviewWorkflowTags
from api_python_client.api.default_api_endpoints.list_form_schemas import ListFormSchemas
from api_python_client.api.default_api_endpoints.list_forms import ListForms
from api_python_client.api.default_api_endpoints.submit_source_document import SubmitSourceDocument
from api_python_client.api.default_api_endpoints.update_form_review import UpdateFormReview
from api_python_client.api.default_api_endpoints.update_form_schema import UpdateFormSchema
from api_python_client.api.default_api_endpoints.update_status import UpdateStatus


class DefaultApi(
    CreateFormReviewWorkflowTag,
    CreateFormSchema,
    DeleteFormSchema,
    GetDocument,
    GetDocumentForm,
    GetDocumentUploadUrl,
    GetFormSchema,
    GetMetrics,
    ListDocumentForms,
    ListDocuments,
    ListFormReviewWorkflowTags,
    ListFormSchemas,
    ListForms,
    SubmitSourceDocument,
    UpdateFormReview,
    UpdateFormSchema,
    UpdateStatus,
    ApiClient,
):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    pass
