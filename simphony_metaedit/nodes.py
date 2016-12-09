from traits.api import HasTraits, Str, List, This


class EntryNode(HasTraits):
    """Represents an entry in the tree"""
    name = Str('<unknown>')
    children = List(This)


class RootNode(HasTraits):
    """Represents the root node"""
    name = Str("/")
    path = Str('/')
    children = List(EntryNode)


def traverse(node):
    """Traverses the tree depth first."""
    yield node
    for c in node.children:
        for sub in traverse(c):
            yield sub
