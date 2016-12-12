import os
import yaml
from .. import nodes


class ParsingError(Exception):
    pass


class YamlDirParser:
    """Parser for the current format of metadata as two files in a directory"""

    def parse(self, directory):
        """Parses a directory containing file and extracts the tree."""
        cuba_nodemap = self._parse_cuba_file(
            os.path.join(directory, "cuba.yml"))
        metadata_nodemap = self._parse_metadata_no_linkage(
            os.path.join(directory, "simphony_metadata.yml"))
        root_node = self._do_linkage(cuba_nodemap, metadata_nodemap)
        return root_node

    def _parse_cuba_file(self, cuba_file):
        with open(cuba_file) as f:
            cuba_data = yaml.safe_load(f)

        nodemap = {}

        for name, data in cuba_data.get("CUBA_KEYS", {}).items():
            if with_cuba_prefix(name) in nodemap:
                raise ParsingError("Duplicate entry {} in "
                                   "{}".format(name, cuba_file))

            try:
                cuba_type = parse_cuba_type_data(name, data)
            except Exception as e:
                raise ParsingError("Unable to parse entry {} "
                                   "in {}: {}".format(name,
                                                      cuba_file,
                                                      str(e)))
            nodemap[cuba_type.name] = cuba_type

        return nodemap

    def _parse_metadata_no_linkage(self, metadata_file):
        with open(metadata_file) as f:
            cuds_data = yaml.safe_load(f)

        nodemap = {}
        # We need to collect all cuds entities first, because in the file
        # they are a dictionary, and they can be recovered in arbitrary order.
        for name, data in cuds_data.get("CUDS_KEYS", {}).items():
            name = with_cuba_prefix(name)
            if name in nodemap:
                raise ParsingError("Duplicate entry {} in "
                                   "{}".format(name, metadata_file))
            try:
                raw_concept = parse_raw_concept(name, data)
            except Exception as e:
                raise ParsingError("Unable to parse entry {} "
                                   "in {}: {}".format(name,
                                                      metadata_file,
                                                      str(e)))

            nodemap[name] = raw_concept

        return nodemap

    def _do_linkage(self, cuba_nodemap, metadata_nodemap):
        common_keys = set(cuba_nodemap.keys()).intersection(
            set(metadata_nodemap.keys())
            )

        if len(common_keys):
            raise ParsingError("Duplicate keys between files: {}".format(
                common_keys))

        root = nodes.Root()
        cuba_types = nodes.CubaTypes()
        root.children.append(cuba_types)
        cuba_types.children = list(cuba_nodemap.values())

        concepts_root = nodes.Concepts()
        concept_nodemap = {}

        for concept_name in metadata_nodemap.keys():
            add_to_concepts_tree(
                concepts_root,
                concept_nodemap,
                metadata_nodemap,
                concept_name)

        root.children.append(concepts_root)
        return root


def parse_cuba_type_data(name, data):
    return nodes.CubaType(
        name=with_cuba_prefix(name),
        definition=data.get("definition", ""),
        type=data["type"],
        shape=data["shape"]
    )


def parse_raw_concept(name, raw_concept_data):
    raw_properties = []

    for prop_name, prop_data in [(name[5:], data)
                                 for name, data in raw_concept_data.items()
                                 if name.startswith("CUBA.")]:
        if prop_data is None:
            raw_property = nodes.RawProperty(name=name)
        else:
            raw_property = nodes.RawProperty(
                name=name,
                default=prop_data.get("default"),
                shape=prop_data.get("shape")
            )
        raw_properties.append(raw_property)

    return nodes.RawConcept(
        name=name,
        parent=raw_concept_data.get("parent") or "",
        definition=raw_concept_data.get("definition") or "",
        models=raw_concept_data.get("models") or [],
        variables=raw_concept_data.get("variables") or [],
        properties=raw_properties
    )


def add_to_concepts_tree(concepts_root, concept_nodemap, raw_concept_nodemap,
                         concept_name):

    concept = concept_nodemap.get(with_cuba_prefix(concept_name))
    if concept is not None:
        return

    raw_concept = raw_concept_nodemap[concept_name]
    concept = nodes.Concept(
        name=raw_concept.name,
        definition=raw_concept.definition,
        )

    parent_name = raw_concept.parent.strip()
    if len(parent_name) == 0:
        parent = None
    else:
        add_to_concepts_tree(concepts_root,
            concept_nodemap, raw_concept_nodemap, parent_name)
        parent = concept_nodemap[parent_name]

    if parent is None:
        concepts_root.children.append(concept)
    else:
        parent.children.append(concept)

    concept_nodemap[concept_name] = concept

def with_cuba_prefix(string):
    if string.startswith("CUBA."):
        return string

    return "CUBA."+string

def without_cuba_prefix(string):
    if string.startswith("CUBA."):
        return string[5:]

    return string
