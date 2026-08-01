import libcst
from analysis.context import AnalysisContext
from analysis.models import ExceptionInfo


class FindExceptionsVisitor(libcst.CSTVisitor):
    def __init__(self, context: AnalysisContext | None = None):
        self.context = context or AnalysisContext(tree=None)
        self.exceptions = []

    def visit_ExceptHandler(self, node: libcst.ExceptHandler):
        self.exceptions.append(
            ExceptionInfo(
                is_bare=node.type is None,
            )
        )
