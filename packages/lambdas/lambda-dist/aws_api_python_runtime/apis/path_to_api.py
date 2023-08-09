import typing_extensions

from aws_api_python_runtime.paths import PathValues
from aws_api_python_runtime.apis.paths.tags import Tags
from aws_api_python_runtime.apis.paths.sources_document import SourcesDocument
from aws_api_python_runtime.apis.paths.documents_upload_url import DocumentsUploadUrl
from aws_api_python_runtime.apis.paths.documents import Documents
from aws_api_python_runtime.apis.paths.documents_document_id import DocumentsDocumentId
from aws_api_python_runtime.apis.paths.documents_document_id_forms import DocumentsDocumentIdForms
from aws_api_python_runtime.apis.paths.forms import Forms
from aws_api_python_runtime.apis.paths.documents_document_id_forms_form_id import DocumentsDocumentIdFormsFormId
from aws_api_python_runtime.apis.paths.documents_document_id_forms_form_id_status import DocumentsDocumentIdFormsFormIdStatus
from aws_api_python_runtime.apis.paths.documents_document_id_forms_form_id_review import DocumentsDocumentIdFormsFormIdReview
from aws_api_python_runtime.apis.paths.schemas import Schemas
from aws_api_python_runtime.apis.paths.schemas_schema_id import SchemasSchemaId
from aws_api_python_runtime.apis.paths.metrics import Metrics

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.TAGS: Tags,
        PathValues.SOURCES_DOCUMENT: SourcesDocument,
        PathValues.DOCUMENTS_UPLOADURL: DocumentsUploadUrl,
        PathValues.DOCUMENTS: Documents,
        PathValues.DOCUMENTS_DOCUMENT_ID: DocumentsDocumentId,
        PathValues.DOCUMENTS_DOCUMENT_ID_FORMS: DocumentsDocumentIdForms,
        PathValues.FORMS: Forms,
        PathValues.DOCUMENTS_DOCUMENT_ID_FORMS_FORM_ID: DocumentsDocumentIdFormsFormId,
        PathValues.DOCUMENTS_DOCUMENT_ID_FORMS_FORM_ID_STATUS: DocumentsDocumentIdFormsFormIdStatus,
        PathValues.DOCUMENTS_DOCUMENT_ID_FORMS_FORM_ID_REVIEW: DocumentsDocumentIdFormsFormIdReview,
        PathValues.SCHEMAS: Schemas,
        PathValues.SCHEMAS_SCHEMA_ID: SchemasSchemaId,
        PathValues.METRICS: Metrics,
    }
)

path_to_api = PathToApi(
    {
        PathValues.TAGS: Tags,
        PathValues.SOURCES_DOCUMENT: SourcesDocument,
        PathValues.DOCUMENTS_UPLOADURL: DocumentsUploadUrl,
        PathValues.DOCUMENTS: Documents,
        PathValues.DOCUMENTS_DOCUMENT_ID: DocumentsDocumentId,
        PathValues.DOCUMENTS_DOCUMENT_ID_FORMS: DocumentsDocumentIdForms,
        PathValues.FORMS: Forms,
        PathValues.DOCUMENTS_DOCUMENT_ID_FORMS_FORM_ID: DocumentsDocumentIdFormsFormId,
        PathValues.DOCUMENTS_DOCUMENT_ID_FORMS_FORM_ID_STATUS: DocumentsDocumentIdFormsFormIdStatus,
        PathValues.DOCUMENTS_DOCUMENT_ID_FORMS_FORM_ID_REVIEW: DocumentsDocumentIdFormsFormIdReview,
        PathValues.SCHEMAS: Schemas,
        PathValues.SCHEMAS_SCHEMA_ID: SchemasSchemaId,
        PathValues.METRICS: Metrics,
    }
)
