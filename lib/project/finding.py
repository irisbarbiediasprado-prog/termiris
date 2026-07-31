from dataclasses import dataclass
from pathlib import Path
from typing import Any

@dataclass(frozen=True)
class ProjectFinding:
    kind: str
    message: str
    file: Path
    item: Any | None = None
