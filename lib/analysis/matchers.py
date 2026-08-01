from .matcher import Matcher
from .models import ImportInfo
from project.rules.ids import RuleId


class LegacyImportMatcher(Matcher):
    rule_id = RuleId.LEGACY_IMPORT  # Estável, independente do nome da classe

    def __init__(self, module: str):
        self.module = module

    def matches(self, item):
        return (
            isinstance(item, ImportInfo)
            and item.module == self.module
        )
