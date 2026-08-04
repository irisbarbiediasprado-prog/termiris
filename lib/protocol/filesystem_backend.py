from typing import List
from protocol.backend import Backend
from protocol.isa import Operation, PrimitiveISA
from protocol.plan import MigrationPlan

class FilesystemBackend(Backend):
    """
    Legado: agora também puro.
    Antes fazia os.listdir dentro do compile (IO misturado).
    Agora retorna Operation e deixa IO pro RuntimeEngine.
    """

    SUPPORTED = {"LIST_DIRECTORY"}

    def validate(self, plan: MigrationPlan) -> None:
        for step in plan.steps:
            if step.action not in self.SUPPORTED:
                raise ValueError(f"Ação não suportada pelo FilesystemBackend: {step.action}")

    def compile(self, plan: MigrationPlan) -> List[Operation]:
        self.validate(plan)
        operations = []
        for step in plan.steps:
            path = step.parameters.get("path")
            operations.append(
                Operation(
                    instruction=PrimitiveISA.LIST,
                    payload={"path": path, "backend": "filesystem"},
                )
            )
        return operations
