from protocol.kernel import CommandRouter, ProtocolKernel
from protocol.isa import PrimitiveISA


def test_retrieve_status_pipeline():
    router = CommandRouter()
    router.auto_discover()
    kernel = ProtocolKernel(router=router)

    operations = kernel.compile("<<RETRIEVE STATUS>>")

    assert len(operations) == 1

    op = operations[0]

    assert op.instruction == PrimitiveISA.RETRIEVE
    assert op.payload["provider"] == "STATUS"
    assert op.payload["target"] == "status://current"
