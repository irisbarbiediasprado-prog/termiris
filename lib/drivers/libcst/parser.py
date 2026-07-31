from pathlib import Path
import libcst


def parse_source(source: str) -> libcst.Module:
    return libcst.parse_module(source)


def parse_file(path) -> libcst.Module:
    return parse_source(Path(path).read_text())
