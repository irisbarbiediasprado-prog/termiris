import libcst
from analysis.context import AnalysisContext
from analysis import CallInfo


class FindCallsVisitor(libcst.CSTVisitor):
    def __init__(self, context: AnalysisContext | None = None):
        self.context = context or AnalysisContext(tree=None)
        self.calls = []

    def visit_Call(self, node: libcst.Call):
        if isinstance(node.func, libcst.Name):
            self.calls.append(
                CallInfo(
                    function=node.func.value,
                )
            )
