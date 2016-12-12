from traits.api import HasTraits, Str, List, This, \
    Either, Instance, Int, Enum, Any
from traits.api import Property as TraitsProperty


# Raw nodes as extracted from the file, pretty much verbatim
from traits.has_traits import cached_property


class RawCubaType(HasTraits):
    name = Str()
    definition = Str()
    shape = List(Int)
    type = Enum('string', 'double', 'integer', 'boolean')


class RawProperty(HasTraits):
    name = Str()
    default = Any()
    shape = Any()


class RawConcept(HasTraits):
    name = Str()
    parent = Str()
    definition = Str()
    models = List(Str)
    variables = List(Str)
    properties = List(RawProperty)


# Nodes that we use to represent the actual logical tree
class CubaType(RawCubaType):
    name = Str(regex="^CUBA\.[A-Z_]*")


class CubaTypes(HasTraits):
    children = List(CubaType)


class Property(HasTraits):
    name = Str(regex="^CUBA\.[A-Z_]*")
    type = Instance(CubaType)
    default = Str()
    shape = Either(Str(), None)


class Model(HasTraits):
    ref = Str(regex="^CUBA\.[A-Z_]*")


class Variable(HasTraits):
    ref = Str(regex="^CUBA\.[A-Z_]*")


class Concept(HasTraits):
    name = Str(regex="^CUBA\.[A-Z_]*")
    definition = Str()
    models = List(Model)
    variables = List(Variable)
    properties = List(Property)
    derived = List(This)
    children = TraitsProperty(depends_on="models,variables,properties,derived")

    @cached_property
    def _get_children(self):
        return self.models + self.variables + self.properties + self.derived


class Concepts(HasTraits):
    children = List(Concept)


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
