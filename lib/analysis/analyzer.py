from analysis.runner import AnalysisRunner
from analysis.engine import AnalysisEngine
from drivers.libcst.find_functions import FindFunctionsVisitor
from drivers.libcst.find_classes import FindClassesVisitor
from drivers.libcst.find_imports import FindImportsVisitor
from drivers.libcst.find_calls import FindCallsVisitor


class Analyzer:
    def __init__(self, visitors=None, matchers=None):
        self.runner = AnalysisRunner(
            visitors or [
                FindFunctionsVisitor,
                FindClassesVisitor,
                FindImportsVisitor,
                FindCallsVisitor,
            ]
        )
        self.engine = AnalysisEngine(matchers) if matchers else None

    def analyze(self, source: str):
        index = self.runner.analyze(source)

        if self.engine:
            return self.engine.analyze(index)

        return index
