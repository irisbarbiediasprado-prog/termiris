from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectReport:
    files_count: int
    functions_count: int
    classes_count: int
    imports_count: int
    calls_count: int
