from abc import ABC, abstractmethod
from typing import Any


class Matcher(ABC):
    @abstractmethod
    def matches(self, item: Any) -> bool:
        raise NotImplementedError
