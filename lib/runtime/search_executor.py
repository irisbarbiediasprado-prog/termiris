import shlex
import subprocess
from protocol.isa import PrimitiveISA, Operation
from protocol.executor import Executor
from models import Artifact, RuntimeResult


class SearchExecutor(Executor):
    def __init__(self, repository=None, emitter=None, state=None):
        self.repository = repository
        self.emitter = emitter
        self.state = state if state is not None else {}

    def can_handle(self, op: Operation) -> bool:
        return op.instruction == PrimitiveISA.SEARCH

    def execute(self, op: Operation) -> RuntimeResult:
        pattern = op.payload["pattern"]
        root = op.payload.get("root", ".")
        max_results = op.payload.get("max_results", 200)

        cmd = f"rg -n --no-heading {shlex.quote(pattern)} {shlex.quote(root)} --type py 2>/dev/null | head -n {max_results}"
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        raw_lines = proc.stdout.strip().splitlines() if proc.stdout else []

        matches = []
        for raw in raw_lines:
            parts = raw.split(":", 2)
            if len(parts) != 3:
                continue
            file, line, text = parts
            try:
                line_num = int(line)
            except ValueError:
                continue
            matches.append({"file": file, "line": line_num, "text": text})

        artifact = Artifact(
            uri=f"search://{pattern}",
            content="\n".join(raw_lines),
            metadata={
                "count": len(matches),
                "root": root,
                "matches": matches,
            },
        )

        self.state["generation"] = self.state.get("generation", 0) + 1
        snapshot = self.emitter.emit(self.state["generation"], [artifact])

        return RuntimeResult(
            success=True,
            snapshot=snapshot,
        )
