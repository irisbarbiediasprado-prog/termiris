import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from protocol.isa import PrimitiveISA

@dataclass(frozen=True)
class ResourceReference:
    uri: str


@dataclass
class Artifact:
    uri: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ContextSnapshot:
    generation: int
    snapshot_hash: str
    artifacts: List[Artifact]
    size_bytes: int
    timestamp: float

@dataclass
class RuntimeResult:
    success: bool
    snapshot: Optional[ContextSnapshot] = None
    error: Optional[str] = None
