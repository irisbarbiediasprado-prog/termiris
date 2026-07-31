from pathlib import Path

from analysis.analyzer import Analyzer
from .analysis import ProjectAnalysis
from .scanner import ProjectScanner


class ProjectAnalyzer:
    def __init__(self, analyzer: Analyzer):
        self.analyzer = analyzer

    def analyze(self, root: str | Path) -> ProjectAnalysis:
        files = ProjectScanner(root).scan()

        indexes = tuple(
            self.analyzer.analyze(
                path.read_text()
            )
            for path in files
        )

        return ProjectAnalysis(
            files=files,
            indexes=indexes,
        )
