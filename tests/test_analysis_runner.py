from analysis.runner import AnalysisRunner
from drivers.libcst.find_functions import FindFunctionsVisitor
from analysis import FunctionInfo


def test_analysis_runner():
    runner = AnalysisRunner(
        visitors=[
            FindFunctionsVisitor,
        ]
    )

    index = runner.analyze(
        """
def hello():
    pass
"""
    )

    assert index.functions == [
        FunctionInfo(
            name="hello",
            parameters=(),
        )
    ]
