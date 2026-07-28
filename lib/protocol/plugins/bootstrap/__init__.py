from dataclasses import dataclass
from pathlib import Path
from typing import List
from protocol.base import ProtocolPlugin
from protocol.ir import Intent, IntentKind
from protocol.isa import Operation, PrimitiveISA

@dataclass(frozen=True)
class BootstrapAST:
    pass

class BootstrapPlugin(ProtocolPlugin):
    def __init__(self):
        # O próprio plugin define o caminho do seu recurso específico
        self.target_file = Path.home() / ".termiris" / "tp" / "bootstrap" / "000-bootstrap.card"

    @property
    def command(self) -> str:
        return "BOOTSTRAP"

    def parse_ast(self, tokens: List[str]) -> BootstrapAST:
        return BootstrapAST()

    def lower_to_intent(self, ast_node: BootstrapAST) -> Intent:
        return Intent(
            kind=IntentKind.QUERY_STATE,
            target="bootstrap_plugin",
            metadata={"source_file": str(self.target_file)}
        )

    def lower_to_operations(self, intent: Intent) -> List[Operation]:
        return [
            Operation(
                instruction=PrimitiveISA.SNAPSHOT,
                payload={
                    "action": "BOOTSTRAP_GENESIS",
                    "file_path": str(self.target_file)  # <--- O caminho exato vai direto na Operation!
                }
            )
        ]
