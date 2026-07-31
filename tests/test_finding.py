from analysis.finding import Finding
from analysis.models import ImportInfo


def test_finding_contract():
    finding = Finding(
        kind="legacy_import",
        message="import optparse é legado",
        item=ImportInfo(module="optparse"),
    )

    assert finding.kind == "legacy_import"
    assert finding.message == "import optparse é legado"
    assert finding.item.module == "optparse"
