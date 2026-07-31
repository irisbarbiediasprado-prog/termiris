from analysis.models import ImportInfo
from analysis.finding import Finding
from refactor.generator import OperationGenerator
from refactor.operations import ReplaceImportOperation
from refactor.rules import MigrationRule

def test_generate_replace_import():
    finding = Finding(
        kind="LegacyImportMatcher",
        message="legacy import",
        item=ImportInfo(module="optparse"),
    )
    rule = MigrationRule(source="optparse", target="argparse")
    generator = OperationGenerator([rule])
    operation = generator.generate(finding)
    assert isinstance(operation, ReplaceImportOperation)
    assert operation.old_module == "optparse"
    assert operation.new_module == "argparse"
