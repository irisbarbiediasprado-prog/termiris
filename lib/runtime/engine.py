from pathlib import Path
from typing import List

from models import Operation, RuntimeResult, Artifact, ResourceReference
from protocol.isa import PrimitiveISA
from runtime.repository import ArtifactRepository
from runtime.emitter import SnapshotEmitter


class RuntimeEngine:
    def __init__(self, repository=None, emitter=None):
        self.repository = repository or ArtifactRepository()
        self.emitter = emitter or SnapshotEmitter()
        self._active_artifacts: List[Artifact] = []
        self._generation: int = 0

    def apply(self, operation: Operation) -> RuntimeResult:
        inst_name = (
            operation.instruction.name
            if hasattr(operation.instruction, "name")
            else str(operation.instruction)
        )

        if inst_name == "SNAPSHOT":
            return self._handle_snapshot(operation)

        return RuntimeResult(
            success=False,
            error=f"Instrução não suportada: {operation.instruction}",
        )

    def _handle_snapshot(self, operation: Operation) -> RuntimeResult:
        payload = operation.payload or {}

        # Compatibilidade: protocolo novo (targets) e legado (file_path)
        targets = list(payload.get("targets") or [])

        legacy = payload.get("file_path")
        if legacy:
            targets.append(legacy)

        for raw_path in targets:
            uri = (
                raw_path
                if "://" in raw_path
                else f"filesystem://{Path(raw_path).resolve()}"
            )

            artifact = self.repository.fetch(
                ResourceReference(uri=uri)
            )
            self._active_artifacts.append(artifact)

        self._generation += 1
        snapshot = self.emitter.emit(
            self._generation,
            self._active_artifacts,
        )

        return RuntimeResult(
            success=True,
            snapshot=snapshot,
        )
