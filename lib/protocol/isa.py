from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict

class PrimitiveISA(Enum):
    READ     = auto()
    WRITE    = auto()
    SEARCH   = auto()
    BUILD    = auto()
    LIST     = auto()
    PATCH    = auto()
    RUN      = auto()
    QUERY    = auto()
    INDEX    = auto()
    SNAPSHOT = auto()
    HELP     = auto()
    RETRIEVE = auto()

@dataclass(frozen=True)
class Operation:
    instruction: PrimitiveISA
    payload: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
