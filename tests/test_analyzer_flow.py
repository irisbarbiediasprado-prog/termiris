from analysis.analyzer import Analyzer
from analysis.engine import AnalysisEngine
from analysis.matchers import LegacyImportMatcher
from drivers.libcst.find_imports import FindImportsVisitor


def test_analyzer_full_flow():
    source = "import optparse\n"

    analyzer = Analyzer(
        visitors=[
            FindImportsVisitor,
        ],
    )

    index = analyzer.analyze(source)

    findings = AnalysisEngine(
        matchers=[
            LegacyImportMatcher("optparse"),
        ]
    ).analyze(index)

    assert len(findings) == 1
    assert findings[0].item.module == "optparse"
