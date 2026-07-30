from typing import Dict

from models import RuntimeResult
from protocol.isa import Operation
from runtime.emitter import SnapshotEmitter
from runtime.executors import ExecutorRegistry
from runtime.repository import ArtifactRepository


class RuntimeEngine:
    def __init__(self, repository=None, emitter=None, registry=None):
        self.repository = repository or ArtifactRepository()
        self.emitter = emitter or SnapshotEmitter()
        self.registry = registry or ExecutorRegistry()

        self._state: Dict = {
            "generation": 0,
            "artifacts": [],
        }

    def apply(self, operation: Operation) -> RuntimeResult:
        executor = self.registry.resolve(operation.instruction)

        return executor.execute(
            operation,
            self.repository,
            self.emitter,
            self._state,
        )
