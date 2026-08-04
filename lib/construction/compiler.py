from protocol.ir import Intent, IntentKind
from construction.ir import SourceFile, Class, Function, Import

class ConstructionCompiler:
    def compile(self, intent: Intent) -> SourceFile:
        if intent.kind != IntentKind.MUTATE_RESOURCE:
            raise ValueError(f"ConstructionCompiler só suporta MUTATE_RESOURCE, recebido {intent.kind}")
        meta = intent.metadata
        imports = [Import(module=m) for m in meta.get("imports", [])]
        classes = []
        for cls_data in meta.get("classes", []):
            methods = []
            for m in cls_data.get("methods", []):
                methods.append(Function(
                    name=m["name"],
                    params=m.get("params", []),
                    body=m.get("body", ""),
                    docstring=m.get("docstring"),
                    decorators=m.get("decorators", []),
                ))
            classes.append(Class(
                name=cls_data["name"],
                methods=methods,
                docstring=cls_data.get("docstring"),
                decorators=cls_data.get("decorators", []),
            ))
        return SourceFile(
            imports=imports,
            classes=classes,
        )
