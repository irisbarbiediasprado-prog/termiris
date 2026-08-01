from typing import Iterable
from project.diagnostic_rule import DiagnosticRule
from project.analysis import ProjectAnalysis
from project.finding import ProjectFinding, Severity

class BareExceptRule(DiagnosticRule):
    def run(self, analysis: ProjectAnalysis) -> Iterable[ProjectFinding]:
        for fa in analysis.files:
            for exc in fa.index.exceptions:
                if exc.is_bare:
                    yield ProjectFinding(
                        rule_id="bare_except",
                        message=f"Bare except at line {exc.line}",
                        file=fa.source.path,
                        severity=Severity.WARNING,
                        category="error_handling",
                        item=exc,
                    )
