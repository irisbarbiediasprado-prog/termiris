from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Any, Optional

# Estados do Ciclo de Vida do Artefato
class ArtifactStatus(Enum):
    NEW = auto()
    ACTIVE = auto()
    DORMANT = auto()
    INVALID = auto()
    EXPIRED = auto()
    TRUNCATED = auto()

@dataclass
class ArtifactState:
    """Estado mutável e operacional do artefato durante o ciclo de vida."""
    status: ArtifactStatus = ArtifactStatus.NEW
    access_count: int = 0
    token_cost: int = 0

@dataclass(frozen=True)
class ResourceReference:
    uri: str
    scheme: str = "filesystem"

@dataclass(frozen=True)
class ArtifactMetadata:
    id: str
    artifact_type: str
    priority: int

@dataclass
class Artifact:
    """Entidade agregada do Artefato."""
    metadata: ArtifactMetadata
    resource: ResourceReference
    state: ArtifactState = field(default_factory=ArtifactState)

# Objeto puro representativo da compilação de contexto
@dataclass(frozen=True)
class ContextSnapshot:
    """Representação conceitual do snapshot compilado antes da serialização."""
    generation: int
    snapshot_hash: str
    artifacts: List[Artifact]
    size_bytes: int
    timestamp: float

# Operations (Comandos do Domínio)
class OperationType(Enum):
    INGEST_ARTIFACT = auto()
    EXPIRE_ARTIFACT = auto()
    PROMOTE_ARTIFACT = auto()
    REBUILD_SNAPSHOT = auto()

@dataclass(frozen=True)
class DomainOperation:
    type: OperationType
    artifact: Optional[Artifact] = None
    payload: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class RuntimeResult:
    success: bool
    snapshot: Optional[ContextSnapshot]
    artifacts_processed: int
    warnings: List[str] = field(default_factory=list)

