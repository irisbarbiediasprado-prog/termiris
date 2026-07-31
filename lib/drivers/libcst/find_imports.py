import libcst
from analysis.context import AnalysisContext
from analysis import ImportInfo


class FindImportsVisitor(libcst.CSTVisitor):
    def __init__(self, context: AnalysisContext | None = None):
        self.context = context or AnalysisContext(tree=None)
        self.imports = []

    def visit_Import(self, node: libcst.Import):
        for alias in node.names:
            self.imports.append(
                ImportInfo(
                    module=alias.name.value,
                    alias=(
                        alias.asname.name.value
                        if alias.asname
                        else None
                    ),
                )
            )

    def visit_ImportFrom(self, node: libcst.ImportFrom):
        module_name = node.module.value if node.module else ""

        if isinstance(node.names, libcst.ImportStar):
            return

        for alias in node.names:
            self.imports.append(
                ImportInfo(
                    module=module_name,
                    alias=None,
                )
            )
