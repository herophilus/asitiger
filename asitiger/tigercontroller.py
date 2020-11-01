import time
from typing import Dict, List, Union

from asitiger.axis import Axis
from asitiger.command import Command
from asitiger.errors import Errors
from asitiger.serialconnection import SerialConnection


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

    def set_led_brightness(
        self, led_brightnesses: Union[Dict[str, int], int], card_address: int = None
    ):

        led_coords = (
            {"X": led_brightnesses}
            if isinstance(led_brightnesses, int)
            else led_brightnesses
        )

        self.send_command(
            Command.format(
                Command.LED, coordinates=led_coords, card_address=card_address
            )
        )

    def where(self, axes: List[str]) -> dict:
        response = self.send_command(f"{Command.WHERE.value} {' '.join(axes)}")
        coordinates = response.split(" ")[1:]

        return {axis: coord for axis, coord in zip(axes, coordinates)}

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
