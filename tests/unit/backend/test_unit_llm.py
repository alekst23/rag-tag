import pytest

from src.ragtag.backend.llm import _format_tag

@pytest.mark.parametrize(
    "input_args, expected_output",
    [
        ("- test-val", "test-val"),
        ("test-val", "test-val"),
        (" test-val", "test-val"),
        ("test-val\n\n", "test-val")
    ]
)
def test_format_tag(input_args, expected_output):
    assert _format_tag(input_args) == expected_output