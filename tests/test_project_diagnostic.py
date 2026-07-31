from pathlib import Path
from project.finding import ProjectFinding
from project.diagnostic import ProjectDiagnostic

def test_project_finding_immutable():
    f = ProjectFinding(kind="t", message="m", file=Path("a.py"))
    assert f.kind == "t"
    try:
        f.kind = "x"
    except AttributeError:
        pass
    else:
        raise AssertionError("ProjectFinding should be frozen")

def test_project_diagnostic_immutable_and_empty():
    d = ProjectDiagnostic()
    assert d.findings == ()
    assert isinstance(d.findings, tuple)

    findings = (
        ProjectFinding(kind="a", message="m", file=Path("x.py")),
    )
    d2 = ProjectDiagnostic(findings=findings)
    assert d2.findings == findings
