from dataclasses import dataclass

@dataclass(frozen=True)
class ProjectStatistics:
    files: int
    functions: int
    classes: int
    imports: int
    calls: int
