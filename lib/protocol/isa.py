from dataclasses import dataclass
from enum import Enum, auto

class PrimitiveISA(Enum):
    READ     = auto()
    WRITE    = auto()
    SEARCH   = auto()
    LIST     = auto()
    PATCH    = auto()
    RUN      = auto()
    QUERY    = auto()
    INDEX    = auto()
    SNAPSHOT = auto()
    HELP     = auto()

@dataclass(frozen=True)
class Operation:
    instruction: PrimitiveISA
    payload: dict
