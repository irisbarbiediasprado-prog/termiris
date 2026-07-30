from abc import ABC, abstractmethod
from typing import Any, List

from protocol.ir import Intent
from protocol.isa import Operation


class ProtocolPlugin(ABC):
    """
    Contrato canônico de um plugin do protocolo.

    Pipeline:

        tokens
           ↓
        parse_ast()
           ↓
      lower_to_intent()
           ↓
    lower_to_operations()

    A etapa de compilação é orquestrada pelo ProtocolCompiler.
    """

    @property
    @abstractmethod
    def command(self) -> str:
        """Nome do comando exposto pelo plugin."""
        raise NotImplementedError

    @abstractmethod
    def parse_ast(self, tokens: List[str]) -> Any:
        """
        Tokens -> AST
        """
        raise NotImplementedError

    @abstractmethod
    def lower_to_intent(self, ast_node: Any) -> Intent:
        """
        AST -> Intent (IR)
        """
        raise NotImplementedError

    @abstractmethod
    def lower_to_operations(self, intent: Intent) -> List[Operation]:
        """
        Intent -> ISA

        Mantido por compatibilidade durante a migração.
        Em uma etapa futura esta responsabilidade será
        movida integralmente para ProtocolCompiler.
        """
        raise NotImplementedError
