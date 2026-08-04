from typing import List
from protocol.isa import Operation
from protocol.kernel import CommandRouter, ProtocolKernel

class ProtocolDispatcher:
    def __init__(self, kernel=None, engine=None, router=None):
        if kernel is None:
            router = router or CommandRouter()
            if not router._routes:
                router.auto_discover()
            kernel = ProtocolKernel(router)
        self.kernel = kernel

        if engine is None:
            try:
                from runtime.engine import RuntimeEngine
                self.engine = RuntimeEngine()
            except Exception:
                self.engine = None
        else:
            self.engine = engine

    def dispatch(self, raw_input: str):
        operations: List[Operation] = self.kernel.compile(raw_input)
        if self.engine is None:
            # fallback puro, sem efeito colateral
            return operations
        return [self.engine.apply(op) for op in operations]

class ProtocolRuntime:
    def __init__(self, dispatcher=None):
        self.dispatcher = dispatcher or ProtocolDispatcher()

    def handle(self, raw_text: str):
        return self.dispatcher.dispatch(raw_text)
