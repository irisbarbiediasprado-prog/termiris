from typing import List, Dict, Any, Optional
from dataclasses import replace
from protocol.isa import Operation
from protocol.kernel import CommandRouter, ProtocolKernel
from cli.metadata import extract_metadata

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
        clean_input, metadata = extract_metadata(raw_input)
        operations: List[Operation] = self.kernel.compile(clean_input)
        if metadata:
            operations = [replace(op, metadata=metadata) for op in operations]
        return operations

class ProtocolRuntime:
    def __init__(self, dispatcher=None):
        self.dispatcher = dispatcher or ProtocolDispatcher()

    def handle(self, raw_text: str):
        operations = self.dispatcher.dispatch(raw_text)
        if self.dispatcher.engine is None:
            return operations
        return [self.dispatcher.engine.apply(op) for op in operations]
