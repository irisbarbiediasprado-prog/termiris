import pytest
from protocol.ir import Intent, IntentKind
from construction.compiler import ConstructionCompiler
from construction.renderers.python import PythonRenderer

class TestConstructionCompiler:
    def test_compile_simple_class(self):
        intent = Intent(
            kind=IntentKind.MUTATE_RESOURCE,
            target="workspace.py",
            metadata={
                "imports": ["os"],
                "classes": [
                    {
                        "name": "Workspace",
                        "docstring": "A workspace context.",
                        "methods": [
                            {
                                "name": "resolve",
                                "params": ["path"],
                                "body": "return self.path",
                            }
                        ]
                    }
                ]
            }
        )
        compiler = ConstructionCompiler()
        ir = compiler.compile(intent)
        assert len(ir.classes) == 1
        cls = ir.classes[0]
        assert cls.name == "Workspace"
        assert cls.docstring == "A workspace context."
        assert len(cls.methods) == 1
        m = cls.methods[0]
        assert m.name == "resolve"
        assert m.params == ["path"]
        assert "return self.path" in m.body

    def test_compile_multiple_classes_and_functions(self):
        intent = Intent(
            kind=IntentKind.MUTATE_RESOURCE,
            target="module.py",
            metadata={
                "imports": ["os", "pathlib"],
                "classes": [
                    {"name": "Foo", "methods": []},
                    {
                        "name": "Bar",
                        "decorators": ["dataclass"],
                        "methods": [
                            {"name": "foo", "body": "pass", "decorators": ["property"]}
                        ]
                    }
                ]
            }
        )
        compiler = ConstructionCompiler()
        ir = compiler.compile(intent)
        assert len(ir.classes) == 2
        bar = ir.classes[1]
        assert bar.decorators == ["dataclass"]
        assert bar.methods[0].decorators == ["property"]

    def test_compile_empty_method_body(self):
        intent = Intent(
            kind=IntentKind.MUTATE_RESOURCE,
            target="empty.py",
            metadata={
                "imports": [],
                "classes": [
                    {"name": "Empty", "methods": [{"name": "nothing", "body": ""}]}
                ]
            }
        )
        compiler = ConstructionCompiler()
        ir = compiler.compile(intent)
        assert ir.classes[0].methods[0].body == ""


class TestPythonRenderer:
    def test_render_minimal_class(self):
        ir = ConstructionCompiler().compile(
            Intent(
                kind=IntentKind.MUTATE_RESOURCE,
                target="test.py",
                metadata={
                    "imports": ["sys"],
                    "classes": [
                        {"name": "Minimal", "methods": []}
                    ]
                }
            )
        )
        code = PythonRenderer().render(ir)
        assert "import sys" in code
        assert "class Minimal:" in code
        assert "pass" in code

    def test_render_generated_code_is_valid_python(self):
        compiler = ConstructionCompiler()
        renderer = PythonRenderer()
        intent = Intent(
            kind=IntentKind.MUTATE_RESOURCE,
            target="valid.py",
            metadata={
                "imports": ["os"],
                "classes": [
                    {
                        "name": "Calculator",
                        "methods": [
                            {
                                "name": "add",
                                "params": ["a", "b"],
                                "body": "return a + b",
                            }
                        ]
                    }
                ]
            }
        )
        code = renderer.render(compiler.compile(intent))
        # Must be syntactically valid Python
        exec(compile(code, "test_construction_pipeline.py", "exec"), {})

    def test_render_with_decorators_and_docstrings(self):
        compiler = ConstructionCompiler()
        renderer = PythonRenderer()
        intent = Intent(
            kind=IntentKind.MUTATE_RESOURCE,
            target="deco.py",
            metadata={
                "imports": [],
                "classes": [
                    {
                        "name": "MyClass",
                        "decorators": ["dataclass"],
                        "docstring": "This is my class.",
                        "methods": [
                            {
                                "name": "greet",
                                "decorators": ["staticmethod"],
                                "docstring": "Say hello.",
                                "body": "return 'hello'",
                            }
                        ]
                    }
                ]
            }
        )
        code = renderer.render(compiler.compile(intent))
        assert "@dataclass" in code
        assert '"""This is my class."""' in code
        assert "@staticmethod" in code
        assert '"""Say hello."""' in code
        assert "def greet(self):" in code  # self is added by renderer

    def test_render_function_without_class(self):
        # Note: current ConstructionCompiler only processes classes, but ir supports functions
        from construction.ir import SourceFile, Function
        renderer = PythonRenderer()
        ir = SourceFile(
            functions=[
                Function(name="top_level", body="return 42")
            ]
        )
        code = renderer.render(ir)
        assert "def top_level(self):" in code
        assert "return 42" in code


class TestPipelineIntegration:
    def test_full_pipeline(self):
        from construction.ir import SourceFile
        compiler = ConstructionCompiler()
        renderer = PythonRenderer()
        intent = Intent(
            kind=IntentKind.MUTATE_RESOURCE,
            target="workspace.py",
            metadata={
                "imports": ["os", "pathlib"],
                "classes": [
                    {
                        "name": "Workspace",
                        "docstring": "A workspace representing a working context.",
                        "methods": [
                            {
                                "name": "resolve",
                                "params": ["path"],
                                "body": "return self.path.resolve()",
                            }
                        ]
                    }
                ]
            }
        )
        ir = compiler.compile(intent)
        assert isinstance(ir, SourceFile)
        code = renderer.render(ir)
        assert "import os" in code
        assert "import pathlib" in code
        assert 'class Workspace:' in code
        assert 'def resolve(self, path):' in code
        assert 'return self.path.resolve()' in code
