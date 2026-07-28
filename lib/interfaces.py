from abc import ABC, abstractmethod
from typing import List
from models import Artifact

class ArtifactRepositoryInterface(ABC):
    @abstractmethod
    def list_artifacts(self) -> List[Artifact]:
        pass

