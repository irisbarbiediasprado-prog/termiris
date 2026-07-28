from dataclasses import dataclass
from typing import List
from protocol.base import ProtocolPlugin
from protocol.ir import Intent, IntentKind
from protocol.isa import Operation, PrimitiveISA

@dataclass(frozen=True)
class BootstrapAST:
    pass

class BootstrapPlugin(ProtocolPlugin):
    @property
    def command(self) -> str:
        return "BOOTSTRAP"

    def parse_ast(self, tokens: List[str]) -> BootstrapAST:
        return BootstrapAST()

    def lower_to_intent(self, ast_node: BootstrapAST) -> Intent:
        return Intent(
            kind=IntentKind.QUERY_STATE,
            target="bootstrap_repository",
            metadata={"source": "genesis"}
        )

    def lower_to_operations(self, intent: Intent) -> List[Operation]:
        return [
            Operation(
                instruction=PrimitiveISA.SNAPSHOT,
                payload={"action": "BOOTSTRAP_GENESIS"}
            )
        ]
