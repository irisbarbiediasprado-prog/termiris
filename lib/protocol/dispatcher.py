import sys
from pathlib import Path
from typing import List

LIB_DIR = Path.home() / ".termiris" / "lib"
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))

from protocol.isa import Operation
from models import RuntimeResult
from protocol.kernel import CommandRouter, ProtocolKernel
from runtime.engine import RuntimeEngine

class ProtocolDispatcher:
    def __init__(self, kernel=None, engine=None):
        if kernel is None:
            router = CommandRouter()
            router.auto_discover()
            self.kernel = ProtocolKernel(router)
        else:
            self.kernel = kernel
            
        self.engine = engine or RuntimeEngine()

    def dispatch(self, raw_input: str) -> List[RuntimeResult]:
        operations: List[Operation] = self.kernel.compile(raw_input)
        results = []
        for op in operations:
            res = self.engine.apply(op)
            results.append(res)
        return results

class ProtocolRuntime:
    def __init__(self, dispatcher=None):
        self.dispatcher = dispatcher or ProtocolDispatcher()

    def handle(self, raw_text: str) -> List[RuntimeResult]:
        return self.dispatcher.dispatch(raw_text)
