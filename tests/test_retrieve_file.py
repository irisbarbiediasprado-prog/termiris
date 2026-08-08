from protocol.kernel import CommandRouter, ProtocolKernel
from protocol.isa import PrimitiveISA

def test_retrieve_file_pipeline():
    router = CommandRouter()
    router.auto_discover()

    kernel = ProtocolKernel(router=router)

    operations = kernel.compile("<<RETRIEVE FILE README.md>>")

    assert len(operations) == 1

    op = operations[0]

    assert op.instruction == PrimitiveISA.RETRIEVE
    assert op.payload["resource_type"] == "FILE"
    assert op.payload["target"] == "README.md"
