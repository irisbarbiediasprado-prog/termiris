from pathlib import Path
from analysis.analyzer import Analyzer
from project.analyzer import ProjectAnalyzer

def test_project_analyzer(tmp_path):
    (tmp_path / "app.py").write_text("def hello():\n    pass\n")
    result = ProjectAnalyzer(Analyzer()).analyze(tmp_path)
    assert len(result.files) == 1
    # Novo contrato: acessa o SourceFileAnalysis
    sfa = result.files[0]
    assert sfa.source.path == tmp_path / "app.py"
    assert sfa.source.line_count == 2
    assert sfa.source.size > 0
    # O índice deve ter a função encontrada
    assert len(sfa.index.functions) == 1
    assert sfa.index.functions[0].name == "hello"
