import logging
from contextlib import contextmanager

import serial

LOGGER = logging.getLogger("asitiger.serialconnection")


class SerialConnection:
    def __init__(
        self,
        port: str,
        baud_rate: int,
        num_data_bits=serial.EIGHTBITS,
        num_stop_bits=serial.STOPBITS_ONE,
        read_timeout_s: float = 10.0,
    ):
        LOGGER.debug(f"Connecting to {port} at {baud_rate} baud")
        self.connection = serial.Serial(
            port=port,
            baudrate=baud_rate,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
            timeout=read_timeout_s,
        )

    @classmethod
    @contextmanager
    def connection(cls, *args, **kwargs):
        serial_connection = cls(*args, **kwargs)
        yield serial_connection
        serial_connection.disconnect()

    def reset_buffers(self):
        self.connection.reset_input_buffer()
        self.connection.reset_output_buffer()

    def send(self, data: bytes):
        self.reset_buffers()

        LOGGER.debug(f"Sending data: {data}")
        self.connection.write(data)

    def send_command(self, command: str):
        encoded_command = f"{command}\r".encode("ascii")
        self.send(encoded_command)

    def read_response(self):
        response_bytes = self.connection.readline()
        LOGGER.debug(f"Received: {response_bytes}")

        response = response_bytes.decode("ascii")

        return response.strip()

    def disconnect(self):
        LOGGER.debug("Disconnecting from serial port...")
        self.connection.close()
        LOGGER.debug("Disconnected")
