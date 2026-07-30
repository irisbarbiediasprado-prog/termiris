from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "lib"


def read(relpath: str) -> str:
    return (ROOT / relpath).read_text()


def test_backend_registry_exists():
    assert (ROOT / "protocol/backend_registry.py").exists()


def test_executor_registry_exists():
    assert (ROOT / "protocol/executor_registry.py").exists()


def test_compiler_returns_migration_plan():
    compiler = read("protocol/compiler.py")
    assert "-> MigrationPlan" in compiler
    assert "PrimitiveISA" not in compiler


def test_backend_owns_primitive_isa():
    backend = read("protocol/isa_backend.py")
    assert "PrimitiveISA" in backend


def test_backend_contract_exists():
    backend = read("protocol/backend.py")
    assert "class Backend" in backend


def test_executor_contract_exists():
    executor = read("protocol/executor.py")
    assert "class Executor" in executor
