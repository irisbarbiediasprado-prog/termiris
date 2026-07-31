from pathlib import Path


class ProjectScanner:
    def __init__(self, root: str | Path):
        self.root = Path(root)

    def scan(self) -> tuple[Path, ...]:
        return tuple(
            sorted(
                p for p in self.root.rglob("*.py")
                if p.is_file()
            )
        )
