import pytest
import sys
from pathlib import Path

# Adiciona o diretório bin ao path para importar a função
bin_dir = Path.home() / ".termiris/bin"
sys.path.insert(0, str(bin_dir))

# Importa a função do módulo (que tem hífen, então usamos importlib)
import importlib.util
spec = importlib.util.spec_from_file_location("context_delivery", bin_dir / "context-delivery.py")
context_delivery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(context_delivery)

should_deliver = context_delivery.should_deliver

class TestShouldDeliver:
    def test_same_hash_not_delivered(self):
        assert should_deliver("abc123", "abc123") is False

    def test_new_hash_delivered(self):
        assert should_deliver("def456", "abc123") is True

    def test_empty_new_hash_not_delivered(self):
        assert should_deliver(None, "abc123") is False

    def test_new_hash_with_no_last_success(self):
        assert should_deliver("def456", None) is True
