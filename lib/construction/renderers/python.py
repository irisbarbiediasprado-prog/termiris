from construction.ir import SourceFile, Class, Function, Import

class PythonRenderer:
    def render(self, ir: SourceFile) -> str:
        lines = []
        for imp in ir.imports:
            if imp.names:
                names = ", ".join(imp.names)
                lines.append(f"from {imp.module} import {names}")
            else:
                lines.append(f"import {imp.module}")
        if ir.imports:
            lines.append("")
        for cls in ir.classes:
            lines.extend(self._render_class(cls))
            lines.append("")
        for func in ir.functions:
            lines.extend(self._render_function(func))
            lines.append("")
        return "\n".join(lines).strip() + "\n"

    def _render_class(self, cls: Class) -> list:
        out = []
        for dec in cls.decorators:
            out.append(f"@{dec}")
        if cls.docstring:
            out.append(f'class {cls.name}:')
            out.append(f'    """{cls.docstring}"""')
        else:
            out.append(f'class {cls.name}:')
        if not cls.methods:
            out.append("    pass")
        else:
            for method in cls.methods:
                out.extend("    " + line for line in self._render_function(method))
        return out

    def _render_function(self, func: Function) -> list:
        out = []
        for dec in func.decorators:
            out.append(f"@{dec}")
        params = ", ".join(["self"] + func.params)
        sig = f"def {func.name}({params}):"
        out.append(sig)
        if func.docstring:
            out.append(f'    """{func.docstring}"""')
        if func.body:
            for line in func.body.strip().split("\n"):
                out.append(f"    {line}")
        else:
            out.append("    pass")
        return out
