from pathlib import Path
from abc import ABC, abstractmethod

class TargetResolver(ABC):
    @abstractmethod
    def resolve(self, symbol: str) -> Path | None:...

class FileSystemTargetResolver(TargetResolver):
    def __init__(self, root: Path = Path("lib")):
        self.root = Path(root)
    def resolve(self, symbol: str) -> Path | None:
        base = symbol.split(":")[-1].split(".")[0]
        for py in self.root.rglob("*.py"):
            try:
                if f"class {base}" in py.read_text():
                    return py
            except:
                continue
        return None

class AnalysisIndexTargetResolver(TargetResolver):
    """v1.1 - fast por padrão (1.88s), full atrás de flag."""
    _GLOBAL_CACHE: dict[tuple[str, str], dict[str, Path]] = {}

    def __init__(self, root: Path = Path("lib"), mode: str = "fast"):
        self.root = Path(root).resolve()
        self.mode = mode # "fast" ou "full"
        self._cache_key = (str(self.root), self.mode)
        if self._cache_key not in self._GLOBAL_CACHE:
            if mode == "full":
                self._GLOBAL_CACHE[self._cache_key] = self._build_full()
            else:
                self._GLOBAL_CACHE[self._cache_key] = self._build_fast()
        self._symbol_to_path = self._GLOBAL_CACHE[self._cache_key]

    def _build_fast(self) -> dict[str, Path]:
        import ast
        index: dict[str, Path] = {}
        for py in self.root.rglob("*.py"):
            try:
                tree = ast.parse(py.read_text(), filename=str(py))
                for node in tree.body:
                    if isinstance(node, ast.ClassDef):
                        index[node.name] = py
                        for item in node.body:
                            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                                index[f"{node.name}.{item.name}"] = py
                    elif isinstance(node, ast.FunctionDef):
                        index.setdefault(node.name, py)
            except Exception:
                continue
        return index

    def _build_full(self) -> dict[str, Path]:
        from analysis.analyzer import Analyzer
        analyzer = Analyzer()
        index: dict[str, Path] = {}
        for py in self.root.rglob("*.py"):
            try:
                idx = analyzer.analyze(py.read_text())
                for cls in idx.classes:
                    index[cls.name] = py
                for func in idx.functions:
                    index.setdefault(func.name, py)
            except Exception:
                continue
        return index

    def resolve(self, symbol: str) -> Path | None:
        if ":" in symbol:
            symbol = symbol.rsplit(":", 1)[-1]
        base = symbol.split(".")[0]
        return self._symbol_to_path.get(symbol) or self._symbol_to_path.get(base)

    @classmethod
    def clear_cache(cls):
        cls._GLOBAL_CACHE.clear()
