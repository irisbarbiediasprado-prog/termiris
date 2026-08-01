from analysis.finding import Finding
from .operations import ReplaceImportOperation
from .rules import MigrationRule

# Mapeamento estável entre rule_id e tipo de operação
RULE_ID_TO_OPERATION = {
    "legacy_import": ReplaceImportOperation,
}

class OperationGenerator:
    def __init__(self, rules=None):
        self.rules = rules or []

    def generate(self, finding: Finding):
        # Suporta tanto Finding antigo quanto ProjectFinding novo
        RULE_ALIASES = {"LegacyImportMatcher":"legacy_import"}

        rule_id = getattr(finding,"rule_id",None) or getattr(finding,"kind",None)
        rule_id = RULE_ALIASES.get(rule_id, rule_id)

        operation_type = RULE_ID_TO_OPERATION.get(rule_id)
        if operation_type is None:
            return None

        for rule in self.rules:
            if (
                rule_id == "legacy_import"
                and finding.item.module == rule.source
            ):
                return ReplaceImportOperation(
                    kind="replace_import",
                    reference=finding.item.module,
                    old_module=rule.source,
                    new_module=rule.target,
                )
        return None
