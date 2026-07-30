from protocol.isa_executor import ISAExecutor
from protocol.executor import Executor


class FakeRuntime:
    def __init__(self):
        self.received = None

    def execute(self, operation):
        self.received = operation
        return "ok"


def test_isa_executor_delegates_to_runtime():
    runtime = FakeRuntime()
    executor = ISAExecutor(runtime)

    result = executor.execute("operation")

    assert result == "ok"
    assert runtime.received == "operation"
    assert isinstance(executor, Executor)
