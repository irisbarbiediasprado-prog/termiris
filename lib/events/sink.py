from abc import ABC, abstractmethod

class EventSink(ABC):
    @abstractmethod
    def publish(self, event: dict) -> None:
        ...

    def close(self) -> None:
        pass
