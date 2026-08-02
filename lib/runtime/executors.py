from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List

from models import Artifact, ResourceReference, RuntimeResult
from protocol.isa import Operation
from runtime.repository import ArtifactRepository
from runtime.emitter import SnapshotEmitter
from protocol.executor import Executor


class OperationExecutor(ABC):
    @abstractmethod
    def __init__(
        self,
        repository: ArtifactRepository,
        emitter: SnapshotEmitter,
        state: Dict,
    ):
        self.repository = repository
        self.emitter = emitter
        self.state = state

    def execute(self, operation: Operation) -> RuntimeResult:
        raise NotImplementedError


class SnapshotExecutor(Executor):
    def __init__(
        self,
        repository: ArtifactRepository,
        emitter: SnapshotEmitter,
        state: Dict,
    ):
        self.repository = repository
        self.emitter = emitter
        self.state = state

    def execute(self, operation: Operation) -> RuntimeResult:

        payload = operation.payload or {}

        targets = list(payload.get("targets") or [])

        legacy = payload.get("file_path")
        if legacy:
            targets.append(legacy)

        artifacts = self.state.setdefault("artifacts", [])

        for raw in targets:
            uri = raw if "://" in raw else f"filesystem://{Path(raw).resolve()}"

            artifacts.append(
                self.repository.fetch(
                    ResourceReference(uri=uri)
                )
            )

        self.state["generation"] = self.state.get("generation", 0) + 1

        snapshot = self.emitter.emit(
            self.state["generation"],
            artifacts,
        )

        return RuntimeResult(
            success=True,
            snapshot=snapshot,
        )


class ListExecutor(Executor):
    """Implementa a semântica operacional de PrimitiveISA.LIST."""
    def __init__(
        self,
        repository: ArtifactRepository,
        emitter: SnapshotEmitter,
        state: Dict,
    ):
        self.repository = repository
        self.emitter = emitter
        self.state = state

    def execute(self, operation: Operation) -> RuntimeResult:
        payload = operation.payload or {}
        raw_path = payload.get("path", ".")

        # Resolve caminho: relativo ao home do termiris ou absoluto
        path = Path(raw_path)
        if not path.exists():
            candidate = Path.home() / ".termiris" / path
            if candidate.exists():
                path = candidate
            else:
                return RuntimeResult(
                    success=False,
                    error="DIRECTORY_NOT_FOUND",
                    snapshot=None,
                )

        if not path.is_dir():
            return RuntimeResult(
                success=False,
                error="INVALID_ARGUMENT",
                snapshot=None,
            )

        # Gera conteúdo textual da árvore
        lines = []
        for entry in sorted(path.iterdir()):
            kind = "DIR" if entry.is_dir() else "FILE"
            lines.append(f"{kind}  {entry.name}")

        content = "\n".join(lines)

        artifact = Artifact(
            uri=f"filesystem://{path}",
            content=content,
            metadata={"type": "tree", "path": str(path)},
        )

        self.state["generation"] = self.state.get("generation", 0) + 1

        snapshot = self.emitter.emit(
            self.state["generation"],
            [artifact],
        )

        return RuntimeResult(
            success=True,
            snapshot=snapshot,
        )
