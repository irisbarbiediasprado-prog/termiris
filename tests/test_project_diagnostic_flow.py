import tempfile
from pathlib import Path
from analysis.analyzer import Analyzer
from project.analyzer import ProjectAnalyzer
from project.diagnostic_engine import ProjectDiagnosticEngine
from project.rules.legacy_import import LegacyImportRule

def test_end_to_end_legacy_import_detection():
    with tempfile.TemporaryDirectory() as tmp:
        code = "import optparse\n"
        file_path = Path(tmp) / "sample.py"
        file_path.write_text(code)

        analyzer = ProjectAnalyzer(Analyzer())
        project_analysis = analyzer.analyze(tmp)

        engine = ProjectDiagnosticEngine(rules=[LegacyImportRule()])
        diagnostic = engine.run(project_analysis)

        assert len(diagnostic.findings) == 1
        finding = diagnostic.findings[0]
        assert finding.kind == "legacy_import"
        assert "optparse" in finding.message
        assert finding.file == file_path
        from analysis.models import ImportInfo
        assert isinstance(finding.item, ImportInfo)
        assert finding.item.module == "optparse"
