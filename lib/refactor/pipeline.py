from typing import Iterable
from analysis.finding import Finding
from refactor.generator import OperationGenerator
from refactor.runner import RefactorRunner
from refactor.context import RefactorContext
from refactor.result import RefactorResult


class MigrationPipeline:
    def __init__(
        self,
        generator: OperationGenerator,
        runner: RefactorRunner,
    ):
        self.generator = generator
        self.runner = runner

    def run(
        self,
        findings: Iterable[Finding],
        context: RefactorContext,
    ) -> RefactorResult:
        operations = [
            op
            for finding in findings
            if (op := self.generator.generate(finding)) is not None
        ]
        return self.runner.run(context, operations)
