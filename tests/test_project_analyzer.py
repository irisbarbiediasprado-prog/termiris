from project import ProjectAnalyzer
from analysis.analyzer import Analyzer


def test_project_analyzer(tmp_path):
    (tmp_path / "app.py").write_text(
        "def hello():\n    pass\n"
    )

    result = ProjectAnalyzer(
        Analyzer()
    ).analyze(tmp_path)

    assert len(result.files) == 1
    assert len(result.indexes) == 1
