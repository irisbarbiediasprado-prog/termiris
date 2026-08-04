from dataclasses import dataclass
from enum import Enum, auto
from typing import List
from protocol.base import ProtocolPlugin
from protocol.ir import Intent, IntentKind
from protocol.isa import Operation

class ResourceType(Enum):
    FILE = auto()
    TREE = auto()
    SEARCH = auto()
    DIFF = auto()
    STATUS = auto()

@dataclass(frozen=True)
class RetrieveAST:
    resource_type: ResourceType
    targets: List[str]

class RetrievePlugin(ProtocolPlugin):
    @property
    def command(self) -> str:
        return "RETRIEVE"

    def parse_ast(self, tokens: List[str]) -> RetrieveAST:
        if not tokens:
            raise ValueError("RETRIEVE vazio")

        clean = [t for t in tokens if not t.startswith("<<") and not t.endswith(">>")]
        if not clean:
            clean = tokens

        head = clean[0].upper()
        args = clean[1:]

        if head == "FILE":
            return RetrieveAST(ResourceType.FILE, args if args else ["README.md"])
        elif head == "TREE":
            return RetrieveAST(ResourceType.TREE, args if args else ["."])
        elif head == "SEARCH":
            return RetrieveAST(ResourceType.SEARCH, [" ".join(args)])
        elif head == "DIFF":
            return RetrieveAST(ResourceType.DIFF, args if args else ["."])
        elif head == "STATUS":
            return RetrieveAST(ResourceType.STATUS, ["."])
        else:
            files = [t if t.endswith(".md") else f"{t}.md" for t in clean]
            return RetrieveAST(ResourceType.FILE, files)

    def lower_to_intent(self, ast_node: RetrieveAST) -> Intent:
        return Intent(
            kind=IntentKind.READ_RESOURCE,
            target=" ".join(ast_node.targets),
            metadata={
                "sub_type": ast_node.resource_type.name,
                "targets_list": ast_node.targets
            }
        )

    def lower_to_operations(self, intent: Intent) -> List[Operation]:
        raise NotImplementedError("Operation generation moved to ProtocolCompiler.")
