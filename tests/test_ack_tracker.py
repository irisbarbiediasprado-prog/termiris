#!/usr/bin/env python3
"""
Testes unitários para o AckTracker.

Princípio:
  A mesma sequência de eventos observada no TAP deve produzir
  a mesma decisão no teste, sem MITL, sem socket e sem backend.
"""

import sys
import time
from pathlib import Path

import pytest

LIB_DIR = Path.home() / ".termiris" / "lib"
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))

from runtime.context_ack import ContextAckStore
from runtime.ack_tracker import AckTracker


@pytest.fixture
def ack_store(tmp_path):
    """Cria um ContextAckStore isolado em diretório temporário."""
    return ContextAckStore(base_dir=tmp_path / "context")


@pytest.fixture
def tracker(ack_store):
    """Cria um AckTracker com store isolado."""
    return AckTracker(ack_store)


class TestBasicTransitions:
    """Transições fundamentais da máquina de estados."""

    def test_idle_to_pending_on_file_detection(self, tracker, ack_store):
        """.file snapshot.ctx → PENDING"""
        ack_store.mark_pending("abc123")
        tracker.observe("termiris_ctx) .file /data/data/com.termux/files/home/.termiris/runtime/cache/state/snapshot.ctx")
        assert tracker.state == AckTracker.PENDING
        assert tracker.pending_hash == "abc123"

    def test_pending_to_processing_on_generating(self, tracker, ack_store):
        """Generating → PROCESSING"""
        ack_store.mark_pending("abc123")
        tracker.observe(".file /path/to/snapshot.ctx")
        tracker.observe("⠋ Generating   ")
        assert tracker.state == AckTracker.PROCESSING

    def test_processing_to_ack_on_prompt_without_error(self, tracker, ack_store):
        """prompt sem Error → ACK"""
        ack_store.mark_pending("abc123")
        tracker.observe(".file /path/to/snapshot.ctx")
        tracker.observe("⠋ Generating   ")
        tracker.observe("resposta qualquer do modelo...")
        tracker.observe("termiris_ctx) ")
        assert tracker.state == AckTracker.IDLE
        assert ack_store.get_ack_hash() == "abc123"
        assert ack_store.get_pending_hash() is None

    def test_processing_to_fail_on_error(self, tracker, ack_store):
        """Error: → FAIL"""
        ack_store.mark_pending("abc123")
        tracker.observe(".file /path/to/snapshot.ctx")
        tracker.observe("⠋ Generating   ")
        tracker.observe("Error: Failed to call chat-completions api")
        assert tracker.state == AckTracker.IDLE
        assert ack_store.get_failure_hash() == "abc123"
        assert ack_store.get_pending_hash() is None


class TestFailureCases:
    """Cenários de falha com erros reais do backend."""

    def test_quota_exceeded_error(self, tracker, ack_store):
        """Erro real de quota do Gemini → FAIL"""
        ack_store.mark_pending("e488bc3e5ee2db8d")
        tracker.observe("termiris_ctx) .file /data/data/com.termux/files/home/.termiris/runtime/cache/state/snapshot.ctx")
        tracker.observe("⠴ Generating.  ")
        tracker.observe(
            "Error: Failed to call chat-completions api\r\n\r\n"
            "Caused by:\r\n"
            "    You exceeded your current quota\r\n"
            "    * Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, "
            "limit: 20, model: gemini-3-flash\r\n"
        )
        assert tracker.state == AckTracker.IDLE
        assert ack_store.get_failure_hash() == "e488bc3e5ee2db8d"
        assert ack_store.is_failed("e488bc3e5ee2db8d")

    def test_prompt_after_error_does_not_ack(self, tracker, ack_store):
        """prompt + Error → FAIL (não ACK)"""
        ack_store.mark_pending("abc123")
        tracker.observe(".file /path/to/snapshot.ctx")
        tracker.observe("⠋ Generating   ")
        tracker.observe("Error: Failed to call chat-completions api")
        tracker.observe("termiris_ctx) ")
        assert ack_store.get_failure_hash() == "abc123"
        assert ack_store.get_ack_hash() is None


class TestEdgeCases:
    """Casos-limite e robustez."""

    def test_file_without_pending_hash_ignored(self, tracker, ack_store):
        """.file sem hash pendente → ignorado"""
        tracker.observe(".file /path/to/snapshot.ctx")
        assert tracker.state == AckTracker.IDLE

    def test_prompt_without_prior_file_ignored(self, tracker, ack_store):
        """prompt sem .file anterior → ignorado"""
        tracker.observe("termiris_ctx) ")
        assert tracker.state == AckTracker.IDLE
        assert ack_store.get_ack_hash() is None

    def test_generating_without_file_ignored(self, tracker, ack_store):
        """Generating sem .file anterior → ignorado"""
        tracker.observe("⠋ Generating   ")
        assert tracker.state == AckTracker.IDLE

    def test_empty_text_ignored(self, tracker, ack_store):
        """Texto vazio → ignorado"""
        ack_store.mark_pending("abc123")
        tracker.observe(".file /path/to/snapshot.ctx")
        tracker.observe("")
        tracker.observe(None)
        assert tracker.state == AckTracker.PENDING

    def test_ansi_fragments_same_result(self, tracker, ack_store):
        """Fragmentos ANSI limpos produzem mesmo resultado"""
        ack_store.mark_pending("abc123")
        tracker.observe("termiris_ctx) .file /path/to/snapshot.ctx\x1b7\x1b8")
        tracker.observe("\r\n")
        tracker.observe("⠋ Generating   ")
        tracker.observe("\r\n\r\ntermiris_ctx) \x1b7181(0.02%)\x1b8\x1b7\x1b8")
        assert tracker.state == AckTracker.IDLE
        assert ack_store.get_ack_hash() == "abc123"


class TestTimeout:
    """Comportamento de timeout."""

    def test_timeout_does_not_generate_false_ack(self, tracker, ack_store):
        """Timeout → não gera ACK falso"""
        ack_store.mark_pending("abc123")
        tracker.observe(".file /path/to/snapshot.ctx")
        assert tracker.state == AckTracker.PENDING
        
        # Simula timeout
        tracker.state_since = time.time() - (AckTracker.TIMEOUT_SECONDS + 1)
        tracker.observe("qualquer texto")
        
        assert tracker.state == AckTracker.IDLE
        assert ack_store.get_ack_hash() is None


class TestRealTAPSequences:
    """Sequências reais extraídas do socket_tap.log."""

    def test_success_sequence_from_tap(self, tracker, ack_store):
        """Sequência real de sucesso"""
        ack_store.mark_pending("0a68869e49c9dd6f")
        tracker.observe("\r\n\r\ntermiris_ctx) .file /data/data/com.termux/files/home/.termiris/runtime/cache/state/snapshot.ctx\x1b7\x1b8")
        tracker.observe("\r\n")
        tracker.observe("⠋ Generating   ")
        tracker.observe("⠙ Generating   ")
        tracker.observe("resposta do modelo aqui")
        tracker.observe("termiris_ctx) \x1b7181(0.02%)\x1b8\x1b7\x1b8")
        assert tracker.state == AckTracker.IDLE
        assert ack_store.get_ack_hash() == "0a68869e49c9dd6f"

    def test_failure_sequence_from_tap(self, tracker, ack_store):
        """Sequência real de falha por quota"""
        ack_store.mark_pending("6513108f75b53ed7")
        tracker.observe("\r\n\r\ntermiris_ctx) .file /data/data/com.termux/files/home/.termiris/runtime/cache/state/snapshot.ctx\x1b7\x1b8")
        tracker.observe("\r\n")
        tracker.observe("⠴ Generating.  ")
        tracker.observe(
            "Error: Failed to call chat-completions api\r\n\r\n"
            "Caused by:\r\n"
            "    You exceeded your current quota\r\n"
        )
        tracker.observe("termiris_ctx) \x1b70\x1b8\x1b7\x1b8")
        assert tracker.state == AckTracker.IDLE
        assert ack_store.get_failure_hash() == "6513108f75b53ed7"
        assert ack_store.get_ack_hash() is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
