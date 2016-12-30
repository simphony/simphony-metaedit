import yaml

from .exceptions import ParsingError
from .. import nodes


class CubaFileParser:
    def parse(self, file_handle):
        """Parses the content of the specified file.
        Returns a list of raw nodes for further processing.

        Parameters
        ----------
        file_handle: file object
            file to parse

        Returns
        -------
        list of raw CUBA nodes.
        """
        cuba_data = yaml.safe_load(file_handle)

        nodemap = {}

        for name, data in cuba_data.get("CUBA_KEYS", {}).items():
            if name in nodemap:
                raise ParsingError("Duplicate entry {} in "
                                   "{}".format(name, file_handle))

            try:
                raw_cuba_type = _parse_raw_cuba_type_data(name, data)
            except Exception as e:
                raise ParsingError("Unable to parse entry {} "
                                   "in {}: {}".format(name,
                                                      file_handle,
                                                      str(e)))
            nodemap[raw_cuba_type.name] = raw_cuba_type

        return nodemap.values()


def _parse_raw_cuba_type_data(name, data):
    """Parses the content of the node from the direct yaml parsed content

    Parameters
    ----------
    name: str
        The name of the node

    data: dict
        The data _under_ the yaml node with the specified name

    Returns
    -------
    nodes.RawCubaType
    """
    return nodes.RawCubaType(
        name=name,
        definition=data.get("definition", ""),
        type=data["type"],
        shape=data["shape"]
    )


