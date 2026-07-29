import json
from pathlib import Path

from .sink import EventSink

DEFAULT_PATH = Path.home() / ".termiris" / "runtime" / "events.jsonl"


class JsonlEventSink(EventSink):
    def __init__(self, path=None):
        self.path = Path(path) if path else DEFAULT_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def publish(self, event: dict) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            json.dump(event, f, ensure_ascii=False)
            f.write("\n")

    def close(self) -> None:
        pass
