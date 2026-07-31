from typing import Iterable
from project.diagnostic_rule import DiagnosticRule
from project.analysis import ProjectAnalysis
from project.finding import ProjectFinding

MAX_LINES = 500

class LargeFileRule(DiagnosticRule):
    def run(self, analysis: ProjectAnalysis) -> Iterable[ProjectFinding]:
        for fa in analysis.files:
            if fa.source.line_count > MAX_LINES:
                yield ProjectFinding(
                    kind="large_file",
                    message=f"File exceeds {MAX_LINES} lines ({fa.source.line_count})",
                    file=fa.source.path,
                )
