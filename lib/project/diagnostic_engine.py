from pathlib import Path
from typing import Callable, Iterable
from .analysis import ProjectAnalysis
from .diagnostic import ProjectDiagnostic
from .finding import ProjectFinding

ProjectMatcher = Callable[[object, Path], ProjectFinding | None]

class ProjectDiagnosticEngine:
    def __init__(self, matchers: Iterable[ProjectMatcher]):
        self._matchers = tuple(matchers)

    def run(self, project_analysis: ProjectAnalysis) -> ProjectDiagnostic:
        findings: list[ProjectFinding] = []
        for file_path, index in zip(project_analysis.files, project_analysis.indexes):
            for fact in index.iter_facts():
                for matcher in self._matchers:
                    finding = matcher(fact, file_path)
                    if finding is not None:
                        findings.append(finding)
        return ProjectDiagnostic(findings=tuple(findings))
