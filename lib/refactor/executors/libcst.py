from refactor.operations import ReplaceImportOperation
from refactor.transformers import ReplaceImportTransformer
from refactor.context import RefactorContext


class LibCSTExecutor:
    def __init__(self, driver):
        self.driver = driver

    def execute(
        self,
        context: RefactorContext,
        operation,
    ):
        if isinstance(operation, ReplaceImportOperation):
            transformer = ReplaceImportTransformer(
                context,
                operation,
            )

            return self.driver.transform(
                context.tree,
                transformer,
            )

        raise ValueError(
            f"Unsupported operation: {operation.kind}"
        )
