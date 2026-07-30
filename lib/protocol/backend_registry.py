from typing import Dict
from protocol.isa_backend import ISABackend


class BackendRegistry:
    def __init__(self):
        self._registry: Dict[str, object] = {}

    def register(self, name: str, backend):
        self._registry[name] = backend

    def resolve(self, name: str):
        if name not in self._registry:
            raise ValueError(f"Backend não registrado: {name}")
        return self._registry[name]


backend_registry = BackendRegistry()
backend_registry.register("default", ISABackend())
