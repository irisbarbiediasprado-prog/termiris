from typing import Dict
from protocol.isa_backend import ISABackend
from protocol.filesystem_backend import FilesystemBackend
from protocol.backend import Backend

class BackendNotFoundError(ValueError):
    """Contrato violado: backend solicitado não existe no registry."""
    def __init__(self, name: str):
        super().__init__(f"Backend não registrado: {name}")
        self.name = name

class BackendRegistry:
    def __init__(self):
        self._registry: Dict[str, Backend] = {}

    def register(self, name: str, backend: Backend):
        if not isinstance(backend, Backend):
            raise TypeError(f"Backend inválido: {type(backend).__name__}")
        self._registry[name] = backend

    def resolve(self, name: str):
        if name not in self._registry:
            raise BackendNotFoundError(name)
        return self._registry[name]

backend_registry = BackendRegistry()
backend_registry.register("default", ISABackend())
backend_registry.register("filesystem", FilesystemBackend())
