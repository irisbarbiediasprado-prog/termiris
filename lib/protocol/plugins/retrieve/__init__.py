from dataclasses import dataclass
from enum import Enum, auto
from typing import List
from protocol.base import ProtocolPlugin
from protocol.ir import Intent, IntentKind
from protocol.isa import Operation, PrimitiveISA

class ResourceType(Enum):
    FILE = auto()
    TREE = auto()
    SEARCH = auto()

@dataclass(frozen=True)
class RetrieveAST:
    resource_type: ResourceType
    target: str

class RetrievePlugin(ProtocolPlugin):
    @property
    def command(self) -> str:
        return "RETRIEVE"

    def parse_ast(self, tokens: List[str]) -> RetrieveAST:
        if not tokens or len(tokens) < 2:
            raise ValueError("RETRIEVE requer o tipo do recurso e o caminho (ex: << RETRIEVE FILE main.py >>)")
        
        head = tokens[0].upper()
        if head == "FILE":
            return RetrieveAST(ResourceType.FILE, tokens[1] if len(tokens) > 1 else "")
        elif head == "TREE":
            return RetrieveAST(ResourceType.TREE, tokens[1] if len(tokens) > 1 else ".")
        elif head == "SEARCH":
            return RetrieveAST(ResourceType.SEARCH, " ".join(tokens[1:]))
        else:
            # Fallback para nomes de especificações/arquivos diretos
            target = tokens[0] if tokens[0].endswith(".md") else f"{tokens[0]}.md"
            return RetrieveAST(ResourceType.FILE, target)

    def lower_to_intent(self, ast_node: RetrieveAST) -> Intent:
        if ast_node.resource_type == ResourceType.TREE:
            kind = IntentKind.QUERY_STATE
        elif ast_node.resource_type == ResourceType.SEARCH:
            kind = IntentKind.QUERY_STATE
        else:
            kind = IntentKind.READ_RESOURCE

        return Intent(
            kind=kind,
            target=ast_node.target,
            metadata={"sub_type": ast_node.resource_type.name}
        )

    def lower_to_operations(self, intent: Intent) -> List[Operation]:
        sub_type = intent.metadata.get("sub_type")

        if sub_type == "TREE":
            return [Operation(instruction=PrimitiveISA.LIST, payload={"path": intent.target})]
        elif sub_type == "SEARCH":
            return [Operation(instruction=PrimitiveISA.SEARCH, payload={"query": intent.target})]
        else:
            return [
                Operation(
                    instruction=PrimitiveISA.READ,
                    payload={"target": intent.target, "fallback_dir": "protocol"}
                )
            ]
