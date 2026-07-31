from drivers.libcst import LibCSTDriver
from refactor.pipeline import MigrationPipeline
from refactor.generator import OperationGenerator
from refactor.runner import RefactorRunner
from refactor.executors.libcst import LibCSTExecutor
from refactor.rules import MigrationRule
from refactor.context import RefactorContext
from refactor.operations import ReplaceImportOperation
from analysis.finding import Finding
from analysis.models import ImportInfo

def test_pipeline_uses_plan():
    driver = LibCSTDriver()
    generator = OperationGenerator(
        rules=[MigrationRule(source="optparse", target="argparse")]
    )
    runner = RefactorRunner(LibCSTExecutor(driver))
    pipeline = MigrationPipeline(generator=generator, runner=runner)

    findings = [
        Finding(
            kind="LegacyImportMatcher",
            message="...",
            item=ImportInfo(module="optparse"),
        )
    ]

    source = "import optparse\n"
    context = RefactorContext(tree=driver.parse_source(source))
    result = pipeline.run(findings, context)

    # O plano está implícito nas operações aplicadas
    assert len(result.applied) == 1
    assert isinstance(result.applied[0], ReplaceImportOperation)
    assert result.tree.code == "import argparse\n"
