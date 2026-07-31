from dataclasses import dataclass
from .analysis import ProjectAnalysis

@dataclass(frozen=True)
class ProjectReport:
    files_count: int
    functions_count: int
    classes_count: int
    imports_count: int
    calls_count: int

class ProjectReporter:
    def report(self, analysis: ProjectAnalysis) -> ProjectReport:
        functions_count = 0
        classes_count = 0
        imports_count = 0
        calls_count = 0
        for sfa in analysis.files:
            idx = sfa.index
            functions_count += len(idx.functions)
            classes_count += len(idx.classes)
            imports_count += len(idx.imports)
            calls_count += len(idx.calls)
        return ProjectReport(
            files_count=len(analysis.files),
            functions_count=functions_count,
            classes_count=classes_count,
            imports_count=imports_count,
            calls_count=calls_count,
        )
