# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from api_python_client.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    TAGS = "/tags"
    SOURCES_DOCUMENT = "/sources/document"
    DOCUMENTS_UPLOADURL = "/documents/upload-url"
    DOCUMENTS = "/documents"
    DOCUMENTS_DOCUMENT_ID = "/documents/{documentId}"
    DOCUMENTS_DOCUMENT_ID_FORMS = "/documents/{documentId}/forms"
    FORMS = "/forms"
    DOCUMENTS_DOCUMENT_ID_FORMS_FORM_ID = "/documents/{documentId}/forms/{formId}"
    DOCUMENTS_DOCUMENT_ID_FORMS_FORM_ID_STATUS = "/documents/{documentId}/forms/{formId}/status"
    DOCUMENTS_DOCUMENT_ID_FORMS_FORM_ID_REVIEW = "/documents/{documentId}/forms/{formId}/review"
    SCHEMAS = "/schemas"
    SCHEMAS_SCHEMA_ID = "/schemas/{schemaId}"
    METRICS = "/metrics"
