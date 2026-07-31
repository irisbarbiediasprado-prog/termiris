from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class SourceFile:
    path: Path
    line_count: int
    size: int
