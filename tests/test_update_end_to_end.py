"""Testes end-to-end do pipeline de atualização (UpdateOperation).

Valida que o Termiris consegue modificar a si mesmo via pipeline.
"""
import sys
from pathlib import Path

LIB_DIR = Path(__file__).parent.parent / "lib"
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))

import pytest
from planning.planner import Planner
from refactor.compiler import Compiler
from refactor.executor import OperationExecutor
from refactor.operations import UpdateOperation
from refactor.models import Target, Transformation, Code


class TestUpdatePipeline:
    def test_compiler_creates_update_operation(self):
        """Compiler gera UpdateOperation para intenção de atualização."""
        intent = "Atualizar lib/refactor/executor.py:OperationExecutor para resolver caminhos relativos ao Workspace"
        plan = Planner().plan(intent)
        ops = Compiler().compile(plan)

        assert len(ops) == 1
        assert isinstance(ops[0], UpdateOperation)
        assert ops[0].target.path == "lib/refactor/executor.py"
        assert ops[0].target.symbol == "OperationExecutor"
        assert ops[0].transformation.kind == "replace_body"

    def test_update_operation_executes(self, tmp_path):
        """UpdateOperation modifica arquivo real."""
        # Cria arquivo alvo
        target_file = tmp_path / "target.py"
        target_file.write_text("""\
class Target:
    def execute(self):
        return "old"
""")

        # Cria UpdateOperation manualmente
        op = UpdateOperation(
            kind="update",
            reference=str(target_file),
            target=Target(
                path=str(target_file),
                symbol="Target.execute",
            ),
            transformation=Transformation(
                kind="replace_body",
                value=Code("python", """\
        return "new"
"""),
            ),
        )

        executor = OperationExecutor()
        result = executor.execute(op)

        content = result.read_text()
        assert '"new"' in content
        assert '"old"' not in content

    def test_full_pipeline_update(self, tmp_path):
        """Pipeline completo: Planner → Compiler → Executor."""
        # Cria arquivo alvo
        target_file = tmp_path / "service.py"
        target_file.write_text("""\
class Service:
    def run(self):
        return "before"
""")

        intent = f"Atualizar {target_file}:Service.run para retornar 'after'"
        plan = Planner().plan(intent)
        ops = Compiler().compile(plan)

        assert len(ops) == 1
        assert isinstance(ops[0], UpdateOperation)

        executor = OperationExecutor()
        result = executor.execute(ops[0])

        content = result.read_text()
        assert "before" not in content

    def test_update_without_path_resolves_via_analysis(self):
        """Sem path explícito, Compiler resolve via Analysis IR."""
        intent = "Atualizar OperationExecutor para resolver caminhos relativos ao Workspace"
        plan = Planner().plan(intent)

        try:
            ops = Compiler().compile(plan)
            assert len(ops) == 1
            assert isinstance(ops[0], UpdateOperation)
        except NotImplementedError:
            pytest.skip("Resolução via Analysis IR ainda não implementada")
