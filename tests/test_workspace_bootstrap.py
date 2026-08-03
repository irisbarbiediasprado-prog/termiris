"""Testes do bootstrap do Workspace via pipeline."""
import sys
from pathlib import Path
LIB_DIR = Path(__file__).parent.parent / "lib"
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))

import pytest
from planning.planner import Planner
from refactor.compiler import Compiler
from refactor.executor import OperationExecutor
from refactor.operations import CreateSourceFileOperation, UpdateOperation
from refactor.models import SourceFile, Class, Function, Code, Target, Transformation

class TestWorkspaceBootstrap:
    def test_create_workspace_module(self, tmp_path):
        sf = SourceFile(
            path=str(tmp_path / "workspace.py"),
            language="python",
            imports=("from pathlib import Path",),
            declarations=(Class(name="Workspace", methods=(Function(name="resolve", signature="(self, path)", body=Code("python", "if not path.is_absolute():\n path = self.root / path\nreturn path")),)),)
        )
        op = CreateSourceFileOperation(kind="create_source_file", reference=sf.path, source_file=sf)
        result = OperationExecutor().execute(op)
        assert "class Workspace:" in result.read_text()

    def test_compiler_creates_workspace_from_intent(self, tmp_path):
        target = tmp_path / "workspace.py"
        ops = Compiler().compile(Planner().plan(f"criar modulo {target} com classe Workspace"))
        assert len(ops) == 1

    def test_add_declaration_to_existing_file(self, tmp_path):
        target = tmp_path / "executor.py"
        target.write_text('''from pathlib import Path

class OperationExecutor:
    def execute(self, operation):
        path = Path(operation.payload["path"])
        return path
''')
        cls = Class(name="Workspace", methods=(Function(name="resolve", signature="(self, path)", body=Code("python", "return path")),))
        op = UpdateOperation(kind="update", reference=str(target), target=Target(path=str(target)), transformation=Transformation(kind="add_declaration", value=cls))
        content = OperationExecutor().execute(op).read_text()
        assert "class Workspace:" in content
        assert "class OperationExecutor:" in content

    def test_full_workspace_bootstrap(self, tmp_path):
        workspace_path = tmp_path / "workspace.py"
        ops_1 = Compiler().compile(Planner().plan(f"criar modulo {workspace_path} com classe Workspace"))
        OperationExecutor().execute(ops_1[0])
        assert workspace_path.exists()

        executor_path = tmp_path / "executor.py"
        executor_path.write_text('''from pathlib import Path

class OperationExecutor:
    def execute(self, operation):
        path = Path(operation.payload["path"])
        return path
''')

        ops_3 = Compiler().compile(Planner().plan(f"Adicionar classe Workspace em {executor_path}"))
        OperationExecutor().execute(ops_3[0])
        assert "class Workspace:" in executor_path.read_text()

        ops_4 = Compiler().compile(Planner().plan(f"Atualizar {executor_path}:OperationExecutor para resolver caminhos relativos ao Workspace"))
        OperationExecutor().execute(ops_4[0])
        content_4 = executor_path.read_text()
        assert "self.workspace.resolve" in content_4
        assert "class Workspace:" in content_4
