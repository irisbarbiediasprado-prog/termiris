from abc import ABC, abstractmethod


class TreeDriver(ABC):
    @abstractmethod
    def parse_source(self, source: str):
        raise NotImplementedError

    @abstractmethod
    def parse_file(self, path):
        raise NotImplementedError

    @abstractmethod
    def visit(self, tree, visitor):
        raise NotImplementedError

    @abstractmethod
    def transform(self, tree, transformer):
        raise NotImplementedError
