import libcst as cst
from refactor.operations import ReplaceImportOperation
from refactor.context import RefactorContext


class ReplaceImportTransformer(cst.CSTTransformer):
    def __init__(
        self,
        context: RefactorContext,
        operation: ReplaceImportOperation,
    ):
        self.context = context
        self.operation = operation

    def leave_Import(self, original_node, updated_node):
        names = []

        for alias in updated_node.names:
            if alias.name.value == self.operation.old_module:
                names.append(
                    alias.with_changes(
                        name=cst.Name(
                            self.operation.new_module
                        )
                    )
                )
            else:
                names.append(alias)

        return updated_node.with_changes(
            names=names
        )
