from dataclasses import dataclass

@dataclass(frozen=True)
class Operation:
    kind: str
    reference: str

@dataclass(frozen=True)
class ReplaceImportOperation(Operation):
    old_module: str
    new_module: str
