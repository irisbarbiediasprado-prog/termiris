import sys
import unittest
from pathlib import Path

LIB_DIR = Path.home() / ".termiris" / "lib"
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))

from models import ResourceReference
from runtime.repository import ArtifactRepository

class TestRepository(unittest.TestCase):
    def test_fetch_filesystem_artifact(self):
        repo = ArtifactRepository()
        bootstrap_card = Path.home() / ".termiris" / "tp" / "bootstrap" / "000-bootstrap.card"
        
        if bootstrap_card.exists():
            ref = ResourceReference(uri=f"filesystem://{bootstrap_card}")
            artifact = repo.fetch(ref)
            self.assertEqual(artifact.uri, ref.uri)
            self.assertGreater(len(artifact.content), 0)

if __name__ == "__main__":
    unittest.main()
