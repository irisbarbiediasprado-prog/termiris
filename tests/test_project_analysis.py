from pathlib import Path

from project import ProjectAnalysis


def test_project_analysis_contract():
    analysis = ProjectAnalysis(
        files=(
            Path("app.py"),
        ),
        indexes=(),
    )

    assert analysis.files == (
        Path("app.py"),
    )
    assert analysis.indexes == ()
