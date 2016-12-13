import os
import yaml
from .. import nodes


class ParsingError(Exception):
    pass


class YamlDirParser:
    """Parser for the current format of metadata as two files in a directory"""

    def parse(self, directory):
        """Parses a directory containing file and extracts the tree."""
        raw_cuba_nodes = _parse_cuba_file(
            os.path.join(directory, "cuba.yml"))
        raw_metadata_nodes = _parse_metadata_file(
            os.path.join(directory, "simphony_metadata.yml"))
        root_node = _do_linkage(raw_cuba_nodes, raw_metadata_nodes)
        return root_node


def _do_linkage(raw_cuba_nodes, raw_metadata_nodes):
    raw_cuba_nodemap = {with_cuba_prefix(node.name): node
                    for node in raw_cuba_nodes}
    raw_metadata_nodemap = {with_cuba_prefix(node.name): node
                            for node in raw_metadata_nodes}

    common_keys = set(raw_cuba_nodemap.keys()).intersection(
        set(raw_metadata_nodemap.keys())
        )

    if len(common_keys):
        raise ParsingError("Duplicate keys between files: {}".format(
            common_keys))

    root = nodes.Root()
    cuba_types = nodes.CubaTypes()
    root.children.append(cuba_types)
    for raw_cuba_type in raw_cuba_nodemap.values():
        cuba_type = nodes.CubaType(
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


def _parse_raw_cuba_type_data(name, data):
    return nodes.RawCubaType(
        name=name,
        definition=data.get("definition", ""),
        type=data["type"],
        shape=data["shape"]
    )


def _parse_raw_concept(concept_name, raw_concept_data):
    raw_properties = []

    for prop_name, prop_data in [(name, data)
                                 for name, data in raw_concept_data.items()
                                 if name.startswith("CUBA.")]:
        if prop_data is None:
            raw_property = nodes.RawProperty(ref=prop_name)
        else:
            raw_property = nodes.RawProperty(
                ref=prop_name,
                default=prop_data.get("default"),
                shape=prop_data.get("shape")
            )
        raw_properties.append(raw_property)

    return nodes.RawConcept(
        name=concept_name,
        parent=raw_concept_data.get("parent") or "",
        definition=raw_concept_data.get("definition") or "",
        models=raw_concept_data.get("models") or [],
        variables=raw_concept_data.get("variables") or [],
        properties=raw_properties
    )


def _parse_cuba_file(cuba_file):
    with open(cuba_file) as f:
        cuba_data = yaml.safe_load(f)

    nodemap = {}

    for name, data in cuba_data.get("CUBA_KEYS", {}).items():
        if name in nodemap:
            raise ParsingError("Duplicate entry {} in "
                               "{}".format(name, cuba_file))

        try:
            raw_cuba_type = _parse_raw_cuba_type_data(name, data)
        except Exception as e:
            raise ParsingError("Unable to parse entry {} "
                               "in {}: {}".format(name,
                                                  cuba_file,
                                                  str(e)))
        nodemap[raw_cuba_type.name] = raw_cuba_type

    return nodemap.values()


def _parse_metadata_file(metadata_file):
    with open(metadata_file) as f:
        cuds_data = yaml.safe_load(f)

    nodemap = {}
    # We need to collect all cuds entities first, because in the file
    # they are a dictionary, and they can be recovered in arbitrary order.
    for name, data in cuds_data.get("CUDS_KEYS", {}).items():
        if name in nodemap:
            raise ParsingError("Duplicate entry {} in "
                               "{}".format(name, metadata_file))
        try:
            raw_concept = _parse_raw_concept(name, data)
        except Exception as e:
            raise ParsingError("Unable to parse entry {} "
                               "in {}: {}".format(name,
                                                  metadata_file,
                                                  str(e)))

        nodemap[raw_concept.name] = raw_concept

    return nodemap.values()


def _add_to_concepts_tree(concepts_root, concept_nodemap, raw_concept_nodemap,
                          concept_name):

    concept = concept_nodemap.get(with_cuba_prefix(concept_name))
    if concept is not None:
        return

    raw_concept = raw_concept_nodemap[concept_name]
    concept = nodes.Concept(
        name=with_cuba_prefix(raw_concept.name),
        definition=raw_concept.definition,
        )

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
    if string.startswith("CUBA."):
        return string

    return "CUBA."+string


def without_cuba_prefix(string):
    if string.startswith("CUBA."):
        return string[5:]

    return string
