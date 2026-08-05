from protocol.default_executors import create_executor_registry
from protocol.isa import Operation, PrimitiveISA


def test_retrieve_status_runtime():
    registry = create_executor_registry(repository=None)

    executor = registry.resolve(PrimitiveISA.RETRIEVE)

    op = Operation(
        instruction=PrimitiveISA.RETRIEVE,
        payload={
            "provider": "STATUS",
            "target": "status://current",
        },
    )

    result = executor.execute(op)

    assert result.success is True
