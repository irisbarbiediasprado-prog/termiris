from analysis.engine import AnalysisEngine
from analysis.matchers import LegacyImportMatcher
from analysis.index import AnalysisIndex
from analysis.models import ImportInfo


def test_analysis_engine_generates_findings():
    index = AnalysisIndex(
        imports=[
            ImportInfo(module="optparse"),
            ImportInfo(module="argparse"),
        ]
    )

    engine = AnalysisEngine(
        matchers=[
            LegacyImportMatcher("optparse")
        ]
    )

    findings = engine.analyze(index)

    assert len(findings) == 1
    assert findings[0].item.module == "optparse"
