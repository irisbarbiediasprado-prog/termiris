from protocol.executor import Executor


class ISAExecutor(Executor):
    def __init__(self, runtime=None):
        self.runtime = runtime

    def execute(self, operation):
        if self.runtime is None:
            raise RuntimeError("ISAExecutor sem runtime associado")
        return self.runtime.execute(operation)
