import time
from contextlib import contextmanager
from typing import Dict, List, Union

from asitiger.axis import Axis
from asitiger.commands import Commands
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

    @staticmethod
    def format_coordinate(
        axis: str, value: Union[str, float], flag_overrides: List[str] = None
    ) -> str:
        value_is_flag = flag_overrides and value in flag_overrides

        if value_is_flag:
            return f"{axis}{value}"

        return f"{axis}={value}"

    @classmethod
    def format_coordinates(
        cls, coordinates: Dict[str, Union[float, str]], flag_overrides: List[str] = None
    ):
        return " ".join(
            map(
                lambda coord: cls.format_coordinate(
                    coord[0], coord[1], flag_overrides=flag_overrides
                ),
                coordinates.items(),
            )
        )

    @contextmanager
    def with_poll_interval(self, poll_interval_s: float):
        old_poll_interval_s = self.poll_interval_s

        self.poll_interval_s = poll_interval_s
        yield
        self.poll_interval_s = old_poll_interval_s

    @staticmethod
    def command_with_address(command: str, card_address: int = None) -> str:
        return f"{card_address}{command}" if card_address else command

    def send_command(self, command: str) -> str:
        self.connection.send_command(command)
        response = self.connection.read_response()

        Errors.raise_error_if_present(command, response)

        return response

    def is_busy(self) -> bool:
        return self.send_command(Commands.STATUS.value) == "B"

    def wait_until_idle(self, poll_interval_s: float = None):
        poll_interval_s = poll_interval_s if poll_interval_s else self.poll_interval_s

        while self.is_busy():
            time.sleep(poll_interval_s)

    def home(self, axes: List[str]) -> str:
        return self.send_command(f"{Commands.HOME.value} {' '.join(axes)}")

    def move(self, coordinates: Dict[str, float]):
        return self.send_command(
            f"{Commands.MOVE.value} {self.format_coordinates(coordinates)}"
        )

    def set_led_brightness(
        self, led_brightnesses: Union[Dict[str, int], int], card_address: int = None
    ):

        led_coords = (
            {"X": led_brightnesses}
            if isinstance(led_brightnesses, int)
            else led_brightnesses
        )
        formatted_coords = self.format_coordinates(led_coords)

        self.send_command(
            self.command_with_address(
                f"{Commands.LED.value} {formatted_coords}", card_address=card_address,
            )
        )

    def where(self, axes: List[str]) -> dict:
        response = self.send_command(f"{Commands.WHERE.value} {' '.join(axes)}")
        coordinates = response.split(" ")[1:]

        return {axis: coord for axis, coord in zip(axes, coordinates)}

    def who(self) -> List[str]:
        return self.send_command(Commands.WHO.value).split("\r")

    def set_home(self, axes: Dict[str, Union[str, int]]) -> str:
        return self.send_command(
            f"{Commands.SETHOME.value} {self.format_coordinates(axes, flag_overrides=['+'])}"
        )

    def here(self, coordinates: Dict[str, float]) -> str:
        return self.send_command(
            f"{Commands.HERE.value} {self.format_coordinates(coordinates)}"
        )

    def build(self, card_address: int = None) -> List[str]:
        response = self.send_command(
            self.command_with_address(
                f"{Commands.BUILD.value} X", card_address=card_address
            )
        )
        return response.split("\r")

    def axes(self, card_address: int = None):
        return Axis.get_axes_from_build(self.build(card_address=card_address))
