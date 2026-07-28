import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path.home() / ".termiris" / "lib"))
from runtime.repository import FilesystemBootstrapRepository

class TestRepository(unittest.TestCase):
    def test_list_artifacts_finds_md_files(self):
        repo = FilesystemBootstrapRepository(bootstrap_dir=Path.home() / ".termiris" / "tp")
        artifacts = repo.list_artifacts()
        print(f"\n[DEBUG REPO] Encontrados {len(artifacts)} artefatos em ~/.termiris/tp")
        for art in artifacts:
            print(f"  - ID: {art.metadata.id} | URI: {art.resource.uri}")
        self.assertGreater(len(artifacts), 0, "Nenhum arquivo .md foi encontrado em ~/.termiris/tp")

if __name__ == "__main__":
    unittest.main()
