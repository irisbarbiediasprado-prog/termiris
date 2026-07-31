from refactor.pipeline import MigrationPipeline
from refactor.generator import OperationGenerator
from refactor.runner import RefactorRunner
from refactor.context import RefactorContext
from refactor.executors.libcst import LibCSTExecutor
from refactor.rules import MigrationRule
from refactor.operations import ReplaceImportOperation
from drivers.libcst import LibCSTDriver
from analysis.analyzer import Analyzer
from analysis.matchers import LegacyImportMatcher

def test_pipeline_with_real_components():
    source = "import optparse\n"
    # Analyzer com matchers já retorna uma lista de Finding
    analyzer = Analyzer(matchers=[LegacyImportMatcher("optparse")])
    findings = analyzer.analyze(source)  # lista de Finding

    # Configurar pipeline com regra real
    rule = MigrationRule(source="optparse", target="argparse")
    generator = OperationGenerator([rule])
    runner = RefactorRunner(LibCSTExecutor(LibCSTDriver()))
    pipeline = MigrationPipeline(generator=generator, runner=runner)

    # Executar migração
    context = RefactorContext(tree=LibCSTDriver().parse_source(source))
    result = pipeline.run(findings, context)

    # Verificar resultado tipado
    assert result.tree.code == "import argparse\n"
    assert len(result.applied) == 1
    assert isinstance(result.applied[0], ReplaceImportOperation)
    assert result.applied[0].old_module == "optparse"
    assert result.applied[0].new_module == "argparse"
    assert result.failed == ()
