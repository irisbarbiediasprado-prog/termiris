from pathlib import Path
from.operations import Operation, CreateFileOperation, CreateSourceFileOperation, UpdateOperation
from.models import SourceFile
from.assemblers import PythonAssembler
from.workspace import Workspace
import libcst as cst
import textwrap

class OperationExecutor:
    def __init__(self, assemblers=None, workspace=None):
        self.assemblers = assemblers or {"python": PythonAssembler(),}
        self.workspace = workspace or Workspace()
    def execute(self, operation: Operation) -> Path:
        if isinstance(operation, CreateFileOperation):
            path = self.workspace.resolve(operation.path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(operation.content)
            return path
        if isinstance(operation, CreateSourceFileOperation):
            sf = operation.source_file
            assembler = self.assemblers.get(sf.language)
            content = assembler.assemble(sf)
            path = self.workspace.resolve(sf.path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            return path
        if isinstance(operation, UpdateOperation):
            return self._apply_update(operation)
        raise NotImplementedError
    def _apply_update(self, operation: UpdateOperation) -> Path:
        path = self.workspace.resolve(operation.target.path)
        if not path.exists():
            raise FileNotFoundError(f"Arquivo nao encontrado: {path}")
        content = path.read_text()
        kind = operation.transformation.kind
        if kind == "replace_body": content = self._replace_body(content, operation)
        elif kind == "replace_import": content = self._replace_import(content, operation)
        elif kind == "add_declaration": content = self._add_declaration(content, operation)
        elif kind == "add_import": content = self._add_import(content, operation)
        elif kind == "add_method": content = self._add_method(content, operation)
        else: raise NotImplementedError(kind)
        path.write_text(content)
        return path
    def _replace_body(self, content: str, operation: UpdateOperation) -> str:
        symbol = operation.target.symbol or ""
        if "." in symbol:
            class_name, method_name = symbol.rsplit(".", 1)
        else:
            class_name = symbol if symbol == "OperationExecutor" else None
            method_name = "execute" if symbol == "OperationExecutor" else symbol
        tree = cst.parse_module(content)
        class Rep(cst.CSTTransformer):
            def __init__(self, cn, mn, nb):
                self.cn = cn; self.mn = mn; self.nb = nb; self.stack = []
            def visit_ClassDef(self, node):
                self.stack.append(node.name.value); return True
            def leave_ClassDef(self, o, u):
                self.stack.pop(); return u
            def leave_FunctionDef(self, o, u):
                in_target = self.cn is None or (self.stack and self.stack[-1] == self.cn)
                if o.name.value == self.mn and in_target:
                    src = textwrap.dedent(self.nb).strip()
                    nodes = cst.parse_module(src).body
                    return u.with_changes(body=cst.IndentedBlock(body=nodes))
                return u
        return tree.visit(Rep(class_name, method_name, operation.transformation.value.source)).code
    def _replace_import(self, content: str, operation: UpdateOperation) -> str:
        old = operation.transformation.value.get("old"); new = operation.transformation.value.get("new")
        tree = cst.parse_module(content)
        class R(cst.CSTTransformer):
            def leave_Import(self, o, u):
                ns = []
                for a in u.names:
                    if a.name.value == old: ns.append(a.with_changes(name=cst.Name(new)))
                    else: ns.append(a)
                return u.with_changes(names=ns)
        return tree.visit(R()).code
    def _add_import(self, content: str, operation: UpdateOperation) -> str:
        stmt = operation.transformation.value.strip()
        if stmt in content: return content
        tree = cst.parse_module(content)
        node = cst.parse_statement(stmt + "\n")
        body = list(tree.body); last = -1
        for i, s in enumerate(body):
            if isinstance(s, (cst.Import, cst.ImportFrom)): last = i
        body.insert(last+1 if last>=0 else 0, node)
        return cst.Module(body=body).code
    def _add_declaration(self, content: str, operation: UpdateOperation) -> str:
        assembler = PythonAssembler()
        sf = SourceFile(path="__temp__.py", language="python", declarations=(operation.transformation.value,))
        code = assembler.assemble(sf)
        tree = cst.parse_module(content)
        add = cst.parse_module(code).body
        return tree.with_changes(body=list(tree.body)+list(add)).code
    def _add_method(self, content: str, operation: UpdateOperation) -> str:
        target_class = operation.target.symbol
        func = operation.transformation.value
        assembler = PythonAssembler()
        tree = cst.parse_module(content)
        class AM(cst.CSTTransformer):
            def leave_ClassDef(self, o, u):
                if o.name.value == target_class:
                    m = assembler._assemble_function(func)
                    nb = list(u.body.body)+[m]
                    return u.with_changes(body=u.body.with_changes(body=nb))
                return u
        return tree.visit(AM()).code
