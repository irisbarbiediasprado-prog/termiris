from analysis.context import AnalysisContext
from analysis.index import AnalysisIndex
from drivers.libcst import LibCSTDriver
from drivers.libcst.location import wrap, get_positions


class AnalysisRunner:
    def __init__(self, visitors):
        self.driver = LibCSTDriver()
        self.visitor_types = visitors

    def analyze(self, source: str):
        tree = self.driver.parse_source(source)

        wrapper = wrap(tree)

        context = AnalysisContext(
            tree=tree,
            positions=get_positions(wrapper),
        )

        index = AnalysisIndex()

        for visitor_type in self.visitor_types:
            visitor = visitor_type(context)
            self.driver.visit(tree, visitor)

            if hasattr(visitor, "functions"):
                index.functions.extend(visitor.functions)

            if hasattr(visitor, "classes"):
                index.classes.extend(visitor.classes)

            if hasattr(visitor, "imports"):
                index.imports.extend(visitor.imports)

            if hasattr(visitor, "calls"):
                index.calls.extend(visitor.calls)

            if hasattr(visitor, "comments"):
                index.comments.extend(visitor.comments)

            if hasattr(visitor, "exceptions"):
                index.exceptions.extend(visitor.exceptions)

        return index
