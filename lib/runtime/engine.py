import time
import hashlib
from typing import List
from models import DomainOperation, RuntimeResult, ContextSnapshot, Artifact, ArtifactStatus

class RuntimeEngine:
    """Runtime pragmático direto. Sem abstração especulativa de pipeline."""
    def __init__(self):
        self._active_artifacts: List[Artifact] = []
        self._generation: int = 0

    def apply(self, operation: DomainOperation) -> RuntimeResult:
        if operation.artifact:
            self._index(operation.artifact)
            self._plan(operation.artifact)
        
        snapshot = self._emit()
        return RuntimeResult(
            success=True,
            snapshot=snapshot,
            artifacts_processed=1 if operation.artifact else 0
        )

    def _index(self, artifact: Artifact) -> None:
        """Registra e marca o estado inicial."""
        artifact.state.status = ArtifactStatus.NEW
        self._active_artifacts.append(artifact)

    def _plan(self, artifact: Artifact) -> None:
        """Ordena por prioridade de forma direta."""
        artifact.state.status = ArtifactStatus.ACTIVE
        self._active_artifacts.sort(key=lambda a: a.metadata.priority, reverse=True)

    def _emit(self) -> ContextSnapshot:
        """Gera o ContextSnapshot conceitual sem preocupação com serialização física."""
        self._generation += 1
        raw_ids = "".join([a.metadata.id for a in self._active_artifacts]).encode("utf-8")
        snapshot_hash = hashlib.sha256(raw_ids).hexdigest()[:16]

        return ContextSnapshot(
            generation=self._generation,
            snapshot_hash=snapshot_hash,
            artifacts=list(self._active_artifacts),
            size_bytes=len(raw_ids),
            timestamp=time.time()
        )

