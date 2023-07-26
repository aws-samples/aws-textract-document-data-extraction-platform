import typing

from api_python_client.apis.tags import TagValues
from api_python_client.apis.tags.default_api import DefaultApi

TagToApi = typing.TypedDict(
    'TagToApi',
    {
        TagValues.DEFAULT: DefaultApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.DEFAULT: DefaultApi,
    }
)
