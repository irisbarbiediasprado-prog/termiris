from analysis.analyzer import Analyzer
from project.analysis import ProjectAnalysis, SourceFileAnalysis
from project.source_file import SourceFile
from pathlib import Path
from project.rules import TodoCommentRule, RuleId


def _analyze_code(code: str) -> ProjectAnalysis:
    index = Analyzer().analyze(code)
    source = SourceFile(path=Path("test.py"), line_count=code.count("\n") + 1, size=len(code))
    return ProjectAnalysis(files=(SourceFileAnalysis(source=source, index=index),))


def test_detects_todo():
    code = "# TODO: fix this\nx = 1"
    analysis = _analyze_code(code)
    findings = list(TodoCommentRule().run(analysis))
    assert len(findings) == 1
    assert findings[0].rule_id == RuleId.TODO_COMMENT


def test_detects_fixme_case_insensitive():
    code = "# fixme: urgent\nx = 1"
    analysis = _analyze_code(code)
    findings = list(TodoCommentRule().run(analysis))
    assert len(findings) == 1


def test_ignores_normal_comments():
    code = "# This is fine\nx = 1"
    analysis = _analyze_code(code)
    findings = list(TodoCommentRule().run(analysis))
    assert len(findings) == 0


def test_ignores_partial_word():
    code = "# METHODODOLOGY\nx = 1"
    analysis = _analyze_code(code)
    findings = list(TodoCommentRule().run(analysis))
    assert len(findings) == 0
