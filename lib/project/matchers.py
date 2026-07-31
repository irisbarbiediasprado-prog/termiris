from pathlib import Path
from analysis.matchers import LegacyImportMatcher
from .finding import ProjectFinding

def make_legacy_import_matcher(module: str):
    domain_matcher = LegacyImportMatcher(module)

    def match(fact: object, file_path: Path) -> ProjectFinding | None:
        if domain_matcher.matches(fact):
            return ProjectFinding(
                kind="legacy_import",
                message=f"Deprecated import: {module}",
                file=file_path,
                item=fact,
            )
        return None

    return match
