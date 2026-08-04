from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Function:
    name: str
    params: List[str] = field(default_factory=list)
    body: str = ""
    docstring: Optional[str] = None
    decorators: List[str] = field(default_factory=list)

@dataclass
class Class:
    name: str
    methods: List[Function] = field(default_factory=list)
    docstring: Optional[str] = None
    decorators: List[str] = field(default_factory=list)

@dataclass
class Import:
    module: str
    names: List[str] = field(default_factory=list)

@dataclass
class SourceFile:
    classes: List[Class] = field(default_factory=list)
    functions: List[Function] = field(default_factory=list)
    imports: List[Import] = field(default_factory=list)
