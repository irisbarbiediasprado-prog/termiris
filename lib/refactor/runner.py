from refactor.context import RefactorContext
from refactor.result import RefactorResult


class RefactorRunner:
    def __init__(self, executor):
        self.executor = executor

    def run(self, context: RefactorContext, operations):
        result = context.tree
        applied = []
        failed = []

        for operation in operations:
            try:
                context = RefactorContext(
                    tree=result,
                    positions=context.positions,
                    artifacts=context.artifacts,
                )

                result = self.executor.execute(
                    context,
                    operation,
                )

                applied.append(operation)

            except Exception as error:
                failed.append(
                    (operation, error)
                )

        return RefactorResult(
            tree=result,
            applied=tuple(applied),
            failed=tuple(failed),
        )
