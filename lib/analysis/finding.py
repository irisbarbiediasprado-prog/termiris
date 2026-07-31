from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Finding:
    kind: str
    message: str
    item: Any
