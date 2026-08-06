import pytest
from unittest.mock import MagicMock
from protocol.dispatcher import ProtocolDispatcher, _ENGINE_DEFAULT

class TestDispatcherSentinel:
    def test_dispatcher_default_engine(self):
        """ProtocolDispatcher() deve criar engine (comportamento padrão)."""
        mock_kernel = MagicMock()
        dispatcher = ProtocolDispatcher(kernel=mock_kernel)
        # O engine pode ser None se a importação falhar,
        # mas nunca deve ser o sentinel
        assert dispatcher.engine is not _ENGINE_DEFAULT

    def test_dispatcher_explicit_none(self):
        """ProtocolDispatcher(engine=None) deve desabilitar engine."""
        mock_kernel = MagicMock()
        dispatcher = ProtocolDispatcher(kernel=mock_kernel, engine=None)
        assert dispatcher.engine is None

    def test_dispatcher_sentinel_preserved(self):
        """Verifica que o sentinel não vazou para a instância."""
        mock_kernel = MagicMock()
        dispatcher = ProtocolDispatcher(kernel=mock_kernel)
        assert dispatcher.engine is not _ENGINE_DEFAULT
