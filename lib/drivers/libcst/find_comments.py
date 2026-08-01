import libcst
from analysis.context import AnalysisContext
from analysis.models import CommentInfo


class FindCommentsVisitor(libcst.CSTVisitor):
    def __init__(self, context: AnalysisContext | None = None):
        self.context = context or AnalysisContext(tree=None)
        self.comments = []

    def visit_Comment(self, node: libcst.Comment):
        self.comments.append(
            CommentInfo(
                text=node.value,
            )
        )
