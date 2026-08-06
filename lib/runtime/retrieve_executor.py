from pathlib import Path
from datetime import datetime, timezone

from protocol.executor import Executor
from protocol.isa import Operation
from models import Artifact, RuntimeResult


def _now():
    return datetime.now(timezone.utc).isoformat()


def _status(target, state):
    generation = state.get("generation", 0)

    return Artifact(
        uri="status://current",
        content=(
            "BEGIN STATUS\n\n"
            f"generation: {generation}\n"
            f"artifact_count: {len(state.get('artifacts', []))}\n"
            "\nEND STATUS\n"
        ),
        metadata={
            "kind": "status",
            "source": "runtime",
            "produced_at": _now(),
        },
    )


def _analysis(target, state):
    path = Path.home() / ".termiris/runtime/cache/analysis/architecture.md"

    if path.exists():
        content = path.read_text(encoding="utf-8")
    else:
        content = (
            "BEGIN ANALYSIS\n\n"
            "open_questions:\n"
            "discarded_alternatives:\n"
            "architectural_tensions:\n"
            "future_directions:\n\n"
            "END ANALYSIS\n"
        )

    return Artifact(
        uri="analysis://architecture",
        content=content,
        metadata={
            "kind": "analysis",
            "source": "static",
            "produced_at": _now(),
        },
    )


def _handover(target, state):
    status = _status("", state)
    analysis = _analysis("", state)

    return Artifact(
        uri="handover://current",
        content="\n\n".join([
            "BEGIN HANDOVER",
            status.content,
            analysis.content,
            "END HANDOVER",
        ]),
        metadata={
            "kind": "handover",
            "source": "composition",
            "produced_at": _now(),
        },
    )


def _file(target, state):
    path = Path(target)

    if not path.exists():
        return Artifact(
            uri=f"file://{target}",
            content="",
            metadata={
                "kind": "file",
                "error": "NOT_FOUND",
                "produced_at": _now(),
            },
        )

    return Artifact(
        uri=f"file://{path.resolve()}",
        content=path.read_text(encoding="utf-8"),
        metadata={
            "kind": "file",
            "source": "filesystem",
            "produced_at": _now(),
        },
    )


_PROVIDERS = {
    "FILE": _file,
    "STATUS": _status,
    "ANALYSIS": _analysis,
    "HANDOVER": _handover,
}


class RetrieveExecutor(Executor):

    def __init__(self, repository=None, emitter=None, state=None):
        self.repository = repository
        self.emitter = emitter
        self.state = state if state is not None else {}

    def execute(self, op: Operation) -> RuntimeResult:
        Path.home().joinpath(".termiris/runtime/retrieve.trace").write_text(repr(op.payload)+"\n", encoding="utf-8")
        provider = op.payload.get("resource_type", "FILE").upper()
        target = op.payload.get("target", "")

        if provider not in _PROVIDERS:
            return RuntimeResult(
                success=False,
                error=f"Retrieve provider desconhecido: {provider}",
            )

        artifact = _PROVIDERS[provider](target, self.state)

        self.state["generation"] = self.state.get("generation", 0) + 1

        if self.emitter:
            snapshot = self.emitter.emit(
                self.state["generation"],
                [artifact],
            )
            return RuntimeResult(success=True, snapshot=snapshot)

        return RuntimeResult(success=True, snapshot=None)
