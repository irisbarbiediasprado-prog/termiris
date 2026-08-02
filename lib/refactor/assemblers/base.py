from abc import ABC, abstractmethod
from ..models import SourceFile


class Assembler(ABC):
    @abstractmethod
    def assemble(self, source_file: SourceFile) -> str:
        raise NotImplementedError
