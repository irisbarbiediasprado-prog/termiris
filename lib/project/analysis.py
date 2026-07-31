from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ProjectAnalysis:
    files: tuple[Path, ...]
    indexes: tuple[Any, ...]
