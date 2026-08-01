from typing import Iterable
from analysis.models import ImportInfo
from project.diagnostic_rule import DiagnosticRule
from project.analysis import ProjectAnalysis
from project.finding import ProjectFinding, Severity

LEGACY_IMPORT_MAP = {
    "optparse": "argparse",
    "imp": "importlib",
    "StringIO": "io",
    "cStringIO": "io",
    "urlparse": "urllib.parse",
    "urllib2": "urllib.request",
    "commands": "subprocess",
}

class LegacyImportRule(DiagnosticRule):
    def run(self, analysis: ProjectAnalysis) -> Iterable[ProjectFinding]:
        for fa in analysis.files:
            for fact in fa.index.iter_facts():
                if isinstance(fact, ImportInfo) and fact.module in LEGACY_IMPORT_MAP:
                    new_module = LEGACY_IMPORT_MAP[fact.module]
                    yield ProjectFinding(
                        rule_id="legacy_import",
                        message=f"Deprecated import: {fact.module} (use {new_module})",
                        file=fa.source.path,
                        severity=Severity.WARNING,
                        category="imports",
                        item=fact,
                    )
