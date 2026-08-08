from protocol.kernel import CommandRouter, ProtocolKernel
from protocol.isa import Operation, PrimitiveISA

router = CommandRouter()
router.auto_discover()
kernel = ProtocolKernel(router=router)

def test_compile_retrieve_file():
    ops = kernel.compile("<<RETRIEVE FILE main.py>>")

    assert len(ops) == 1

    op = ops[0]
    assert isinstance(op, Operation)
    assert op.instruction == PrimitiveISA.RETRIEVE
    assert op.payload["resource_type"] == "FILE"
    assert op.payload["target"] == "main.py"

def test_compile_retrieve_tree():
    ops = kernel.compile("<<RETRIEVE TREE lib>>")
    assert len(ops) == 1
