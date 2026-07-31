from pathlib import Path
from project.analysis import ProjectAnalysis, SourceFileAnalysis
from project.source_file import SourceFile
from analysis.index import AnalysisIndex

def test_project_analysis_contract():
    sf = SourceFile(path=Path("app.py"), line_count=0, size=0)
    sfa = SourceFileAnalysis(source=sf, index=AnalysisIndex())
    analysis = ProjectAnalysis(files=(sfa,))
    assert len(analysis.files) == 1
    assert analysis.files[0].source.path == Path("app.py")
