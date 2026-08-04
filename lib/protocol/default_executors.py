from protocol.executor_registry import ExecutorRegistry
from protocol.isa_executor import ISAExecutor
from runtime.executors import SnapshotExecutor, ListExecutor
from runtime.search_executor import SearchExecutor
from runtime.construction_executor import ConstructionExecutor
from protocol.isa import PrimitiveISA


def create_executor_registry(repository, emitter=None, state=None):
    if emitter is None and state is None:
        if hasattr(repository, "repository"):
            emitter = repository.emitter
            state = repository.state
            repository = repository.repository
        else:
            registry = ExecutorRegistry()
            registry.register("default", ISAExecutor())
            return registry

    registry = ExecutorRegistry()
    registry.register(PrimitiveISA.SNAPSHOT, SnapshotExecutor(repository, emitter, state))
    registry.register(PrimitiveISA.LIST, ListExecutor(repository, emitter, state))
    registry.register(PrimitiveISA.SEARCH, SearchExecutor(repository, emitter, state))
    registry.register(PrimitiveISA.BUILD, ConstructionExecutor(repository, emitter, state))
    return registry
