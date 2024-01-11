import pytest
from aws_lambda_powertools import Logger

from aws_document_extraction_platform_api_python_handlers.say_hello import say_hello
from aws_document_extraction_platform_api_python_runtime.api.operation_config import (
    SayHelloRequest, SayHelloRequestParameters, SayHelloRequestBody
)


@pytest.fixture
def request_arguments():
    """
    Fixture for constructing common request arguments
    """
    return {
        "event": {},
        "context": None,
        "interceptor_context": {
            "logger": Logger(),
        },
    }


def test_say_hello_should_return_not_implemented_error(request_arguments):
    # TODO: Update the test as appropriate when you implement your handler
    response = say_hello(SayHelloRequest(
        **request_arguments,
        # request_parameters=SayHelloRequestParameters(
        #     # Add request parameters here...
        # ),
        request_parameters=None,
        
        body=None,
    ))

    assert response.status_code == 500
    assert response.body.message == "Not Implemented!"