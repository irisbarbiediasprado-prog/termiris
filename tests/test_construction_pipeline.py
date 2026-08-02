"""Testes do pipeline de construção (Planner → Compiler)."""
import sys
from pathlib import Path

LIB_DIR = Path(__file__).parent.parent / "lib"
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))

import pytest
from planning.planner import Planner
from refactor.compiler import Compiler
from refactor.executor import OperationExecutor
from refactor.operations import CreateSourceFileOperation


class TestConstructionPipeline:
    def test_compiler_rejects_empty_module(self):
        """Compiler rejeita 'criar módulo' sem conteúdo."""
        planner = Planner()
        plan = planner.plan("criar módulo lib/foo.py")
        compiler = Compiler()

        with pytest.raises(ValueError, match="sem conteúdo"):
            compiler.compile(plan)
