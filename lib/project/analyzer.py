from pathlib import Path
from analysis.analyzer import Analyzer
from .analysis import ProjectAnalysis, SourceFileAnalysis
from .source_file import SourceFile
from .scanner import ProjectScanner

class ProjectAnalyzer:
    def __init__(self, analyzer: Analyzer):
        self.analyzer = analyzer

    def analyze(self, root: str | Path) -> ProjectAnalysis:
        paths = ProjectScanner(root).scan()
        file_analyses = []
        for path in paths:
            source_code = path.read_text()
            line_count = source_code.count('\n') + (1 if source_code and not source_code.endswith('\n') else 0)
            size = path.stat().st_size
            index = self.analyzer.analyze(source_code)
            file_analyses.append(
                SourceFileAnalysis(
                    source=SourceFile(path=path, line_count=line_count, size=size),
                    index=index,
                )
            )
        return ProjectAnalysis(files=tuple(file_analyses))
