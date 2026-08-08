"""
AckTracker — máquina de estados para rastrear o ciclo de entrega de contexto.

Estados:
  IDLE       → aguardando envio de .file
  PENDING    → .file detectado, aguardando processamento
  PROCESSING → Generating detectado, aguardando resultado

Transições:
  IDLE       + .file snapshot.ctx → PENDING
  PENDING    + Generating         → PROCESSING
  PROCESSING + Error:             → FAIL  → IDLE
  PROCESSING + termiris_ctx)      → ACK   → IDLE
  PENDING/PROCESSING + timeout    → IDLE (permanece sem ACK)
"""

import time


class AckTracker:
    IDLE = "IDLE"
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"

    TIMEOUT_SECONDS = 120

    def __init__(self, store):
        self.store = store
        self.state = self.IDLE
        self.pending_hash = None
        self.saw_error = False
        self.state_since = None

    def observe(self, cleaned_text):
        if not cleaned_text:
            return

        # Verifica timeout primeiro
        if self.state in (self.PENDING, self.PROCESSING):
            if self.state_since and time.time() - self.state_since > self.TIMEOUT_SECONDS:
                self._reset()
                return

        # Detecta envio de .file
        if self.state == self.IDLE:
            if ".file" in cleaned_text and "snapshot.ctx" in cleaned_text:
                self.pending_hash = self.store.get_pending_hash()
                if self.pending_hash:
                    self.state = self.PENDING
                    self.saw_error = False
                    self.state_since = time.time()
                else:
                    pass  # .file sem hash pendente, ignora

        # Detecta início de processamento
        elif self.state == self.PENDING:
            if "Generating" in cleaned_text:
                self.state = self.PROCESSING
                self.state_since = time.time()

        # Detecta resultado durante processamento
        elif self.state == self.PROCESSING:
            if "Error:" in cleaned_text:
                self.saw_error = True
                self.store.mark_failed(
                    self.pending_hash,
                    reason="Error detected in terminal output",
                )
                self._reset()

            elif "termiris_ctx)" in cleaned_text and not self.saw_error:
                self.store.mark_ack(self.pending_hash)
                self._reset()

    def _reset(self):
        self.state = self.IDLE
        self.pending_hash = None
        self.saw_error = False
        self.state_since = None
