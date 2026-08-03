from dataclasses import dataclass
from .models import SourceFile, Target, Transformation


@dataclass(frozen=True)
class Operation:
    kind: str
    reference: str


@dataclass(frozen=True)
class ReplaceImportOperation(Operation):
    old_module: str
    new_module: str


@dataclass(frozen=True)
class CreateFileOperation(Operation):
    path: str
    content: str = ""


@dataclass(frozen=True)
class CreateSourceFileOperation(Operation):
    source_file: SourceFile


@dataclass(frozen=True)
class UpdateOperation(Operation):
    """Atualiza um alvo com uma transformação."""
    target: Target
    transformation: Transformation
