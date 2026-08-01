from enum import StrEnum


class RuleId(StrEnum):
    """Identificadores canônicos para todas as regras de diagnóstico."""
    LEGACY_IMPORT = "legacy_import"
    LARGE_FILE = "large_file"
    LARGE_FUNCTION = "large_function"
    TODO_COMMENT = "todo_comment"
    BARE_EXCEPT = "bare_except"
