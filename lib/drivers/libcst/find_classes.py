import libcst
from analysis.context import AnalysisContext
from analysis import ClassInfo


class FindClassesVisitor(libcst.CSTVisitor):
    def __init__(self, context: AnalysisContext | None = None):
        self.context = context or AnalysisContext(tree=None)
        self.classes = []

    def visit_ClassDef(self, node: libcst.ClassDef):
        self.classes.append(
            ClassInfo(
                name=node.name.value,
            )
        )
