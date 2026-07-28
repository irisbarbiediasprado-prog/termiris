from dataclasses import dataclass
from enum import Enum, auto

class ResourceType(Enum):
    FILE = auto()
    TREE = auto()
    SEARCH = auto()

class ProtocolNode: pass

@dataclass(frozen=True)
class BootstrapNode(ProtocolNode): pass

@dataclass(frozen=True)
class RetrieveNode(ProtocolNode):
    resource_type: ResourceType
    target: str

@dataclass(frozen=True)
class InvalidNode(ProtocolNode):
    raw: str
    reason: str

