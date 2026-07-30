from typing import List
from protocol.isa import Operation, PrimitiveISA
from protocol.plan import MigrationPlan
from protocol.backend import Backend


class ISABackend(Backend):
    """
    Backend único que traduz o MigrationPlan puramente semântico para a PrimitiveISA.
    """

    def compile(self, plan: MigrationPlan) -> List[Operation]:
        operations = []
        for step in plan.steps:
            if step.action == "LIST_DIRECTORY":
                operations.append(
                    Operation(
                        instruction=PrimitiveISA.LIST,
                        payload={"path": step.parameters.get("path")},
                    )
                )
            elif step.action == "INJECT_RESOURCE":
                operations.append(
                    Operation(
                        instruction=PrimitiveISA.SNAPSHOT,
                        payload={
                            "action": "INJECT_RESOURCE",
                            "resource_type": step.parameters.get("resource_type"),
                            "targets": step.parameters.get("targets"),
                        },
                    )
                )
            elif step.action == "BOOTSTRAP_GENESIS":
                operations.append(
                    Operation(
                        instruction=PrimitiveISA.SNAPSHOT,
                        payload={
                            "action": "BOOTSTRAP_GENESIS",
                            "file_path": step.parameters.get("file_path"),
                        },
                    )
                )
            else:
                raise ValueError(f"Ação de migração não suportada pelo ISABackend: {step.action}")
        return operations
