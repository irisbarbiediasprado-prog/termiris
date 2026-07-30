from typing import Dict

from protocol.executor import Executor


class ExecutorRegistry:
    def __init__(self):
        self._registry: Dict[str, Executor] = {}

    def register(self, name: str, executor: Executor):
        if not isinstance(executor, Executor):
            raise TypeError(f"Executor inválido: {type(executor).__name__}")
        self._registry[name] = executor

    def resolve(self, name: str) -> Executor:
        if name not in self._registry:
            raise ValueError(f"Executor não registrado: {name}")
        return self._registry[name]
