from protocol.executor import Executor


class NoopExecutor(Executor):
    def execute(self, operation):
        return None
