from .finding import Finding


class AnalysisEngine:
    def __init__(self, matchers=None):
        self.matchers = matchers or []

    def analyze(self, index):
        findings = []

        for matcher in self.matchers:
            for item in index.iter_facts():
                if matcher.matches(item):
                    findings.append(
                        Finding(
                            kind=getattr(matcher, "rule_id", matcher.__class__.__name__),
                            message=f"{matcher.__class__.__name__} detectou {item}",
                            item=item,
                        )
                    )

        return findings
