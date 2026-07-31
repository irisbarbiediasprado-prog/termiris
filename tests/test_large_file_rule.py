import tempfile
from pathlib import Path
from project.source_file import SourceFile
from project.analysis import ProjectAnalysis, SourceFileAnalysis
from project.rules.large_file import LargeFileRule
from analysis.index import AnalysisIndex

def test_large_file_rule():
    with tempfile.TemporaryDirectory() as tmp:
        small = Path(tmp) / "small.py"
        small.write_text("x = 1\n" * 10)
        large = Path(tmp) / "large.py"
        large.write_text("x = 1\n" * 501)

        # Cria SourceFileAnalysis manualmente (sem precisar do ProjectAnalyzer completo)
        small_sf = SourceFile(path=small, line_count=10, size=small.stat().st_size)
        large_sf = SourceFile(path=large, line_count=501, size=large.stat().st_size)
        empty_index = AnalysisIndex()

        analysis = ProjectAnalysis(files=(
            SourceFileAnalysis(source=small_sf, index=empty_index),
            SourceFileAnalysis(source=large_sf, index=empty_index),
        ))

        rule = LargeFileRule()
        findings = list(rule.run(analysis))

        assert len(findings) == 1
        assert findings[0].kind == "large_file"
        assert findings[0].file == large
