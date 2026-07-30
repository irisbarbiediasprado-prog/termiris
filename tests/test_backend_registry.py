import pytest

from protocol.backend_registry import BackendRegistry
from protocol.backend import Backend


class FakeBackend(Backend):
    def compile(self, plan):
        return []


def test_backend_registry_accepts_valid_backend():
    registry = BackendRegistry()
    registry.register("fake", FakeBackend())

    assert isinstance(registry.resolve("fake"), Backend)


def test_backend_registry_rejects_invalid_backend():
    registry = BackendRegistry()

    with pytest.raises(TypeError):
        registry.register("invalid", object())
