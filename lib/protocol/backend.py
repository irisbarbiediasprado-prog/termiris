from abc import ABC, abstractmethod
from typing import List
from protocol.plan import MigrationPlan

class Backend(ABC):
    def validate(self, plan: MigrationPlan) -> None:
        """Valida estrutura do plano. Padrão: sem op."""
        pass

    @abstractmethod
    def compile(self, plan: MigrationPlan) -> List:
       ...
