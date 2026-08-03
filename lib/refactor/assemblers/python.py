import libcst as cst
import textwrap
from ..models import SourceFile, Class, Function, Code
from .base import Assembler


class PythonAssembler(Assembler):
    """Monta código Python a partir de SourceFile usando LibCST."""

    def assemble(self, source_file: SourceFile) -> str:
        statements = []

        # Imports
        for imp in source_file.imports:
            statements.append(cst.parse_statement(imp))

        # Declarações (classes e funções)
        for decl in source_file.declarations:
            if isinstance(decl, Class):
                statements.append(self._assemble_class(decl))
            elif isinstance(decl, Function):
                statements.append(self._assemble_function(decl))

        if not statements:
            return ""

        module = cst.Module(body=statements)
        return module.code

    def _assemble_class(self, cls: Class) -> cst.ClassDef:
        body = []
        for method in cls.methods:
            body.append(self._assemble_function(method))

        return cst.ClassDef(
            name=cst.Name(cls.name),
            body=cst.IndentedBlock(body=body),
        )

    def _assemble_function(self, func: Function) -> cst.FunctionDef:
        # Monta parâmetros a partir da assinatura
        params = self._parse_signature(func.signature)

        # Remove indentação do corpo antes de parsear
        body_source = textwrap.dedent(func.body.source).strip()
        body_nodes = cst.parse_module(body_source).body

        return cst.FunctionDef(
            name=cst.Name(func.name),
            params=cst.Parameters(params=params),
            body=cst.IndentedBlock(body=body_nodes),
        )

    def _parse_signature(self, signature: str) -> list[cst.Param]:
        """Converte assinatura como '(self, a: int)' em lista de cst.Param."""
        # Remove parênteses externos
        sig = signature.strip()
        if sig.startswith("(") and sig.endswith(")"):
            sig = sig[1:-1]

        if not sig.strip():
            return []

        params = []
        for part in self._split_params(sig):
            part = part.strip()
            if not part:
                continue

            # Separa default (=)
            default = None
            if "=" in part:
                name_part, default_part = part.rsplit("=", 1)
                part = name_part.strip()
                default = cst.parse_expression(default_part.strip())

            # Separa anotação (:)
            annotation = None
            if ":" in part:
                name_part, type_part = part.rsplit(":", 1)
                name = name_part.strip()
                type_str = type_part.strip()
                annotation = cst.Annotation(
                    cst.parse_expression(type_str)
                )
            else:
                name = part

            params.append(
                cst.Param(
                    name=cst.Name(name),
                    annotation=annotation,
                    default=default,
                )
            )

        return params

    def _split_params(self, sig: str) -> list[str]:
        """Divide parâmetros respeitando Union types com |."""
        parts = []
        current = []
        depth = 0

        for char in sig:
            if char in "([{":
                depth += 1
            elif char in ")]}":
                depth -= 1

            if char == "," and depth == 0:
                parts.append("".join(current).strip())
                current = []
            else:
                current.append(char)

        if current:
            parts.append("".join(current).strip())

        return parts
