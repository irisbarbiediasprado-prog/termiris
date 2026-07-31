from project import (
    ProjectAnalysis,
    ProjectReporter,
)
from pathlib import Path


class FakeIndex:
    functions = [1, 2]
    classes = [1]
    imports = [1, 2, 3]
    calls = [1]


def test_project_reporter():
    report = ProjectReporter().report(
        ProjectAnalysis(
            files=(Path("app.py"),),
            indexes=(FakeIndex(),),
        )
    )

    assert report.files_count == 1
    assert report.functions_count == 2
    assert report.classes_count == 1
    assert report.imports_count == 3
    assert report.calls_count == 1
