import time
from contextlib import contextmanager
from typing import Dict

from asitiger.commands import Commands
from asitiger.serialconnection import SerialConnection


class TigerHub:

    RESP_HEADER_FAILURE = ":N"
    DEFAULT_POLL_INTERVAL_S = 0.1

    class CommandFailedError(Exception):
        pass

    def __init__(
        self,
        serial_connection: SerialConnection,
        poll_interval_s: float = DEFAULT_POLL_INTERVAL_S,
    ):
        self.connection = serial_connection
        self.poll_interval_s = poll_interval_s

    @classmethod
    def from_serial_port(
        cls, port: str, baud_rate: int, *tiger_args, **tiger_kwargs
    ) -> "TigerHub":
        return cls(SerialConnection(port, baud_rate), *tiger_args, **tiger_kwargs)

    @staticmethod
    def format_coordinates(coordinates: Dict[str, float]):
        return " ".join(
            map(lambda coord: f"{coord[0]}={coord[1]}", coordinates.items())
        )

    @contextmanager
    def with_poll_interval(self, poll_interval_s: float):
        old_poll_interval_s = self.poll_interval_s

        self.poll_interval_s = poll_interval_s
        yield
        self.poll_interval_s = old_poll_interval_s

    def send_command(self, command: str) -> str:
        self.connection.send_command(command)
        response = self.connection.read_response()

        if response.startswith(self.RESP_HEADER_FAILURE):
            raise self.CommandFailedError(
                f'Command "{command}" failed with response: {response}'
            )

        return response

    def is_busy(self) -> bool:
        return self.send_command(Commands.STATUS.value) == "B"

    def wait_until_idle(self, poll_interval_s: float = None):
        poll_interval_s = poll_interval_s if poll_interval_s else self.poll_interval_s

        while self.is_busy():
            time.sleep(poll_interval_s)

    def home(self) -> str:
        return self.send_command(Commands.HOME.value)

    def move(self, coordinates: Dict[str, float]):
        return self.send_command(
            f"{Commands.MOVE.value} {self.format_coordinates(coordinates)}"
        )
