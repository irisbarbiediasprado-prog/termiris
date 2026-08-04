from abc import ABC, abstractmethod
from typing import Any, List

from protocol.ir import Intent
from protocol.isa import Operation

class ProtocolPlugin(ABC):
    """
    Contrato canônico de um plugin do protocolo.
    """

    @property
    @abstractmethod
    def command(self) -> str:...

    @abstractmethod
    def parse_ast(self, tokens: List[str]) -> Any:...

    @abstractmethod
    def lower_to_intent(self, ast_node: Any) -> Intent:...

    @abstractmethod
    def lower_to_operations(self, intent: Intent) -> List[Operation]:...
