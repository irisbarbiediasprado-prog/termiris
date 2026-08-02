"""Testes end-to-end do pipeline de construção.

Valida o fluxo completo:
SourceFile → Assembler → Operation → Executor → Arquivo
"""
import sys
from pathlib import Path

# Garante que lib/ está no path
LIB_DIR = Path(__file__).parent.parent / "lib"
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))

import pytest

from refactor.models import SourceFile, Class, Function, Code
from refactor.assemblers.python import PythonAssembler
from refactor.operations import CreateSourceFileOperation
from refactor.executor import OperationExecutor
from refactor.compiler import Compiler
from planning.planner import Planner


class TestConstructionPipeline:
    """Testes end-to-end do pipeline de construção."""

    def test_assemble_simple_class(self):
        """Assembler gera código Python a partir de SourceFile."""
        sf = SourceFile(
            path="lib/foo.py",
            language="python",
            imports=("import os",),
            declarations=(
                Class(
                    name="Foo",
                    methods=(
                        Function(
                            name="bar",
                            signature="(self)",
                            body=Code("python", "        return 42"),
                        ),
                    ),
                ),
            ),
        )

        assembler = PythonAssembler()
        code = assembler.assemble(sf)

        assert "import os" in code
        assert "class Foo:" in code
        assert "def bar(self):" in code
        assert "return 42" in code

    def test_assemble_function_with_params(self):
        """Assembler gera função com parâmetros tipados."""
        sf = SourceFile(
            path="lib/foo.py",
            language="python",
            declarations=(
                Function(
                    name="add",
                    signature="(a: int, b: int)",
                    body=Code("python", "        return a + b"),
                ),
            ),
        )

        assembler = PythonAssembler()
        code = assembler.assemble(sf)

        assert "def add(a: int, b: int):" in code
        assert "return a + b" in code

    def test_executor_creates_file(self, tmp_path):
        """Executor cria arquivo no filesystem."""
        sf = SourceFile(
            path=str(tmp_path / "created.py"),
            language="python",
            declarations=(
                Class(
                    name="Created",
                    methods=(
                        Function(
                            name="run",
                            signature="(self)",
                            body=Code("python", "        pass"),
                        ),
                    ),
                ),
            ),
        )

        op = CreateSourceFileOperation(
            kind="create_source_file",
            reference=sf.path,
            source_file=sf,
        )

        executor = OperationExecutor()
        result = executor.execute(op)

        assert result.exists()
        content = result.read_text()
        assert "class Created:" in content
        assert "def run(self):" in content

    def test_compiler_rejects_empty_source_file(self):
        """Compiler rejeita SourceFile vazio."""
        plan = Planner().plan("criar arquivo lib/novo.py")
        with pytest.raises(ValueError, match="sem conteúdo"):
            Compiler().compile(plan)


class TestBootstrapScenario:
    """Testes que simulam o bootstrap real do Termiris."""

    def test_create_search_executor_module(self, tmp_path):
        """Cria o SearchExecutor via pipeline (bootstrapping)."""
        sf = SourceFile(
            path=str(tmp_path / "search_executor.py"),
            language="python",
            imports=("from abc import ABC, abstractmethod",),
            declarations=(
                Class(
                    name="SearchExecutor",
                    methods=(
                        Function(
                            name="execute",
                            signature="(self, query: str)",
                            body=Code("python", '''        print(f"Searching for: {query}")'''),
                        ),
                    ),
                ),
            ),
        )

        op = CreateSourceFileOperation(
            kind="create_source_file",
            reference=sf.path,
            source_file=sf,
        )

        executor = OperationExecutor()
        path = executor.execute(op)

        content = path.read_text()
        assert "from abc import ABC, abstractmethod" in content
        assert "class SearchExecutor:" in content
        assert "def execute(self, query: str):" in content
        assert 'print(f"Searching for: {query}")' in content

    def test_create_list_executor_module(self, tmp_path):
        """Cria o ListExecutor via pipeline (bootstrapping)."""
        sf = SourceFile(
            path=str(tmp_path / "list_executor.py"),
            language="python",
            imports=(
                "from pathlib import Path",
                "from typing import Dict",
            ),
            declarations=(
                Class(
                    name="ListExecutor",
                    methods=(
                        Function(
                            name="execute",
                            signature="(self, operation)",
                            body=Code("python", '''        path = Path(operation.payload["path"])
        entries = []
        for entry in sorted(path.iterdir()):
            entries.append(entry.name)
        return entries'''),
                        ),
                    ),
                ),
            ),
        )

        op = CreateSourceFileOperation(
            kind="create_source_file",
            reference=sf.path,
            source_file=sf,
        )

        executor = OperationExecutor()
        path = executor.execute(op)

        content = path.read_text()
        assert "from pathlib import Path" in content
        assert "class ListExecutor:" in content
        assert "def execute(self, operation):" in content
        assert 'operation.payload["path"]' in content

    def test_create_module_with_multiple_functions(self, tmp_path):
        """Cria módulo com múltiplas funções."""
        sf = SourceFile(
            path=str(tmp_path / "utils.py"),
            language="python",
            declarations=(
                Function(
                    name="helper_a",
                    signature="(x: int)",
                    body=Code("python", "        return x * 2"),
                ),
                Function(
                    name="helper_b",
                    signature="(y: str)",
                    body=Code("python", "        return y.upper()"),
                ),
            ),
        )

        op = CreateSourceFileOperation(
            kind="create_source_file",
            reference=sf.path,
            source_file=sf,
        )

        executor = OperationExecutor()
        path = executor.execute(op)

        content = path.read_text()
        assert "def helper_a(x: int):" in content
        assert "return x * 2" in content
        assert "def helper_b(y: str):" in content
        assert "return y.upper()" in content


class TestCodeAbstraction:
    """Testes da abstração Code (linguagem + source)."""

    def test_code_is_language_agnostic(self):
        """Code pode representar qualquer linguagem."""
        python_code = Code("python", "print('hello')")
        bash_code = Code("bash", "echo hello")
        json_code = Code("json", '{"hello": "world"}')

        assert python_code.language == "python"
        assert bash_code.language == "bash"
        assert json_code.language == "json"

    def test_code_with_empty_source(self):
        """Code com source vazio é válido."""
        code = Code("python", "")
        assert code.source == ""
