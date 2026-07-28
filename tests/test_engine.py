import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path.home() / ".termiris" / "lib"))
from models import DomainOperation, OperationType, Artifact, ArtifactMetadata, ResourceReference
from runtime.engine import RuntimeEngine

class TestRuntimeEngine(unittest.TestCase):
    def test_apply_operation_generates_snapshot(self):
        engine = RuntimeEngine()
        artifact = Artifact(metadata=ArtifactMetadata(id="tp_test", artifact_type="protocol", priority=100), resource=ResourceReference(uri="filesystem:///tmp/test.md"))
        result = engine.apply(DomainOperation(type=OperationType.INGEST_ARTIFACT, artifact=artifact))
        self.assertTrue(result.success)
        self.assertIsNotNone(result.snapshot)
        self.assertEqual(result.snapshot.generation, 1)
        self.assertEqual(len(result.snapshot.artifacts), 1)

if __name__ == "__main__":
    unittest.main()
