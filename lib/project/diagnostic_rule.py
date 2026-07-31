from abc import ABC, abstractmethod
from typing import Iterable
from .analysis import ProjectAnalysis
from .finding import ProjectFinding

class DiagnosticRule(ABC):
    @abstractmethod
    def run(self, analysis: ProjectAnalysis) -> Iterable[ProjectFinding]:
        ...
