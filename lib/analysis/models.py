from dataclasses import dataclass


@dataclass(frozen=True)
class FunctionInfo:
    name: str
    parameters: tuple[str, ...]
    line: int | None = None


@dataclass(frozen=True)
class ClassInfo:
    name: str
    line: int | None = None


@dataclass(frozen=True)
class ImportInfo:
    module: str
    alias: str | None = None


@dataclass(frozen=True)
class CallInfo:
    function: str
    line: int | None = None


@dataclass(frozen=True)
class CommentInfo:
    text: str
    line: int | None = None


@dataclass(frozen=True)
class ExceptionInfo:
    line: int | None = None
    is_bare: bool = False
