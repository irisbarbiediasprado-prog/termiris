from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class MigrationPlan:
    operations: tuple[Any, ...] = ()
    metadata: dict[str, Any] | None = None
