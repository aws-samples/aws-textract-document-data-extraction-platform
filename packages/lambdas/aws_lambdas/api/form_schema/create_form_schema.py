#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from api_python_client.apis.tags.default_api_operation_config import (
    create_form_schema_handler,
    CreateFormSchemaRequest,
)
from api_python_client.model.form_schema import FormSchema
from api_python_client.model.api_error import ApiError

from aws_lambdas.api.utils.api import api, CallingUser, DefaultCallingUser
from aws_lambdas.api.utils.response import Response, ApiResponse
from aws_lambdas.utils.ddb.form_schema_store import FormSchemaStore
from aws_lambdas.utils.misc import copy_defined_keys

# import debugpy
# debugpy.listen(5678)
# print("waiting for response from debugger")
# debugpy.wait_for_client()
# print("attached!")


@api
@create_form_schema_handler
def handler(
    input: CreateFormSchemaRequest,
    caller: CallingUser = DefaultCallingUser,
    **kwargs,
) -> ApiResponse[FormSchema]:
    """
    Handler for creating a form schema
    """
    # Lowercase form title is used as the schema id. This allows for a fast lookup for potential matching schemas during
    # the form classification phase
    print(input)
    print(input.body)
    schema_id = input.body.title.lower()
    print("23452345345234 schema_id ", schema_id)
    print(schema_id)

    store = FormSchemaStore()
    existing_schema = store.get_form_schema(schema_id)
    print("!!!!existing schema ", existing_schema)
    if existing_schema is not None:
        return Response.bad_request(
            ApiError(message="Schema already exists with id {}".format(schema_id))
        )

    schema = FormSchemaStore().put_form_schema(
        caller.username,
        FormSchema(
            schemaId=schema_id,
            schema=input.body.schema,
            **copy_defined_keys(input.body, ["description", "title"]),
        ),
    )

    return Response.success(schema)


handler(
    {
        "headers": {"x-username": "em"},
        "queryStringParameters": None,
        "multiValueQueryStringParameters": None,
        "pathParameters": None,
        "stageVariables": None,
        "body": '{"title":"test6666","description":"some description","schema":{"properties":{"myFormField":{"order":1,"extractionMetadata":{"formKey":"Key for this form field as present in the document","tablePosition":1,"rowPosition":1,"columnPosition":1,"textractQuery":"What is my form field?"},"title":"My Form Field"}},"description":"some description"}}',
    },
    {},
)
