from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Operation:
    kind: str
    metadata: dict[str, Any] | None = None
    reference: str | None = None
