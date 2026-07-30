from abc import ABC, abstractmethod
from typing import Dict, List

from protocol.ir import Intent, IntentKind
from protocol.plan import MigrationPlan, MigrationStep
from protocol.backend_registry import backend_registry


class IntentCompiler(ABC):
    @abstractmethod
    def compile(self, intent: Intent) -> MigrationPlan:
        raise NotImplementedError


class ReadResourceCompiler(IntentCompiler):
    def compile(self, intent: Intent) -> MigrationPlan:
        subtype = intent.metadata["sub_type"]
        targets = intent.metadata["targets_list"]

        if subtype == "TREE":
            return MigrationPlan(
                steps=[
                    MigrationStep(
                        action="LIST_DIRECTORY",
                        target=targets[0],
                        parameters={"path": targets[0]},
                    )
                ]
            )

        return MigrationPlan(
            steps=[
                MigrationStep(
                    action="INJECT_RESOURCE",
                    target=targets[0] if targets else "",
                    parameters={
                        "resource_type": subtype,
                        "targets": targets,
                    },
                )
            ]
        )


class QueryStateCompiler(IntentCompiler):
    def compile(self, intent: Intent) -> MigrationPlan:
        source_file = intent.metadata["source_file"]
        return MigrationPlan(
            steps=[
                MigrationStep(
                    action="BOOTSTRAP_GENESIS",
                    target=source_file,
                    parameters={"file_path": source_file},
                )
            ]
        )


class CompilerRegistry:
    def __init__(self):
        self._registry: Dict[IntentKind, IntentCompiler] = {}

    def register(self, kind: IntentKind, compiler: IntentCompiler):
        self._registry[kind] = compiler

    def resolve(self, kind: IntentKind) -> IntentCompiler:
        return self._registry[kind]


class ProtocolCompiler:
    def __init__(self, registry=None, backend=None):
        self.registry = registry or CompilerRegistry()
        self.backend = backend or backend_registry.resolve("default")

        self.registry.register(IntentKind.READ_RESOURCE, ReadResourceCompiler())
        self.registry.register(IntentKind.QUERY_STATE, QueryStateCompiler())

    def compile(self, intent: Intent) -> List:
        compiler = self.registry.resolve(intent.kind)
        plan: MigrationPlan = compiler.compile(intent)
        return self.backend.compile(plan)
