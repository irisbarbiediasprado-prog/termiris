from .analysis import ProjectAnalysis
from .report import ProjectReport


class ProjectReporter:
    def report(self, analysis: ProjectAnalysis) -> ProjectReport:
        return ProjectReport(
            files_count=len(analysis.files),
            functions_count=sum(
                len(index.functions)
                for index in analysis.indexes
            ),
            classes_count=sum(
                len(index.classes)
                for index in analysis.indexes
            ),
            imports_count=sum(
                len(index.imports)
                for index in analysis.indexes
            ),
            calls_count=sum(
                len(index.calls)
                for index in analysis.indexes
            ),
        )
