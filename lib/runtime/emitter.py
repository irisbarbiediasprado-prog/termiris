import hashlib
import time
from pathlib import Path
from typing import List

from models import Artifact, ContextSnapshot


class SnapshotEmitter:
    def __init__(self, target_path: Path = None):
        self.target_path = target_path or (
            Path.home()
            / ".termiris"
            / "runtime"
            / "cache"
            / "state"
            / "snapshot.ctx"
        )

    def _serialize_artifact(self, artifact: Artifact) -> str:
        path = (
            getattr(artifact, "path", None)
            or getattr(artifact, "uri", None)
            or getattr(artifact, "name", None)
            or "<unknown>"
        )

        kind = getattr(artifact, "kind", "FILE")
        language = getattr(artifact, "language", "text")

        return f"""RESOURCE {{
  type: {kind}
  path: {path}
  language: {language}
}}

----- BEGIN CONTENT -----
{artifact.content.rstrip()}
----- END CONTENT -----"""

    def emit(self, generation: int, artifacts: List[Artifact]) -> ContextSnapshot:
        blocks = [
            self._serialize_artifact(a)
            for a in artifacts
        ]

        timestamp = int(time.time())

        full_text = f"""=== TERMIRIS SNAPSHOT ===
generation: {generation}
timestamp: {timestamp}
artifacts: {len(artifacts)}

{"\n\n".join(blocks)}

=== END SNAPSHOT ===
"""

        raw = full_text.encode("utf-8")
        snapshot_hash = hashlib.sha256(raw).hexdigest()[:16]

        self.target_path.parent.mkdir(parents=True, exist_ok=True)

        self.target_path.write_text(
            full_text,
            encoding="utf-8"
        )

        meta = self.target_path.with_suffix(".meta")

        meta.write_text(
            f"""snapshot_hash={snapshot_hash}
generation={generation}
timestamp={timestamp}
size_bytes={len(raw)}
artifacts={len(artifacts)}
""",
            encoding="utf-8",
        )

        return ContextSnapshot(
            generation=generation,
            snapshot_hash=snapshot_hash,
            artifacts=artifacts,
            size_bytes=len(raw),
            timestamp=time.time(),
        )
