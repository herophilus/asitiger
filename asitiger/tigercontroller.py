import time
from typing import Dict, List, Union

from asitiger.axis import Axis
from asitiger.command import Command
from asitiger.errors import Errors
from asitiger.serialconnection import SerialConnection
from asitiger.status import statuses_for_rdstat


class TigerController:

    DEFAULT_POLL_INTERVAL_S = 0.01

    def __init__(
        self,
        serial_connection: SerialConnection,
        poll_interval_s: float = DEFAULT_POLL_INTERVAL_S,
    ):
        self.connection = serial_connection
        self.poll_interval_s = poll_interval_s

    @classmethod
    def from_serial_port(
        cls, port: str, baud_rate: int = 115200, *tiger_args, **tiger_kwargs
    ) -> "TigerController":
        return cls(SerialConnection(port, baud_rate), *tiger_args, **tiger_kwargs)

    def send_command(self, command: str) -> str:
        self.connection.send_command(command)
        response = self.connection.read_response()

        Errors.raise_error_if_present(command, response)

        return response

    @staticmethod
    def _cast_number(number_str: str):
        try:
            return int(number_str)
        except ValueError:
            return float(number_str)

    def is_busy(self) -> bool:
        return self.send_command(Command.STATUS) == "B"

    def wait_until_idle(self, poll_interval_s: float = None):
        poll_interval_s = poll_interval_s if poll_interval_s else self.poll_interval_s

        while self.is_busy():
            time.sleep(poll_interval_s)

    def home(self, axes: List[str]) -> str:
        return self.send_command(f"{Command.HOME} {' '.join(axes)}")

    def move(self, coordinates: Dict[str, float]):
        return self.send_command(Command.format(Command.MOVE, coordinates=coordinates))

    def move_relative(self, offsets: Dict[str, float]):
        axes = list(offsets.keys())
        current_location = self.where(axes)

        new_location = {
            axis: float(current_location[axis]) + offsets[axis] for axis in axes
        }

        self.move(new_location)

    def led(self, led_brightnesses: Dict[str, int], card_address: int = None):
        self.send_command(
            Command.format(
                Command.LED, coordinates=led_brightnesses, card_address=card_address
            )
        )

    def where(self, axes: List[str]) -> dict:
        response = self.send_command(f"{Command.WHERE} {' '.join(axes)}")
        coordinates = response.split(" ")[1:]

        return {
            axis: self._cast_number(coord) for axis, coord in zip(axes, coordinates)
        }

    def who(self) -> List[str]:
        return self.send_command(Command.WHO.value).split("\r")

    def set_home(self, axes: Dict[str, Union[str, int]]) -> str:
        return self.send_command(
            Command.format(Command.SETHOME, coordinates=axes, flag_overrides=["+"])
        )

    def here(self, coordinates: Dict[str, float]) -> str:
        return self.send_command(Command.format(Command.HERE, coordinates=coordinates))

    def build(self, card_address: int = None) -> List[str]:
        response = self.send_command(
            Command.format(f"{Command.BUILD} X", card_address=card_address)
        )
        return response.split("\r")

    def axes(self, card_address: int = None):
        return Axis.get_axes_from_build(self.build(card_address=card_address))

    def rdstat(self, axes: List[str]):
        response = self.send_command(f"{Command.RDSTAT} {' '.join(axes)}")
        return statuses_for_rdstat(response)
