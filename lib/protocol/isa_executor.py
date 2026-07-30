from protocol.executor import Executor


class ISAExecutor(Executor):
    def __init__(self, runtime):
        self.runtime = runtime

    def execute(self, operation):
        return self.runtime.execute(operation)
