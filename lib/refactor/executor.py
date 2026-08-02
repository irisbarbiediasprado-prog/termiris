from pathlib import Path
from .operations import (
    Operation,
    CreateFileOperation,
    CreateSourceFileOperation,
)
from .assemblers import PythonAssembler


class OperationExecutor:
    def __init__(self, assemblers=None):
        self.assemblers = assemblers or {
            "python": PythonAssembler(),
        }

    def execute(self, operation: Operation) -> Path:
        if isinstance(operation, CreateFileOperation):
            path = Path(operation.path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(operation.content)
            return path

        if isinstance(operation, CreateSourceFileOperation):
            sf = operation.source_file
            assembler = self.assemblers.get(sf.language)
            if assembler is None:
                raise ValueError(
                    f"Assembler não disponível para: {sf.language}"
                )
            content = assembler.assemble(sf)
            path = Path(sf.path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            return path

        raise NotImplementedError(
            f"Nenhum executor disponível para {type(operation).__name__}"
        )
