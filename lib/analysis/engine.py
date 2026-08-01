from .finding import Finding
from project.rules.ids import RuleId


class AnalysisEngine:
    def __init__(self, matchers=None):
        self.matchers = matchers or []

    def analyze(self, index):
        findings = []

        for matcher in self.matchers:
            for item in index.iter_facts():
                if matcher.matches(item):
                    # Matchers que definem rule_id usam ele; senão, nome da classe (legado)
                    rule_id = getattr(matcher, "rule_id", matcher.__class__.__name__)
                    findings.append(
                        Finding(
                            kind=rule_id,
                            message=f"{matcher.__class__.__name__} detectou {item}",
                            item=item,
                        )
                    )

        return findings
