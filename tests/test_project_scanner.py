from pathlib import Path

from project import ProjectScanner


def test_project_scanner(tmp_path: Path):
    (tmp_path / "app.py").write_text("print('app')")
    (tmp_path / "utils.py").write_text("print('utils')")
    (tmp_path / "README.md").write_text("# docs")

    files = ProjectScanner(tmp_path).scan()

    assert files == (
        tmp_path / "app.py",
        tmp_path / "utils.py",
    )
