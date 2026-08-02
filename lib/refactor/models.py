from dataclasses import dataclass


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
