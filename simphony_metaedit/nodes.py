from traits.api import (
    HasStrictTraits, Str, String, List, This, Either, Int, Enum, Any,
    Instance, cached_property, Dict
)
from traits.api import Property as TraitsProperty


# Support traits
CUBAName = String(regex="^[A-Z_][A-Z0-9_]*$")
Version = String(regex="^\d+\.\d+$")


# First pass parsing raw nodes as extracted from the file, almost verbatim
# to the yaml representation, but uses traits to validate the content
# according to the type.

# Nodes for CUBA parser
class RawCUBAEntry(HasStrictTraits):
    """Represents the raw data of a CUBA type before the linkage step"""
    name = CUBAName
    definition = Str()
    shape = List(Int)
    length = Either(Int, None)
    type = Enum('string', 'double', 'integer', 'boolean')


class RawRootNode(HasStrictTraits):
    version = Version()
    purpose = Str()
    type = Enum("CUBA", "CUDS")
    entries = Dict(CUBAName(), RawCUBAEntry)


#######


class RawProperty(HasStrictTraits):
    """Represents the raw data of a property before the linkage step"""
    ref = Str()
    default = Any()
    shape = Any()


class RawConcept(HasStrictTraits):
    """Represents the raw data of a concept before the linkage step"""
    name = Str()
    parent = Str()
    definition = Str()
    models = List(Str)
    variables = List(Str)
    properties = List(RawProperty)


# Nodes that we use to represent the final parse tree
class CUBAType(RawCUBAEntry):
    """Represents a CUBA type"""
    name = Str(regex="^CUBA\.[A-Z_]*")


class CubaTypes(HasStrictTraits):
    """Holds the list of the CUBA types"""
    children = List(Instance(CUBAType))


class Property(HasStrictTraits):
    """A property as specified in the Concept"""
    ref = Str(regex="^CUBA\.[A-Z_]*")
    default = Str()
    shape = Either(Str(), None)


class Model(HasStrictTraits):
    """A model as specified in the Concept"""
    ref = Str(regex="^CUBA\.[A-Z_]*")


class Variable(HasStrictTraits):
    """A variable as specified in the Concept"""
    ref = Str(regex="^CUBA\.[A-Z_]*")


class Concept(HasStrictTraits):
    """Contains a concept, that is, an entity we describe """
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


class Concepts(HasStrictTraits):
    """Container for concepts"""
    name = Str("Concepts")
    children = List(Concept)


class Root(HasStrictTraits):
    """Represents the root node"""
    name = Str("/")
    path = Str('/')
    children = List(Either(Concepts, CubaTypes))


def traverse(node, level=0):
    """Traverses the tree depth first.
    yields the node and the level at which the node is found.
    """
    yield node, level
    if hasattr(node, "children"):
        for c in node.children:
            for sub, sublevel in traverse(c, level+1):
                yield sub, sublevel
