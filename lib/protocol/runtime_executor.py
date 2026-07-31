from protocol.executor import Executor


class RuntimeExecutor(Executor):
    def __init__(self, registry, repository, emitter, state):
        self.registry = registry
        self.repository = repository
        self.emitter = emitter
        self.state = state

    def execute(self, operation):
        executor = self.registry.resolve(operation.instruction)

        return executor.execute(
            operation,
            self.repository,
            self.emitter,
            self.state,
        )
