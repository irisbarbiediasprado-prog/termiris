from pathlib import Path
from project.source_file import SourceFile
from project.analysis import ProjectAnalysis, SourceFileAnalysis
from project.statistics_engine import StatisticsEngine
from analysis.index import AnalysisIndex
from analysis.models import FunctionInfo, ClassInfo, ImportInfo, CallInfo

def test_statistics_engine():
    idx1 = AnalysisIndex(
        functions=[FunctionInfo(name="f1", parameters=(), line=1)],
        classes=[ClassInfo(name="C1", line=2)],
        imports=[ImportInfo(module="os")],
        calls=[CallInfo(function="print", line=3)],
    )
    idx2 = AnalysisIndex(
        functions=[FunctionInfo(name="f2", parameters=("x",), line=1)],
        classes=[],
        imports=[ImportInfo(module="sys")],
        calls=[CallInfo(function="len", line=2), CallInfo(function="range", line=2)],
    )
    sfa1 = SourceFileAnalysis(
        source=SourceFile(path=Path("a.py"), line_count=5, size=100),
        index=idx1,
    )
    sfa2 = SourceFileAnalysis(
        source=SourceFile(path=Path("b.py"), line_count=3, size=50),
        index=idx2,
    )
    analysis = ProjectAnalysis(files=(sfa1, sfa2))
    stats = StatisticsEngine.compute(analysis)
    assert stats.files == 2
    assert stats.functions == 2
    assert stats.classes == 1
    assert stats.imports == 2
    assert stats.calls == 3
