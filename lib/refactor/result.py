from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RefactorResult:
    tree: Any
    applied: tuple = ()
    failed: tuple = ()
