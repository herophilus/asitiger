import pytest

from asitiger.errors import Errors


def test_success():
    Errors.raise_error_if_present("CMD", ":A")


def test_error():
    with pytest.raises(Errors.UnrecognizedAxisParameterError):
        Errors.raise_error_if_present("CMD", ":N-2")


def test_unknown_error_code():
    with pytest.raises(Errors.UnknownError):
        Errors.raise_error_if_present("CMD", ":N-123")
