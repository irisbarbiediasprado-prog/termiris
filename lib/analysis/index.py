from dataclasses import dataclass, field
from .models import (
    FunctionInfo,
    ClassInfo,
    ImportInfo,
    CallInfo,
    CommentInfo,
    ExceptionInfo,
)

@dataclass
class AnalysisIndex:
    functions: list[FunctionInfo] = field(default_factory=list)
    classes: list[ClassInfo] = field(default_factory=list)
    imports: list[ImportInfo] = field(default_factory=list)
    calls: list[CallInfo] = field(default_factory=list)
    comments: list[CommentInfo] = field(default_factory=list)
    exceptions: list[ExceptionInfo] = field(default_factory=list)

    def iter_facts(self):
        yield from self.functions
        yield from self.classes
        yield from self.imports
        yield from self.calls
        yield from self.comments
        yield from self.exceptions
