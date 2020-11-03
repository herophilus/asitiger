import re
from collections import namedtuple
from enum import Enum
from typing import List, Union


class Status(Enum):
    IDLE = "N"
    BUSY = "B"

    @classmethod
    def from_flag(cls, status_flag: Union[str, int]):
        if isinstance(status_flag, int):
            return cls.IDLE if status_flag == 0 else cls.BUSY
        return Status(status_flag)


class AxisEnabledStatus(Enum):
    DISABLED = 0
    ENABLED = 1


class MotorStatus(Enum):
    INACTIVE = 0
    ACTIVE = 1


class JoystickStatus(Enum):
    DISABLED = 0
    ENABLED = 1


class RampingStatus(Enum):
    NOT_RAMPING = 0
    RAMPING = 1


class RampingDirection(Enum):
    DOWN = 0
    UP = 1


class LimitStatus(Enum):
    OPEN = 0
    CLOSED = 1


_STATUS_BYTE_BITMAP = [
    Status.from_flag,
    AxisEnabledStatus,
    MotorStatus,
    JoystickStatus,
    RampingStatus,
    RampingDirection,
    LimitStatus,
    LimitStatus,
]

AxisStatus = namedtuple(
    "AxisStatus",
    [
        "status",
        "enabled",
        "motor",
        "joystick",
        "ramping",
        "ramping_direction",
        "upper_limit",
        "lower_limit",
    ],
)


def status_from_decimal(status_byte_dec: Union[str, int]) -> AxisStatus:
    status_bits = list(map(int, f"{int(status_byte_dec):08b}"))

    statuses = [
        EnumClass(bit)
        for EnumClass, bit in zip(_STATUS_BYTE_BITMAP, reversed(status_bits))
    ]

    return AxisStatus(*statuses)


def status_for_rdstat(axis_response: str) -> Union[Status, AxisStatus]:
    try:
        return Status(axis_response)
    except ValueError:
        return status_from_decimal(axis_response)


def statuses_for_rdstat(response: str) -> List[AxisStatus]:
    # This funny business is required because the tiger controller
    # is inconsistent with its use of spaces in its responses, e.g.:
    # $ RS X Y? Z
    # :A  10N 138
    # Note there is NO space between the X and Y responses for some reason
    axis_responses = re.split(r"(\d+|[BN]|\s+)", response)
    axis_responses = " ".join(axis_responses).split()[1:]

    return list(map(status_for_rdstat, axis_responses))
