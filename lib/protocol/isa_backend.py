from typing import List
from protocol.isa import Operation, PrimitiveISA
from protocol.plan import MigrationPlan
from protocol.backend import Backend

class ISABackend(Backend):
    """
    Backend puro: traduz MigrationPlan semântico para PrimitiveISA.
    Zero IO aqui - IO fica no RuntimeEngine.
    """

    SUPPORTED = {"LIST_DIRECTORY", "INJECT_RESOURCE", "BOOTSTRAP_GENESIS", "SEARCH", "RETRIEVE", "RETRIEVE_RESOURCE"}

    def validate(self, plan: MigrationPlan) -> None:
        for step in plan.steps:
            if step.action not in self.SUPPORTED:
                raise ValueError(f"Ação não suportada pelo ISABackend: {step.action}")

    def compile(self, plan: MigrationPlan) -> List[Operation]:
        self.validate(plan)
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
            elif step.action == "SEARCH":
                operations.append(
                    Operation(
                        instruction=PrimitiveISA.SEARCH,
                        payload={
                            "pattern": step.parameters.get("pattern"),
                            "root": step.parameters.get("root", "."),
                            "max_results": step.parameters.get("max_results", 200),
                            "file_types": step.parameters.get("file_types"),
                            "case_sensitive": step.parameters.get("case_sensitive", True),
                            "regex": step.parameters.get("regex", False),
                        },
                    )
                )

            elif step.action in ("RETRIEVE", "RETRIEVE_RESOURCE"):
                operations.append(
                    Operation(
                        instruction=PrimitiveISA.RETRIEVE,
                        payload={
                            "provider": step.parameters.get("provider", "FILE"),
                            "target": step.parameters.get("target", step.target),
                        },
                    )
                )

        return operations
