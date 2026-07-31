from analysis.analyzer import Analyzer


def test_analyzer_collects_code_facts():
    index = Analyzer().analyze(
        """
import os

class App:
    pass

def main():
    print("ok")
"""
    )

    assert index.imports[0].module == "os"
    assert index.classes[0].name == "App"
    assert index.functions[0].name == "main"
    assert index.calls[0].function == "print"
