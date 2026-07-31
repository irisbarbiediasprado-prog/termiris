from analysis.finding import Finding
from analysis.models import ImportInfo
from refactor import OperationGenerator, ReplaceImportOperation
from refactor.rules import MigrationRule


def test_migration_rule_generates_operation():
    generator = OperationGenerator(
        rules=[
            MigrationRule(
                source="optparse",
                target="argparse",
            )
        ]
    )

    finding = Finding(
        kind="LegacyImportMatcher",
        message="legacy",
        item=ImportInfo(module="optparse"),
    )

    operation = generator.generate(finding)

    assert isinstance(operation, ReplaceImportOperation)
    assert operation.new_module == "argparse"
