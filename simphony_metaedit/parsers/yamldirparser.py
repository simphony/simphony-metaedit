import os
from .exceptions import ParsingError
from .. import nodes
from .cuba_file_parser import CUBAFileParser
from .metadata_file_parser import MetadataFileParser


class YamlDirParser:
    """Parser for the current format of metadata as two files in a directory"""

    def parse(self, directory):
        """Parses a directory containing file and extracts the tree.

        Parameters
        ----------
        directory: str
            the directory containing the cuba.yml and simphony_metadata.yml.

        Returns
        -------
        The object tree.
        """
        cuba_file_path = os.path.join(directory, "cuba.yml")
        with open(cuba_file_path) as f:
            root_cuba = CUBAFileParser().parse(f)

        metadata_file_path = os.path.join(directory, "simphony_metadata.yml")
        with open(metadata_file_path) as f:
            raw_metadata_nodes = MetadataFileParser().parse(f)

        root_node = _do_linkage(root_cuba, raw_metadata_nodes)

        return root_node


def _do_linkage(raw_cuba_nodes, raw_metadata_nodes):
    """Performs the final linkage between the raw nodes,
    and returns the final parse tree.

    Parameters
    ----------

    raw_cuba_nodes: list
        a list of the raw nodes obtained by parsing the cuba.yml file

    raw_metadata_nodes: list
        a list of the raw nodes obtained by parsing the simphony_metadata.yml

    Returns
    -------
    a Root node, properly filled in.

    """

    raw_cuba_nodemap = {with_cuba_prefix(node.name): node
                        for node in raw_cuba_nodes.entries.values()}
    raw_metadata_nodemap = {with_cuba_prefix(node.name): node
                            for node in raw_metadata_nodes}

    common_keys = set(raw_cuba_nodemap.keys()).intersection(
        set(raw_metadata_nodemap.keys())
        )

    if len(common_keys):
        raise ParsingError("Duplicate keys between files: {}".format(
            common_keys))

    root = nodes.Root()
    cuba_types = nodes.CUBATypes()
    root.children.append(cuba_types)
    for raw_cuba_type in raw_cuba_nodemap.values():
        cuba_type = nodes.CUBAType(
            name=with_cuba_prefix(raw_cuba_type.name),
            definition=raw_cuba_type.definition,
            shape=raw_cuba_type.shape,
            type=raw_cuba_type.type,
            )
        cuba_types.children.append(cuba_type)

    concepts_root = nodes.Concepts()
    concept_nodemap = {}

    for concept_name in raw_metadata_nodemap.keys():
        _add_to_concepts_tree(
            concepts_root,
            concept_nodemap,
            raw_metadata_nodemap,
            concept_name)

    root.children.append(concepts_root)
    return root


def _add_to_concepts_tree(concepts_root, concept_nodemap, raw_concept_nodemap,
                          concept_name):
    """
    Recursive function that instantiates the Concept nodes and populates
    the parse tree according to the "parent" hierarchy.

    As we don't know the order of the incoming nodes (because the file
    uses a yaml dictionary and the order is arbitrary no matter what the
    order in the file is, we need to do the binding of the tree with a
    lenient strategy that accommodates for non yet declared nodes.

    Parameters
    ----------
    concepts_root: node.Concepts
        the Concepts node that will hold the tree.
    concept_nodemap: dict
        a name: Concept mapping for easy lookup.
    raw_concept_nodemap:
        a name: RawConcept mapping for easy lookup. Note that the name can
        be different from the nodemap above.
    concept_name:
        The name of the concept node to add to the tree.
    """

    # If the node is already in the tree, it's also already in the
    # nodemap (which is populated in parallel). So we don't do anything.
    concept = concept_nodemap.get(with_cuba_prefix(concept_name))
    if concept is not None:
        return

    # The node is not there, create it from the raw concept node.
    raw_concept = raw_concept_nodemap[concept_name]
    concept = nodes.Concept(
        name=with_cuba_prefix(raw_concept.name),
        definition=raw_concept.definition,
    )

    # Add the ancillary data.
    for raw_property in raw_concept.properties:
        property = nodes.Property(
            ref=with_cuba_prefix(raw_property.ref),
        )
        concept.properties.append(property)

    for model_name in raw_concept.models:
        model = nodes.Model(
            ref=with_cuba_prefix(model_name),
        )
        concept.models.append(model)

    for variable_name in raw_concept.variables:
        variable = nodes.Variable(
            ref=with_cuba_prefix(variable_name),
        )
        concept.variables.append(variable)

    parent_name = raw_concept.parent.strip()
    if len(parent_name) == 0:
        parent = None
    else:
        # If it has a parent specified in the raw concept node, then we have
        # to first check if that node exists, recursively adding it if needed,
        # until we either traverse up to the root of the parent hierarchy
        # (creating each node along the way), or we find a node that is already
        # present.
        _add_to_concepts_tree(
            concepts_root,
            concept_nodemap,
            raw_concept_nodemap,
            parent_name)
        parent = concept_nodemap[parent_name]

    if parent is None:
        concepts_root.children.append(concept)
    else:
        parent.derived.append(concept)

    concept_nodemap[concept_name] = concept


def with_cuba_prefix(string):
    """Adds the CUBA. prefix to the string if not there."""
    if string.startswith("CUBA."):
        return string

    return "CUBA."+string


def without_cuba_prefix(string):
    """Removes the CUBA. prefix to the string if there."""
    if string.startswith("CUBA."):
        return string[5:]

    return string
