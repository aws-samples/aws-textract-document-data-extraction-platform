import pytest

from aws_document_extraction_platform_lib.example import hello

@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("A. Musing", "Hello A. Musing!"),
        ("traveler", "Hello traveler!"),
        ("projen developer", "Hello projen developer!"),
    ],
)
def test_hello(name, expected):
    """Example test with parametrization."""
    assert hello(name) == expected
