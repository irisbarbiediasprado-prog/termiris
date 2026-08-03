from pathlib import Path

class Workspace:
    def __init__(self, root: Path | None = None):
        self.root = Path(root) if root is not None else Path.cwd()
    def resolve(self, path: str | Path) -> Path:
        p = Path(path)
        if not p.is_absolute():
            p = self.root / p
        return p.resolve()
