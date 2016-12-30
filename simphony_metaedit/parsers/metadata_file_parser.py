import yaml
from .exceptions import ParsingError
from .. import nodes


class MetadataFileParser:
    def parse(self, file_handle):
        """Parses the content of the specified filename.
        Returns a list of raw nodes for further processing.

        Parameters
        ----------
        file_handle: str
            Path of the file to parse

        Returns
        -------
        list of raw metadata nodes.
        """
        cuds_data = yaml.safe_load(file_handle)

        nodemap = {}
        # We need to collect all cuds entities first, because in the file
        # they are a dictionary, and they can be recovered in arbitrary order.
        for name, data in cuds_data.get("CUDS_KEYS", {}).items():
            if name in nodemap:
                raise ParsingError("Duplicate entry {} in "
                                   "{}".format(name, file_handle))
            try:
                raw_concept = _parse_raw_concept(name, data)
            except Exception as e:
                raise ParsingError("Unable to parse entry {} "
                                   "in {}: {}".format(name,
                                                      file_handle,
                                                      str(e)))

            nodemap[raw_concept.name] = raw_concept

        return nodemap.values()


def _parse_raw_concept(concept_name, raw_concept_data):
    """Parses the content of the node from the direct yaml parsed content

    Parameters
    ----------
    concept_name: str
        The name of the node

    raw_concept_data: dict
        The data _under_ the yaml node with the specified name

    Returns
    -------
    nodes.RawConcept
    """
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


