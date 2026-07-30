from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict

from models import Artifact, ResourceReference, RuntimeResult
from protocol.isa import Operation, PrimitiveISA
from runtime.repository import ArtifactRepository
from runtime.emitter import SnapshotEmitter


class OperationExecutor(ABC):
    @abstractmethod
    def execute(
        self,
        operation: Operation,
        repository: ArtifactRepository,
        emitter: SnapshotEmitter,
        state: Dict,
    ) -> RuntimeResult:
        raise NotImplementedError


class SnapshotExecutor(OperationExecutor):
    def execute(
        self,
        operation: Operation,
        repository: ArtifactRepository,
        emitter: SnapshotEmitter,
        state: Dict,
    ) -> RuntimeResult:

        payload = operation.payload or {}

        targets = list(payload.get("targets") or [])

        legacy = payload.get("file_path")
        if legacy:
            targets.append(legacy)

        artifacts = state.setdefault("artifacts", [])

        for raw in targets:
            uri = raw if "://" in raw else f"filesystem://{Path(raw).resolve()}"

            artifacts.append(
                repository.fetch(
                    ResourceReference(uri=uri)
                )
            )

        state["generation"] = state.get("generation", 0) + 1

        snapshot = emitter.emit(
            state["generation"],
            artifacts,
        )

        return RuntimeResult(
            success=True,
            snapshot=snapshot,
        )


class ExecutorRegistry:
    def __init__(self):
        self._registry = {
            PrimitiveISA.SNAPSHOT: SnapshotExecutor(),
        }

    def resolve(self, instruction):
        try:
            return self._registry[instruction]
        except KeyError:
            raise NotImplementedError(
                f"Nenhum executor registrado para {instruction}"
            )
