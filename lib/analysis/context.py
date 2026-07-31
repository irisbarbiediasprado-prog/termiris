from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class AnalysisContext:
    tree: Any
    positions: Mapping | None = None
    index: Any = None
