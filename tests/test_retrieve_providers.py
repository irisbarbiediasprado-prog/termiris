from protocol.default_executors import create_executor_registry
from protocol.isa import Operation, PrimitiveISA


def execute(provider, target):
    registry = create_executor_registry(repository=None)
    executor = registry.resolve(PrimitiveISA.RETRIEVE)

    op = Operation(
        instruction=PrimitiveISA.RETRIEVE,
        payload={
            "resource_type": provider,
            "target": target,
        },
    )

    return executor.execute(op)


def test_retrieve_status_provider():
    result = execute("STATUS", "status://current")

    assert result.success is True


def test_retrieve_analysis_provider():
    result = execute("ANALYSIS", "analysis://architecture")

    assert result.success is True


def test_retrieve_handover_provider():
    result = execute("HANDOVER", "handover://current")

    assert result.success is True
