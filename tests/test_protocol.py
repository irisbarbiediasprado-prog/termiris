from protocol.kernel import CommandRouter, ProtocolKernel
from protocol.isa import Operation, PrimitiveISA

# Inicializa o CommandRouter e o Kernel corretamente
router = CommandRouter()
router.auto_discover()
kernel = ProtocolKernel(router=router)

def test_compile_retrieve_file():
    ops = kernel.compile("<<RETRIEVE FILE main.py>>")

    assert len(ops) == 1

    op = ops[0]
    assert isinstance(op, Operation)
    assert op.instruction == PrimitiveISA.SNAPSHOT
    assert op.payload["action"] == "INJECT_RESOURCE"
    assert op.payload["resource_type"] == "FILE"
    assert "main.py" in str(op.payload["targets"])

def test_compile_retrieve_tree():
    ops = kernel.compile("<<RETRIEVE TREE lib>>")
    assert len(ops) == 1

