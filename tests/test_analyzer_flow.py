from analysis.analyzer import Analyzer
from drivers.libcst.find_imports import FindImportsVisitor
from analysis.matchers import LegacyImportMatcher


def test_analyzer_full_flow():
    analyzer = Analyzer(
        visitors=[
            FindImportsVisitor,
        ],
        matchers=[
            LegacyImportMatcher("optparse"),
        ],
    )

    findings = analyzer.analyze(
        """
import optparse
"""
    )

    assert len(findings) == 1
    assert findings[0].item.module == "optparse"
