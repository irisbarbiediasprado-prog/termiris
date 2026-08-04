from pathlib import Path
from protocol.isa import PrimitiveISA, Operation
from protocol.executor import Executor
from protocol.ir import Intent, IntentKind
from models import Artifact, RuntimeResult
from construction.compiler import ConstructionCompiler
from construction.renderers.python import PythonRenderer


class ConstructionExecutor(Executor):
    def __init__(self, repository=None, emitter=None, state=None):
        self.repository = repository
        self.emitter = emitter
        self.state = state if state is not None else {}

    def can_handle(self, op: Operation) -> bool:
        return op.instruction == PrimitiveISA.BUILD

    def execute(self, op: Operation) -> RuntimeResult:
        intent_data = op.payload.get("intent")
        if not intent_data:
            return RuntimeResult(success=False, error="Payload sem intent")

        # Reconstrói Intent a partir do dict, aceitando kind como str ou int
        kind_raw = intent_data["kind"]
        if isinstance(kind_raw, str):
            kind = IntentKind[kind_raw]
        elif isinstance(kind_raw, int):
            kind = IntentKind(kind_raw)
        else:
            kind = kind_raw

        intent = Intent(
            kind=kind,
            target=intent_data["target"],
            metadata=intent_data.get("metadata", {}),
        )

        compiler = ConstructionCompiler()
        ir = compiler.compile(intent)
        renderer = PythonRenderer()
        code = renderer.render(ir)

        target_path = Path(op.payload.get("path", intent.target))
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(code)

        artifact = Artifact(
            uri=f"file://{target_path.resolve()}",
            content=code,
            metadata={"path": str(target_path), "size": len(code)},
        )

        self.state["generation"] = self.state.get("generation", 0) + 1
        snapshot = self.emitter.emit(self.state["generation"], [artifact])
        return RuntimeResult(success=True, snapshot=snapshot)
