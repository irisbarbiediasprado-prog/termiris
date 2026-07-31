from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict

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

