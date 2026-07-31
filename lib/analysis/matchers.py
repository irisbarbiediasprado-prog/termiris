from .matcher import Matcher
from .models import ImportInfo


class LegacyImportMatcher(Matcher):
    def __init__(self, module: str):
        self.module = module

    def matches(self, item):
        return (
            isinstance(item, ImportInfo)
            and item.module == self.module
        )
