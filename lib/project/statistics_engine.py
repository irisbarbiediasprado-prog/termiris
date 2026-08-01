from .analysis import ProjectAnalysis
from .statistics import ProjectStatistics

class StatisticsEngine:
    @staticmethod
    def compute(analysis: ProjectAnalysis) -> ProjectStatistics:
        functions = 0
        classes = 0
        imports = 0
        calls = 0
        for sfa in analysis.files:
            idx = sfa.index
            functions += len(idx.functions)
            classes += len(idx.classes)
            imports += len(idx.imports)
            calls += len(idx.calls)
        return ProjectStatistics(
            files=len(analysis.files),
            functions=functions,
            classes=classes,
            imports=imports,
            calls=calls,
        )
