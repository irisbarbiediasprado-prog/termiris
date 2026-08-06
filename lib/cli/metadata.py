#!/usr/bin/env python3
import shlex
from typing import Tuple, Dict, List

def extract_metadata(raw: str) -> Tuple[str, Dict[str, str]]:
    """
    Extrai pares --chave=valor de uma string de comando, preservando argumentos posicionais.
    Retorna: (comando_limpo, dicionario_metadata)
    
    Exemplo:
        extract_metadata(".file snapshot.ctx --hash=abc123 --origin=delivery")
        -> (".file snapshot.ctx", {"hash": "abc123", "origin": "delivery"})
    """
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
