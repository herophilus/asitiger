import logging
from typing import Dict, List, Union

LOGGER = logging.getLogger("asitiger.command")


class Command:
    BUILD = "BU"
    HERE = "H"
    HOME = "!"
    LED = "LED"
    MOVE = "M"
    MOVREL = "R"
    RDSTAT = "RS"
    SETHOME = "HM"
    SPEED = "S"
    STATUS = "/"
    WHERE = "W"
    WHO = "WHO"

    _NUMERAL_MAX_LENGTH = 16

    @classmethod
    def format(
        cls,
        command: str,
        coordinates: Dict[str, Union[float, str]] = None,
        flag_overrides: List[str] = None,
        card_address: int = None,
    ):
        if coordinates:
            formatted_coords = cls.format_coordinates(
                coordinates, flag_overrides=flag_overrides
            )
            command = f"{command} {formatted_coords}"

        if card_address:
            command = f"{card_address}{command}"

        return command

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

    @classmethod
    def format_coordinate(
        cls, axis: str, value: Union[str, float], flag_overrides: List[str] = None
    ) -> str:
        value_is_flag = flag_overrides and value in flag_overrides

        if value_is_flag:
            return f"{axis}{value}"

        if len(str(value)) > cls._NUMERAL_MAX_LENGTH:
            truncated_value = str(value)[: cls._NUMERAL_MAX_LENGTH]
            LOGGER.warning(
                f'Numeral "{value}" is too long for the instrument, it will be truncated to: "{truncated_value}"'
            )
            value = truncated_value

        return f"{axis}={value}"
