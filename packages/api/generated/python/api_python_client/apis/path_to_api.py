import typing

from api_python_client.paths import PathValues
from api_python_client.apis.paths.tags import Tags
from api_python_client.apis.paths.sources_document import SourcesDocument
from api_python_client.apis.paths.documents_upload_url import DocumentsUploadUrl
from api_python_client.apis.paths.documents import Documents
from api_python_client.apis.paths.documents_document_id import DocumentsDocumentId
from api_python_client.apis.paths.documents_document_id_forms import DocumentsDocumentIdForms
from api_python_client.apis.paths.forms import Forms
from api_python_client.apis.paths.documents_document_id_forms_form_id import DocumentsDocumentIdFormsFormId
from api_python_client.apis.paths.documents_document_id_forms_form_id_status import DocumentsDocumentIdFormsFormIdStatus
from api_python_client.apis.paths.documents_document_id_forms_form_id_review import DocumentsDocumentIdFormsFormIdReview
from api_python_client.apis.paths.schemas import Schemas
from api_python_client.apis.paths.schemas_schema_id import SchemasSchemaId
from api_python_client.apis.paths.metrics import Metrics

PathToApi = typing.TypedDict(
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
