"""
ContextAckStore — rastreia o ciclo de entrega de contexto.

Estados:
  pending.hash  → contexto enviado, aguardando confirmação
  ack.hash      → contexto confirmado pelo servidor
  failure.hash  → contexto falhou (erro explícito)

Uso:
  store = ContextAckStore()
  store.mark_pending("abc123")
  store.mark_ack("abc123")
  store.mark_failed("abc123", reason="...")
"""

import time
from pathlib import Path


class ContextAckStore:
    def __init__(self, base_dir=None):
        if base_dir is None:
            base_dir = (
                Path.home()
                / ".termiris"
                / "runtime"
                / "cache"
                / "context"
            )
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

        self.pending_file = self.base_dir / "pending.hash"
        self.ack_file = self.base_dir / "ack.hash"
        self.failure_file = self.base_dir / "failure.hash"
        self.meta_file = self.base_dir / "ack_meta.log"

    def mark_pending(self, hash_value, **meta):
        self.pending_file.write_text(hash_value, encoding="utf-8")
        self._log_meta("PENDING", hash_value, meta)

    def mark_ack(self, hash_value, **meta):
        self.ack_file.write_text(hash_value, encoding="utf-8")
        # Remove pending ao confirmar
        if self.pending_file.exists():
            self.pending_file.unlink()
        # Remove failure se existir
        if self.failure_file.exists():
            self.failure_file.unlink()
        self._log_meta("ACK", hash_value, meta)

    def mark_failed(self, hash_value, reason="", **meta):
        self.failure_file.write_text(hash_value, encoding="utf-8")
        # Remove pending ao falhar
        if self.pending_file.exists():
            self.pending_file.unlink()
        meta["reason"] = reason
        self._log_meta("FAIL", hash_value, meta)

    def get_pending_hash(self):
        return self._read(self.pending_file)

    def get_ack_hash(self):
        return self._read(self.ack_file)

    def get_failure_hash(self):
        return self._read(self.failure_file)

    def is_pending(self, hash_value):
        return self.get_pending_hash() == hash_value

    def is_acked(self, hash_value):
        return self.get_ack_hash() == hash_value

    def is_failed(self, hash_value):
        return self.get_failure_hash() == hash_value

    def clear(self):
        for f in (self.pending_file, self.ack_file, self.failure_file):
            if f.exists():
                f.unlink()

    def _read(self, path):
        try:
            return path.read_text(encoding="utf-8").strip()
        except FileNotFoundError:
            return None

    def _log_meta(self, event, hash_value, meta):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        line = f"{timestamp} {event} hash={hash_value}"
        if meta:
            line += f" meta={meta}"
        with open(self.meta_file, "a", encoding="utf-8") as f:
            f.write(line + "\n")
