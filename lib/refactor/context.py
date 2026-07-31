from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class RefactorContext:
    tree: Any
    positions: Mapping | None = None
    artifacts: Mapping | None = None
