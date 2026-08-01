from analysis.finding import Finding
from .operations import ReplaceImportOperation
from .rules import MigrationRule
from project.rules.ids import RuleId

# Compatibilidade: mapeia nomes antigos de classes para rule_ids canônicos
LEGACY_KIND_ALIASES = {
    "LegacyImportMatcher": RuleId.LEGACY_IMPORT,
}

class OperationGenerator:
    def __init__(self, rules=None):
        self.rules = rules or []

    def generate(self, finding: Finding):
        # Normaliza rule_id: prefere rule_id se existir, senão usa kind com aliases
        rule_id = getattr(finding, "rule_id", None) or finding.kind
        rule_id = LEGACY_KIND_ALIASES.get(rule_id, rule_id)

        if rule_id == RuleId.LEGACY_IMPORT:
            for rule in self.rules:
                if finding.item.module == rule.source:
                    return ReplaceImportOperation(
                        kind="replace_import",
                        reference=finding.item.module,
                        old_module=rule.source,
                        new_module=rule.target,
                    )
        return None
