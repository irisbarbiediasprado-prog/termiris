from dataclasses import dataclass, field
from typing import Any, Dict, List

@dataclass(frozen=True)
class MigrationStep:
    action: str
    target: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    instruction: Any = None
    payload: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class MigrationPlan:
    steps: List[MigrationStep] = field(default_factory=list)
