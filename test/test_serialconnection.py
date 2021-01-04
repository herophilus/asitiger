from unittest.mock import patch

from asitiger.serialconnection import SerialConnection


@patch("asitiger.serialconnection.serial.Serial")
def test_send_command(mock_serial):
    connection = SerialConnection("/dev/ttyS01", 115200)
    serial = mock_serial.return_value

    connection.send_command("My Command")

    serial.reset_input_buffer.assert_called_once()
    serial.reset_output_buffer.assert_called_once()

    serial.write.assert_called_once_with(b"My Command\r")


@patch("asitiger.serialconnection.serial.Serial")
def test_read_response_stripped(mock_serial):
    connection = SerialConnection("/dev/ttyS01", 115200)
    serial = mock_serial.return_value

    serial.readline.return_value = b"  Some Response\r\n"

    response = connection.read_response()

    assert response == "Some Response"


@patch("asitiger.serialconnection.serial.Serial")
def test_context_manager(mock_serial):

    with SerialConnection.connection("/dev/ttyS01", 115200):
        serial = mock_serial.return_value

    serial.close.assert_called_once()
