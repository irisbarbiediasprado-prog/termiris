from pathlib import Path
from analysis.models import ImportInfo
from .finding import ProjectFinding

# Mapeamento de módulos legados para substitutos modernos
LEGACY_IMPORT_MAP = {
    "optparse": "argparse",
    "imp": "importlib",
    "StringIO": "io",
    "cStringIO": "io",
    "urlparse": "urllib.parse",
    "urllib2": "urllib.request",
    "commands": "subprocess",
}

def make_legacy_import_matchers():
    """Retorna uma lista de ProjectMatchers, um para cada módulo legado."""
    matchers = []
    for old, new in LEGACY_IMPORT_MAP.items():
        def make_matcher(old=old, new=new):
            def match(fact: object, file_path: Path) -> ProjectFinding | None:
                if isinstance(fact, ImportInfo) and fact.module == old:
                    return ProjectFinding(
                        kind="legacy_import",
                        message=f"Deprecated import: {old} (use {new})",
                        file=file_path,
                        item=fact,
                    )
                return None
            return match
        matchers.append(make_matcher())
    return matchers
