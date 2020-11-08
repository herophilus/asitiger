from enum import Enum
from typing import Union


class SecurePosition(Enum):
    LOCKED = 0
    UNLOCKED = 1

    @classmethod
    def resolve_value(cls, position: Union["SecurePosition", int, float]):
        if isinstance(position, cls):
            return position.value

        return position
