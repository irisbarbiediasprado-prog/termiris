from libcst.metadata import MetadataWrapper, PositionProvider


def wrap(tree):
    return MetadataWrapper(tree)


def get_positions(wrapper):
    return wrapper.resolve(PositionProvider)
