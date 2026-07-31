from pathlib import Path
from project.source_file import SourceFile
from project.analysis import ProjectAnalysis, SourceFileAnalysis
from analysis.index import AnalysisIndex
from project.reporter import ProjectReporter

def test_project_reporter():
    sf = SourceFile(path=Path("app.py"), line_count=2, size=20)
    sfa = SourceFileAnalysis(source=sf, index=AnalysisIndex())
    analysis = ProjectAnalysis(files=(sfa,))
    reporter = ProjectReporter()
    report = reporter.report(analysis)
    assert report.files_count == 1
    assert report.functions_count == 0
    assert report.classes_count == 0
    assert report.imports_count == 0
    assert report.calls_count == 0
