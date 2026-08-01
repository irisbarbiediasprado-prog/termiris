import re
from typing import Iterable
from project.diagnostic_rule import DiagnosticRule
from project.analysis import ProjectAnalysis
from project.finding import ProjectFinding
from .ids import RuleId

TODO_PATTERN = re.compile(r"\b(TODO|FIXME|HACK|XXX)\b", re.IGNORECASE)

class TodoCommentRule(DiagnosticRule):
    def run(self, analysis: ProjectAnalysis) -> Iterable[ProjectFinding]:
        for fa in analysis.files:
            for comment in fa.index.comments:
                if TODO_PATTERN.search(comment.text):
                    yield ProjectFinding(
                        rule_id=RuleId.TODO_COMMENT,
                        message=f"TODO comment: {comment.text.strip()}",
                        file=fa.source.path,
                        item=comment,
                    )
