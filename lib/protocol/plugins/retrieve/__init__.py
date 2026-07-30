import re
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
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

        # Limpa marcas de streaming
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
            # Tratamento para lista direta de arquivos se o subcomando for omitido
            files = [t if t.endswith(".md") else f"{t}.md" for t in clean]
            return RetrieveAST(ResourceType.FILE, files)

    def lower_to_intent(self, ast_node: RetrieveAST) -> Intent:
        resolved_targets = []

        if ast_node.resource_type in (ResourceType.FILE, ResourceType.TREE):
            for target in ast_node.targets:
                p = Path(target)
                c1 = Path.home() / ".termiris" / p
                c2 = p.resolve()

                if c1.exists():
                    resolved_targets.append(str(c1))
                elif c2.exists():
                    resolved_targets.append(str(c2))
                else:
                    # Se não existir, mantém o relativo para o ISA decidir o aviso de erro
                    resolved_targets.append(str(p))
        else:
            resolved_targets = ast_node.targets

        return Intent(
            kind=IntentKind.READ_RESOURCE,
            target=" ".join(resolved_targets),
            metadata={
                "sub_type": ast_node.resource_type.name,
                "targets_list": resolved_targets
            }
        )

    def lower_to_operations(self, intent: Intent) -> List[Operation]:
        raise NotImplementedError("Operation generation moved to ProtocolCompiler.")

