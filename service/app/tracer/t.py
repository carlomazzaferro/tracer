from enum import Enum
from typing import Iterable, List, Set


class ExtendedEnum(str, Enum):
    @classmethod
    def set(cls) -> Set:
        return {c.value for c in cls}

    @classmethod
    def list(cls) -> List:
        return [c.value for c in cls]

    @classmethod
    def names(cls: Iterable) -> List:
        return [c.name for c in cls]


class TraceType(ExtendedEnum):
    call = "call"
    create = "create"
    delegate_call = "delegateCall"
    reward = "reward"
    suicide = "suicide"
