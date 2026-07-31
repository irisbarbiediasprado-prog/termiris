from dataclasses import dataclass
from .source_file import SourceFile
from analysis.index import AnalysisIndex

@dataclass(frozen=True)
class SourceFileAnalysis:
    source: SourceFile
    index: AnalysisIndex

@dataclass(frozen=True)
class ProjectAnalysis:
    files: tuple[SourceFileAnalysis, ...]
