from datetime import datetime
from pathlib import Path
from typing import Optional

class SocketTap:
    def __init__(self, log_file: Optional[Path] = None):
        self.log_file = log_file or Path.home() / ".termiris/runtime/socket_tap.log"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def record(self, seq: int, raw_bytes: bytes, buffer_before: str, buffer_after: str, cleaned: str):
        """Registra apenas fatos observáveis do transporte."""
        timestamp = datetime.now().isoformat()
        decoded = raw_bytes.decode("utf-8", errors="replace")
        raw_hex = raw_bytes.hex()

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write(f"RECV #{seq}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"LEN: {len(raw_bytes)}\n")
            f.write(f"REPR: {repr(raw_bytes)}\n")
            f.write(f"HEX: {raw_hex[:80]}{'...' if len(raw_hex) > 80 else ''}\n")
            f.write(f"DECODED: {repr(decoded)}\n")
            f.write(f"CLEANED: {repr(cleaned)}\n")
            f.write(f"BUFFER_BEFORE: {repr(buffer_before)}\n")
            f.write(f"BUFFER_AFTER: {repr(buffer_after)}\n")
            f.write("=" * 80 + "\n\n")
