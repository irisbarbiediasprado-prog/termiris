from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Code:
    language: str
    source: str


@dataclass(frozen=True)
class Function:
    name: str
    signature: str = "(self)"
    body: Code = Code("python", "pass")


@dataclass(frozen=True)
class Class:
    name: str
    methods: tuple[Function, ...] = ()


@dataclass(frozen=True)
class SourceFile:
    path: str
    language: str
    imports: tuple[str, ...] = ()
    declarations: tuple[Class | Function, ...] = ()


@dataclass(frozen=True)
class Target:
    """Seleção de alvo para transformações."""
    path: str  # caminho do arquivo
    symbol: str | None = None  # "OperationExecutor" ou "OperationExecutor.execute"


@dataclass(frozen=True)
class Transformation:
    """Representa uma mudança de comportamento."""
    kind: str  # "replace_body" | "add_declaration" | "replace_import"
    value: Any  # Code | Function | Class | ImportInfo
