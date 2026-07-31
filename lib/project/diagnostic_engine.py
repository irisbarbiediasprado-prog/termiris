from typing import Iterable
from .analysis import ProjectAnalysis
from .diagnostic import ProjectDiagnostic
from .diagnostic_rule import DiagnosticRule

class ProjectDiagnosticEngine:
    def __init__(self, rules: Iterable[DiagnosticRule]):
        self._rules = tuple(rules)

    def run(self, analysis: ProjectAnalysis) -> ProjectDiagnostic:
        findings = []
        for rule in self._rules:
            findings.extend(rule.run(analysis))
        return ProjectDiagnostic(findings=tuple(findings))
