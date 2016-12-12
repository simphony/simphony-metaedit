from traits.api import HasTraits, Str, List, This, \
    Either, Instance, Int, Enum, Any


class CubaType(HasTraits):
    name = Str()
    definition = Str()
    shape = List(Int)
    type = Enum('string', 'double', 'integer', 'boolean')


class CubaTypes(HasTraits):
    children = List(CubaType)


class Property(HasTraits):
    type = Instance(CubaType)
    default = Str()
    shape = Either(Str(), None)


class RawProperty(HasTraits):
    name = Str()
    default = Any()
    shape = Any()


class Concept(HasTraits):
    name = Str()
    definition = Str()
    models = List(This)
    variables = List(This)
    properties = List(Property)
    children = List(This)


class RawConcept(HasTraits):
    name = Str()
    parent = Str()
    definition = Str()
    models = List(Str)
    variables = List(Str)
    properties = List(RawProperty)


class Concepts(HasTraits):
    children = List(Concept)


class Reference(HasTraits):
    ref = Either(Str, Instance(Concept), Instance(CubaType))


class Root(HasTraits):
    """Represents the root node"""
    name = Str("/")
    path = Str('/')
    children = List(Either(Concepts, CubaTypes))


def traverse(node, level=0):
    """Traverses the tree depth first."""
    yield node, level
    if hasattr(node, "children"):
        for c in node.children:
            for sub, sublevel in traverse(c, level+1):
                yield sub, sublevel
