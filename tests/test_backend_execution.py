from protocol.plan import MigrationPlan, MigrationStep
from protocol.isa_backend import ISABackend
from protocol.filesystem_backend import FilesystemBackend


def test_same_plan_compiles_in_multiple_backends(tmp_path):
    plan = MigrationPlan(
        steps=[
            MigrationStep(
                action="LIST_DIRECTORY",
                target=str(tmp_path),
                parameters={"path": str(tmp_path)},
            )
        ]
    )

    isa_result = ISABackend().compile(plan)
    fs_result = FilesystemBackend().compile(plan)

    assert len(isa_result) == 1
    assert len(fs_result) == 1

    assert isa_result[0].payload["path"] == str(tmp_path)

    assert fs_result[0]["backend"] == "filesystem"
    assert fs_result[0]["operation"] == "list_directory"
