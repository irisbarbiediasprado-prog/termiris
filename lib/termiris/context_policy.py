import json
import time
from pathlib import Path


class ContextPolicy:
    def __init__(self, state_dir=None):
        self.state_dir = state_dir or (
            Path.home()
            / ".termiris"
            / "runtime"
            / "cache"
            / "state"
        )

        self.state_file = self.state_dir / "context.state"
        self.history_file = self.state_dir / "context.history.jsonl"

        self.state_dir.mkdir(parents=True, exist_ok=True)

    def check(self, snapshot_hash: str) -> dict:
        now = int(time.time())

        state = {}

        if self.state_file.exists():
            try:
                state = json.loads(
                    self.state_file.read_text()
                )
            except Exception:
                state = {}

        last_hash = state.get("last_hash")
        hits = state.get("hash_hits", 0)

        if snapshot_hash == last_hash:
            hits += 1
            event = "HASH_HIT"
        else:
            hits = 0
            event = "HASH_NEW"

        if hits <= 3:
            delay = hits * 30
            mode = "PA"
        else:
            delay = 90 * (2 ** (hits - 3))
            mode = "PG"

        result = {
            "hash": snapshot_hash,
            "event": event,
            "hash_hits": hits,
            "mode": mode,
            "delay": delay,
            "timestamp": now,
            "last_hash": snapshot_hash,   # para persistir a referência
        }

        self.state_file.write_text(
            json.dumps(result, indent=2),
            encoding="utf-8",
        )

        with self.history_file.open(
            "a",
            encoding="utf-8",
        ) as f:
            f.write(
                json.dumps(result)
                + "\n"
            )

        return result
