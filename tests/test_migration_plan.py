import pytest
from refactor.plan import MigrationPlan


def test_migration_plan_contract():
    plan = MigrationPlan(
        operations=("operation",),
        metadata={"rule": "optparse"},
    )

    assert plan.operations == ("operation",)
    assert plan.metadata["rule"] == "optparse"

    with pytest.raises(AttributeError):
        plan.operations = ()  # type: ignore
