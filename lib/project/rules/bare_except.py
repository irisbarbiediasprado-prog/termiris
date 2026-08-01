from typing import Iterable
from project.diagnostic_rule import DiagnosticRule
from project.analysis import ProjectAnalysis
from project.finding import ProjectFinding
from .ids import RuleId

class BareExceptRule(DiagnosticRule):
    def run(self, analysis: ProjectAnalysis) -> Iterable[ProjectFinding]:
        for fa in analysis.files:
            for exc in fa.index.exceptions:
                if exc.is_bare:
                    yield ProjectFinding(
                        rule_id=RuleId.BARE_EXCEPT,
                        message=f"Bare except at line {exc.line}",
                        file=fa.source.path,
                        item=exc,
                    )
