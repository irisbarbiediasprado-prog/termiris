import libcst
from analysis.context import AnalysisContext
from analysis import FunctionInfo


class FindFunctionsVisitor(libcst.CSTVisitor):
    def __init__(self, context: AnalysisContext | None = None):
        self.context = context or AnalysisContext(tree=None)
        self.functions = []

    def visit_FunctionDef(self, node: libcst.FunctionDef):
        self.functions.append(
            FunctionInfo(
                name=node.name.value,
                parameters=tuple(
                    p.name.value
                    for p in node.params.params
                ),
            )
        )
