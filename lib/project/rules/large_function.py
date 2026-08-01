from typing import Iterable
from project.diagnostic_rule import DiagnosticRule
from project.analysis import ProjectAnalysis
from project.finding import ProjectFinding, Severity

DEFAULT_MAX_PARAMETERS = 5

class LargeFunctionRule(DiagnosticRule):
    def __init__(self, max_parameters: int = DEFAULT_MAX_PARAMETERS):
        self.max_parameters = max_parameters

    def run(self, analysis: ProjectAnalysis) -> Iterable[ProjectFinding]:
        for fa in analysis.files:
            for func in fa.index.functions:
                if len(func.parameters) > self.max_parameters:
                    yield ProjectFinding(
                        rule_id="large_function",
                        message=f"Function '{func.name}' has {len(func.parameters)} parameters (max {self.max_parameters})",
                        file=fa.source.path,
                        severity=Severity.WARNING,
                        category="complexity",
                        item=func,
                    )
