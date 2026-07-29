import sys
import unittest
from pathlib import Path

LIB_DIR = Path.home() / ".termiris" / "lib"
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))

from protocol.isa import Operation, PrimitiveISA
from runtime.engine import RuntimeEngine

class TestRuntimeEngine(unittest.TestCase):
    def test_apply_operation_generates_snapshot(self):
        engine = RuntimeEngine()
        bootstrap_card = Path.home() / ".termiris" / "tp" / "bootstrap" / "000-bootstrap.card"
        
        op = Operation(
            instruction=PrimitiveISA.SNAPSHOT,
            payload={"file_path": str(bootstrap_card)}
        )
        
        result = engine.apply(op)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.snapshot)
        self.assertEqual(result.snapshot.generation, 1)

if __name__ == "__main__":
    unittest.main()
