"""Testes do pipeline completo (Planner → Compiler → Executor)."""
import sys
import tempfile
from pathlib import Path

LIB_DIR = Path(__file__).parent.parent / "lib"
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))

import pytest
from planning.planner import Planner
from refactor.compiler import Compiler
from refactor.executor import OperationExecutor
from refactor.models import SourceFile, Class, Function, Code
from refactor.operations import CreateSourceFileOperation


class TestPipelineComplete:
    def test_pipeline_creates_file(self, tmp_path):
        """Pipeline completo cria arquivo com conteúdo."""
        sf = SourceFile(
            path=str(tmp_path / "test_module.py"),
            language="python",
            declarations=(
                Class(
                    name="TestModule",
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
        path = executor.execute(op)

        assert path.exists()
        content = path.read_text()
        assert "class TestModule:" in content
        assert "def run(self):" in content
