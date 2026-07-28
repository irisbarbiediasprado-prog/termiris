from abc import ABC, abstractmethod
from typing import List, Any
from protocol.ir import Intent
from protocol.isa import Operation

class ProtocolPlugin(ABC):
    @property
    @abstractmethod
    def command(self) -> str:
        """Comando de alto nível (Ex: RETRIEVE, BOOTSTRAP)"""
        pass

    @abstractmethod
    def parse_ast(self, tokens: List[str]) -> Any:
        """Estágio 1: Gramática / Tokens -> AST"""
        pass

    @abstractmethod
    def lower_to_intent(self, ast_node: Any) -> Intent:
        """Estágio 2: Semântica / AST -> IR (Intent)"""
        pass

    @abstractmethod
    def lower_to_operations(self, intent: Intent) -> List[Operation]:
        """Estágio 3: Compilação / IR -> Primitivas da ISA"""
        pass
