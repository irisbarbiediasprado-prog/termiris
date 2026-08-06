from typing import List, Dict, Any, Optional
from protocol.isa import Operation
from protocol.kernel import CommandRouter, ProtocolKernel
from cli.metadata import extract_metadata

class DispatchContext:
    def __init__(self, operations: List[Operation], metadata: Dict[str, str]):
        self.operations = operations
        self.metadata = metadata

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

    def dispatch(self, raw_input: str) -> DispatchContext:
        clean_input, metadata = extract_metadata(raw_input)
        operations: List[Operation] = self.kernel.compile(clean_input)
        return DispatchContext(operations, metadata)

class ProtocolRuntime:
    def __init__(self, dispatcher=None):
        self.dispatcher = dispatcher or ProtocolDispatcher()

    def handle(self, raw_text: str) -> List[Operation]:
        """
        Ponto de entrada público.
        Retorna uma lista de operações (API estável).
        """
        context = self.dispatcher.dispatch(raw_text)
        if self.dispatcher.engine is None:
            return context.operations
        return [self.dispatcher.engine.apply(op) for op in context.operations]
