import re
from protocol.ast import ProtocolNode, BootstrapNode, RetrieveNode, ResourceType, InvalidNode

class ProtocolParser:
    PATTERN = re.compile(r"^<<\s*([A-Z_]+)(?:\s+([A-Z_]+))?(?:\s+(.*))?\s*>>$")

    @classmethod
    def parse(cls, raw_line: str) -> ProtocolNode:
        line = raw_line.strip()
        match = cls.PATTERN.match(line)
        if not match:
            return InvalidNode(raw=line, reason="Grammar mismatch")

        verb, target_type, args = match.groups()
        args = args.strip() if args else ""

        match (verb, target_type):
            case ("BOOTSTRAP", _):
                return BootstrapNode()
            case ("RETRIEVE", "FILE"):
                return RetrieveNode(ResourceType.FILE, args) if args else InvalidNode(line, "Missing file path")
            case ("RETRIEVE", "TREE"):
                return RetrieveNode(ResourceType.TREE, args or ".")
            case ("RETRIEVE", "SEARCH"):
                return RetrieveNode(ResourceType.SEARCH, args) if args else InvalidNode(line, "Missing search query")
            case ("RETRIEVE", target) if target:
                filename = target if target.endswith(".md") else f"{target}.md"
                return RetrieveNode(ResourceType.FILE, filename)
            case _:
                return InvalidNode(line, f"Unknown command: {verb} {target_type}")

