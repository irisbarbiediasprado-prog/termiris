from abc import ABC, abstractmethod
from typing import Dict, List

from protocol.ir import Intent, IntentKind
from protocol.isa import Operation, PrimitiveISA


class IntentCompiler(ABC):
    @abstractmethod
    def compile(self, intent: Intent) -> List[Operation]:
        raise NotImplementedError


class ReadResourceCompiler(IntentCompiler):
    def compile(self, intent: Intent) -> List[Operation]:
        subtype = intent.metadata["sub_type"]
        targets = intent.metadata["targets_list"]

        if subtype == "TREE":
            return [
                Operation(
                    instruction=PrimitiveISA.LIST,
                    payload={
                        "path": targets[0],
                    },
                )
            ]

        return [
            Operation(
                instruction=PrimitiveISA.SNAPSHOT,
                payload={
                    "action": "INJECT_RESOURCE",
                    "resource_type": subtype,
                    "targets": targets,
                },
            )
        ]


class QueryStateCompiler(IntentCompiler):
    def compile(self, intent: Intent) -> List[Operation]:
        return [
            Operation(
                instruction=PrimitiveISA.SNAPSHOT,
                payload={
                    "action": "BOOTSTRAP_GENESIS",
                    "file_path": intent.metadata["source_file"],
                },
            )
        ]


class CompilerRegistry:
    def __init__(self):
        self._registry: Dict[IntentKind, IntentCompiler] = {}

    def register(self, kind: IntentKind, compiler: IntentCompiler):
        self._registry[kind] = compiler

    def resolve(self, kind: IntentKind) -> IntentCompiler:
        try:
            return self._registry[kind]
        except KeyError:
            raise NotImplementedError(
                f"Nenhum compilador registrado para {kind}"
            )


class ProtocolCompiler:
    """
    Fachada do backend de compilação.

    Plugin -> Intent -> CompilerRegistry -> Operation
    """

    def __init__(self, registry: CompilerRegistry | None = None):
        self.registry = registry or CompilerRegistry()

        self.registry.register(
            IntentKind.READ_RESOURCE,
            ReadResourceCompiler(),
        )

        self.registry.register(
            IntentKind.QUERY_STATE,
            QueryStateCompiler(),
        )

    def compile(self, intent: Intent) -> List[Operation]:
        compiler = self.registry.resolve(intent.kind)
        return compiler.compile(intent)
