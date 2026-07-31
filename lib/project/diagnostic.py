from dataclasses import dataclass
from .finding import ProjectFinding

@dataclass(frozen=True)
class ProjectDiagnostic:
    findings: tuple[ProjectFinding, ...] = ()
