"""Testes do pipeline incompleto (sem executor para alguns casos)."""
import sys
import tempfile
from pathlib import Path

LIB_DIR = Path(__file__).parent.parent / "lib"
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))

import pytest
from planning.planner import Planner
from refactor.compiler import Compiler


class TestPipelineIncomplete:
    def test_pipeline_fails_without_content(self):
        """Pipeline falha quando intenção não tem conteúdo."""
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "test_module.py"
            planner = Planner()
            plan = planner.plan(f"criar módulo {file_path}")
            compiler = Compiler()

            with pytest.raises(ValueError, match="sem conteúdo"):
                compiler.compile(plan)
