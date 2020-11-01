from typing import Dict, List, Union


class Command:
    BUILD = "BU"
    HERE = "H"
    HOME = "!"
    LED = "LED"
    MOVE = "M"
    RDSTAT = "RS"
    SETHOME = "HM"
    STATUS = "/"
    WHERE = "W"
    WHO = "WHO"

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

    @staticmethod
    def format_coordinate(
        axis: str, value: Union[str, float], flag_overrides: List[str] = None
    ) -> str:
        value_is_flag = flag_overrides and value in flag_overrides

        if value_is_flag:
            return f"{axis}{value}"

        return f"{axis}={value}"
