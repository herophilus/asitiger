from unittest.mock import Mock

import pytest
from asitiger.tigercontroller import TigerController


@pytest.fixture(scope="function")
def tiger():
    serial_connection = Mock()
    serial_connection.read_response.return_value = ":A"

    return TigerController(serial_connection)


def test_parse_response_dict():
    assert TigerController._dict_from_response(":A X=a Y= Z=3") == {
        "X": "a",
        "Y": "",
        "Z": "3",
    }


def test_parse_response_dict_cast():
    assert TigerController._dict_from_response(
        ":A X=1 Y=2 Z=3.4", cast_values_to=float
    ) == {"X": 1, "Y": 2, "Z": 3.4}


def test_cast_number():
    assert TigerController._cast_number("1") == 1
    assert TigerController._cast_number("2.1") == 2.1


def test_send_command_error(tiger):
    tiger.connection.read_response.return_value = "response"

    assert tiger.send_command("command") == "response"


def test_send_command(tiger):
    tiger.connection.read_response.return_value = ":N-2"

    with pytest.raises(Exception):
        tiger.send_command("Nice")
