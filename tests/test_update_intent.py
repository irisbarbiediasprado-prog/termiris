import sys
from pathlib import Path
LIB_DIR = Path(__file__).parent.parent / "lib"
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))

import pytest
from planning.planner import Planner
from refactor.compiler import Compiler
from refactor.operations import UpdateOperation

class TestUpdateIntent:
    def test_update_intent_fails_without_target_resolution(self):
        """Simbolo inexistente ainda falha mesmo com AnalysisIndex."""
        intent = "Atualizar ClasseInexistenteXYZ123 para resolver caminhos relativos ao Workspace"
        plan = Planner().plan(intent)
        compiler = Compiler()
        with pytest.raises(NotImplementedError, match="Intenção não reconhecida"):
            compiler.compile(plan)

    def test_update_intent_with_path_hint(self):
        """Com path explicito, passa."""
        intent = "Atualizar lib/refactor/executor.py:OperationExecutor para resolver caminhos relativos ao Workspace"
        plan = Planner().plan(intent)
        ops = Compiler().compile(plan)
        assert len(ops) == 1
        assert isinstance(ops[0], UpdateOperation)

    def test_update_intent_resolves_via_analysis_index(self):
        """v1: Sem path explicito, resolve via AnalysisIndex."""
        intent = "Atualizar OperationExecutor para resolver caminhos relativos ao Workspace"
        plan = Planner().plan(intent)
        ops = Compiler().compile(plan)
        assert len(ops) == 1
        assert isinstance(ops[0], UpdateOperation)
        assert "executor.py" in ops[0].target.path
