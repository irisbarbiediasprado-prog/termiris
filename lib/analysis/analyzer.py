from analysis.runner import AnalysisRunner
from analysis.index import AnalysisIndex
from drivers.libcst.find_functions import FindFunctionsVisitor
from drivers.libcst.find_classes import FindClassesVisitor
from drivers.libcst.find_imports import FindImportsVisitor
from drivers.libcst.find_calls import FindCallsVisitor
from drivers.libcst.find_comments import FindCommentsVisitor
from drivers.libcst.find_exceptions import FindExceptionsVisitor


class Analyzer:
    def __init__(self, visitors=None):
        self.runner = AnalysisRunner(
            visitors or [
                FindFunctionsVisitor,
                FindClassesVisitor,
                FindImportsVisitor,
                FindCallsVisitor,
                FindCommentsVisitor,
                FindExceptionsVisitor,
            ]
        )

    def analyze(self, source: str) -> AnalysisIndex:
        return self.runner.analyze(source)
