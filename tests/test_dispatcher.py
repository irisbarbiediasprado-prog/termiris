import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path.home() / ".termiris" / "lib"))
from runtime.engine import RuntimeEngine
from runtime.repository import FilesystemBootstrapRepository
from providers.filesystem import TemporaryArtifactProvider
from providers.query import SystemQueryProvider
from protocol.dispatcher import ProtocolDispatcher

class TestProtocolDispatcher(unittest.TestCase):
    def test_bootstrap_command(self):
        engine = RuntimeEngine()
        repo = FilesystemBootstrapRepository(bootstrap_dir=Path.home() / ".termiris" / "tp")
        temp_art = TemporaryArtifactProvider(Path.home() / ".termiris" / "runtime" / "cache" / "state")
        queries = SystemQueryProvider()
        dispatcher = ProtocolDispatcher(engine=engine, bootstrap_repo=repo, temp_artifacts=temp_art, queries=queries)
        result = dispatcher.dispatch("<< BOOTSTRAP >>")
        print(f"\n[DEBUG DISPATCHER] Sucesso: {result.success}")
        print(f"[DEBUG DISPATCHER] Avisos: {result.warnings}")
        if result.snapshot:
            print(f"[DEBUG DISPATCHER] Geração: {result.snapshot.generation}")
            print(f"[DEBUG DISPATCHER] Artefatos no Snapshot: {len(result.snapshot.artifacts)}")
        self.assertTrue(result.success)
        self.assertIsNotNone(result.snapshot)

if __name__ == "__main__":
    unittest.main()
