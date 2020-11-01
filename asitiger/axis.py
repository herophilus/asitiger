import re
from collections import namedtuple
from enum import Enum
from typing import Dict, List


class Axis:

    AxisInfo = namedtuple("AxisInfo", ["label", "type", "address", "address_hex"])

    class Type(Enum):
        DAC = "d"
        FILTER_WHEEL = "w"
        LENS = "b"
        LOGIC = "g"
        MICRO_MIRROR = "u"
        MOTOR = "l"
        MULTI_LED = "i"
        PIEZO = "p"
        PIEZO_LINEAR = "a"
        SHUTTER = "s"
        SLIDER = "f"
        THETA = "t"
        TURRET = "o"
        UNKNOWN = "u"
        XY_MOTOR = "x"
        Z_MOTOR = "z"
        ZOOM = "m"

    @classmethod
    def get_axes_from_build(cls, build_response: List[str]) -> List[AxisInfo]:
        info = cls._make_build_info_dict(build_response)

        axes = [
            cls.AxisInfo(*axis_info)
            for axis_info in zip(
                info["Motor Axes"],
                map(cls.Type, info["Axis Types"]),
                info["Axis Addr"],
                info["Hex Addr"],
            )
        ]

        return axes

    @staticmethod
    def _make_build_info_dict(build_response: List[str]) -> Dict:
        build_info = {}

        for line in build_response:
            if ":" not in line:
                continue

            key, values_tsv = line.split(":")
            values = re.split(r"\s+", values_tsv.strip())

            build_info[key] = values

        return build_info
