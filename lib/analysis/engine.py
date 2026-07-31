from .finding import Finding


class AnalysisEngine:
    def __init__(self, matchers=None):
        self.matchers = matchers or []

    def analyze(self, index):
        findings = []

        items = (
            index.functions
            + index.classes
            + index.imports
            + index.calls
        )

        for matcher in self.matchers:
            for item in items:
                if matcher.matches(item):
                    findings.append(
                        Finding(
                            kind=matcher.__class__.__name__,
                            message=f"{matcher.__class__.__name__} detectou {item}",
                            item=item,
                        )
                    )

        return findings
