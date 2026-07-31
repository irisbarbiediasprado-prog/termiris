from analysis.finding import Finding
from .operations import ReplaceImportOperation
from .rules import MigrationRule

class OperationGenerator:
    def __init__(self, rules=None):
        self.rules = rules or []

    def generate(self, finding: Finding):
        for rule in self.rules:
            if (
                finding.kind == "LegacyImportMatcher"
                and finding.item.module == rule.source
            ):
                return ReplaceImportOperation(
                    kind="replace_import",
                    reference=finding.item.module,
                    old_module=rule.source,
                    new_module=rule.target,
                )
        return None
