from analysis.analyzer import Analyzer
from project.analysis import ProjectAnalysis, SourceFileAnalysis
from project.source_file import SourceFile
from pathlib import Path
from project.rules import LargeFunctionRule, RuleId


def _analyze_code(code: str) -> ProjectAnalysis:
    index = Analyzer().analyze(code)
    source = SourceFile(path=Path("test.py"), line_count=code.count("\n") + 1, size=len(code))
    return ProjectAnalysis(files=(SourceFileAnalysis(source=source, index=index),))


def test_detects_many_parameters():
    code = "def f(a, b, c, d, e, f): pass"
    analysis = _analyze_code(code)
    findings = list(LargeFunctionRule().run(analysis))
    assert len(findings) == 1
    assert findings[0].rule_id == RuleId.LARGE_FUNCTION


def test_ok_with_few_parameters():
    code = "def f(a, b): pass"
    analysis = _analyze_code(code)
    findings = list(LargeFunctionRule().run(analysis))
    assert len(findings) == 0


def test_custom_max_parameters():
    code = "def f(a, b, c): pass"
    analysis = _analyze_code(code)
    rule = LargeFunctionRule(max_parameters=2)
    findings = list(rule.run(analysis))
    assert len(findings) == 1
