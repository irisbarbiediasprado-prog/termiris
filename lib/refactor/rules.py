from dataclasses import dataclass


@dataclass(frozen=True)
class MigrationRule:
    source: str
    target: str
