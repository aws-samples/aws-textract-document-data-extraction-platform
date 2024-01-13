from aws_document_extraction_platform_api_python_runtime.interceptors import (
    INTERCEPTORS,
)
from aws_document_extraction_platform_api_python_handlers.interceptors.identity import (
    identity_interceptor,
)

DEFAULT_INTERCEPTORS = [
    *INTERCEPTORS,
    identity_interceptor,
]
