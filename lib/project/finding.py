from dataclasses import dataclass
from pathlib import Path
from typing import Any
from enum import Enum


class Severity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True, init=False)
class ProjectFinding:
    rule_id: str
    message: str
    file: Path
    severity: Severity
    category: str
    item: Any | None

    def __init__(
        self,
        rule_id: str | None = None,
        *,
        kind: str | None = None,
        message: str,
        file: Path,
        severity: Severity = Severity.WARNING,
        category: str = "general",
        item: Any | None = None,
    ):
        object.__setattr__(self, "rule_id", rule_id or kind)
        object.__setattr__(self, "message", message)
        object.__setattr__(self, "file", file)
        object.__setattr__(self, "severity", severity)
        object.__setattr__(self, "category", category)
        object.__setattr__(self, "item", item)

    @property
    def kind(self) -> str:
        return self.rule_id
