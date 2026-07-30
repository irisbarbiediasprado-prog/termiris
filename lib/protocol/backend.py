from abc import ABC, abstractmethod
from typing import List

from protocol.plan import MigrationPlan


class Backend(ABC):
    @abstractmethod
    def compile(self, plan: MigrationPlan) -> List:
        raise NotImplementedError
