import shlex
from typing import Tuple, Dict, List

def extract_metadata(raw: str) -> Tuple[str, Dict[str, str]]:
    try:
        tokens = shlex.split(raw)
    except ValueError:
        tokens = raw.split()
    
    metadata: Dict[str, str] = {}
    command_parts: List[str] = []
    
    for token in tokens:
        if token.startswith("--") and "=" in token:
            key, value = token[2:].split("=", 1)
            metadata[key] = value
        else:
            command_parts.append(token)
    
    clean = " ".join(command_parts)
    return clean, metadata
