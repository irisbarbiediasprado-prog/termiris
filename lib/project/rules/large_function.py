from typing import Iterable
from project.diagnostic_rule import DiagnosticRule
from project.analysis import ProjectAnalysis
from project.finding import ProjectFinding
from .ids import RuleId

DEFAULT_MAX_PARAMETERS = 5

class LargeFunctionRule(DiagnosticRule):
    def __init__(self, max_parameters: int = DEFAULT_MAX_PARAMETERS):
        self.max_parameters = max_parameters

    def run(self, analysis: ProjectAnalysis) -> Iterable[ProjectFinding]:
        for fa in analysis.files:
            for func in fa.index.functions:
                if len(func.parameters) > self.max_parameters:
                    yield ProjectFinding(
                        rule_id=RuleId.LARGE_FUNCTION,
                        message=f"Function '{func.name}' has {len(func.parameters)} parameters (max {self.max_parameters})",
                        file=fa.source.path,
                        item=func,
                    )
