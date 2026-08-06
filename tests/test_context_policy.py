import json
import time
import pytest
from pathlib import Path
from termiris.context_policy import ContextPolicy

class TestContextPolicy:
    def test_check_new_hash(self, tmp_path):
        """Primeiro hash: deve ser HASH_NEW, hits=0, mode=PA, delay=0."""
        state_dir = tmp_path / "state"
        policy = ContextPolicy(state_dir=state_dir)

        result = policy.check("abc123")
        assert result["hash"] == "abc123"
        assert result["event"] == "HASH_NEW"
        assert result["hash_hits"] == 0
        assert result["mode"] == "PA"
        assert result["delay"] == 0

    def test_check_repeated_hash_hits(self, tmp_path):
        """Hash repetido deve incrementar hits e delay."""
        state_dir = tmp_path / "state"
        policy = ContextPolicy(state_dir=state_dir)

        # Primeira vez
        policy.check("abc123")
        # Segunda vez (mesmo hash)
        result = policy.check("abc123")
        assert result["hash_hits"] == 1
        assert result["event"] == "HASH_HIT"
        assert result["mode"] == "PA"
        assert result["delay"] == 30  # hits * 30 = 30

        # Terceira vez
        result = policy.check("abc123")
        assert result["hash_hits"] == 2
        assert result["delay"] == 60

        # Quarta vez (hits=3, ainda PA)
        result = policy.check("abc123")
        assert result["hash_hits"] == 3
        assert result["delay"] == 90
        assert result["mode"] == "PA"

        # Quinta vez (hits=4, entra em PG)
        result = policy.check("abc123")
        assert result["hash_hits"] == 4
        assert result["mode"] == "PG"
        assert result["delay"] == 90 * (2 ** (4 - 3))  # 90 * 2 = 180

    def test_check_new_hash_resets_hits(self, tmp_path):
        """Novo hash deve resetar hits para 0."""
        state_dir = tmp_path / "state"
        policy = ContextPolicy(state_dir=state_dir)

        policy.check("abc123")  # hits 0
        policy.check("abc123")  # hits 1
        policy.check("abc123")  # hits 2

        # Novo hash
        result = policy.check("def456")
        assert result["hash_hits"] == 0
        assert result["event"] == "HASH_NEW"

    def test_persist_state(self, tmp_path):
        """Verifica se o estado é persistido em arquivo."""
        state_dir = tmp_path / "state"
        policy = ContextPolicy(state_dir=state_dir)

        policy.check("abc123")
        policy.check("abc123")  # hits 1

        # Recria a policy (simula reinicialização)
        policy2 = ContextPolicy(state_dir=state_dir)
        result = policy2.check("abc123")
        assert result["hash_hits"] == 2  # deve continuar contando
        assert result["event"] == "HASH_HIT"

    def test_history_file(self, tmp_path):
        """Verifica se o histórico é escrito."""
        state_dir = tmp_path / "state"
        policy = ContextPolicy(state_dir=state_dir)

        policy.check("abc123")
        policy.check("def456")

        history_file = state_dir / "context.history.jsonl"
        assert history_file.exists()
        lines = history_file.read_text().strip().split("\n")
        assert len(lines) == 2
        for line in lines:
            data = json.loads(line)
            assert "hash" in data
            assert "timestamp" in data
