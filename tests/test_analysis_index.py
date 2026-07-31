from analysis import FunctionInfo, ClassInfo, ImportInfo, CallInfo
from analysis.index import AnalysisIndex


def test_analysis_index():
    index = AnalysisIndex(
        functions=[FunctionInfo("main", ())],
        classes=[ClassInfo("App")],
        imports=[ImportInfo("os")],
        calls=[CallInfo("print")],
    )

    assert index.functions[0].name == "main"
    assert index.classes[0].name == "App"
    assert index.imports[0].module == "os"
    assert index.calls[0].function == "print"
