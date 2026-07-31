from protocol.default_executors import create_executor_registry
from protocol.isa_executor import ISAExecutor


class FakeRuntime:
    def execute(self, operation):
        return operation


def test_default_executor_registry():
    registry = create_executor_registry(FakeRuntime())

    executor = registry.resolve("default")

    assert isinstance(executor, ISAExecutor)
