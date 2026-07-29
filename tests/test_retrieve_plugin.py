from protocol.plugins.retrieve import RetrievePlugin, ResourceType

plugin = RetrievePlugin()

def test_parse_ast():
    ast = plugin.parse_ast(["FILE", "main.py"])
    assert ast.resource_type == ResourceType.FILE
    assert ast.targets == ["main.py"]

def test_lower_to_intent():
    ast = plugin.parse_ast(["FILE", "main.py"])
    intent = plugin.lower_to_intent(ast)
    assert intent.metadata.get("sub_type") == "FILE"
