from dataclasses import dataclass
from enum import Enum, auto

class IntentKind(Enum):
    READ_RESOURCE = auto()
    MUTATE_RESOURCE = auto()
    QUERY_STATE = auto()
    SEARCH = auto()
    INSPECT_PROTOCOL = auto()

@dataclass(frozen=True)
class Intent:
    kind: IntentKind
    target: str
    metadata: dict
