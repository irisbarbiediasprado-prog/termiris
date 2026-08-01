from analysis.analyzer import Analyzer
from project.analysis import ProjectAnalysis, SourceFileAnalysis
from project.source_file import SourceFile
from pathlib import Path
from project.rules import BareExceptRule, RuleId


def _analyze_code(code: str) -> ProjectAnalysis:
    index = Analyzer().analyze(code)
    source = SourceFile(path=Path("test.py"), line_count=code.count("\n") + 1, size=len(code))
    return ProjectAnalysis(files=(SourceFileAnalysis(source=source, index=index),))


def test_detects_bare_except():
    code = "try:\n    pass\nexcept:\n    pass"
    analysis = _analyze_code(code)
    findings = list(BareExceptRule().run(analysis))
    assert len(findings) == 1
    assert findings[0].rule_id == RuleId.BARE_EXCEPT


def test_ignores_typed_except():
    code = "try:\n    pass\nexcept ValueError:\n    pass"
    analysis = _analyze_code(code)
    findings = list(BareExceptRule().run(analysis))
    assert len(findings) == 0


def test_detects_bare_except_multiple():
    code = "try:\n    pass\nexcept:\n    pass\ntry:\n    pass\nexcept:\n    pass"
    analysis = _analyze_code(code)
    findings = list(BareExceptRule().run(analysis))
    assert len(findings) == 2
