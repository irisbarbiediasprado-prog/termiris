import pytest

from protocol.executor import Executor
from protocol.executor_registry import ExecutorRegistry


class FakeExecutor(Executor):
    def execute(self, operation):
        return operation


def test_executor_registry_accepts_valid_executor():
    registry = ExecutorRegistry()
    registry.register("fake", FakeExecutor())

    assert isinstance(registry.resolve("fake"), Executor)


def test_executor_registry_rejects_invalid_executor():
    registry = ExecutorRegistry()

    with pytest.raises(TypeError):
        registry.register("invalid", object())
