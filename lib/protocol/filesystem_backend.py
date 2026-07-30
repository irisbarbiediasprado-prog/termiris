import os
from typing import List

from protocol.backend import Backend
from protocol.plan import MigrationPlan


class FilesystemBackend(Backend):
    def compile(self, plan: MigrationPlan) -> List:
        operations = []

        for step in plan.steps:
            if step.action == "LIST_DIRECTORY":
                path = step.parameters.get("path")
                operations.append({
                    "backend": "filesystem",
                    "operation": "list_directory",
                    "result": os.listdir(path),
                })
            else:
                raise ValueError(
                    f"Ação não suportada pelo FilesystemBackend: {step.action}"
                )

        return operations
