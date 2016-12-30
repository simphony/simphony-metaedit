import yaml
from traits.api import TraitError

from .exceptions import ParsingError
from .. import nodes


class CUBAFileParser:
    """Parser for the CUBA file. Returns raw nodes without further linkage"""

    # Trivial check: verify the file version before acting. We support only
    # these versions
    SUPPORTED_VERSIONS = ["1.0"]

    # The recognized keys for version 1.0 for the root of the yaml file
    _RECOGNIZED_KEYS_ROOT_1_0 = {
        "VERSION",
        "CUBA",
        "Resources",
        "Purpose",
        "CUBA_KEYS"}

    _RECOGNIZED_KEYS_CUBA_ENTRY_1_0 = {
        "shape",
        "length",
        "definition",
        "type"
    }

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
        try:
            cuba_data = yaml.safe_load(file_handle)
        except Exception as e:
            raise ParsingError("Unable to parse basic YAML "
                               "structure. {}".format(e))

        root_node = nodes.RawRootNode()

        unrecognized_keys = set(cuba_data.keys()).difference(
            self._RECOGNIZED_KEYS_ROOT_1_0)

        if len(unrecognized_keys) != 0:
            raise ParsingError("Unrecognized key(s) "
                               "in file: {}".format(unrecognized_keys))

        try:
            # I suspect that a value of 1.0 will come up as a float
            version = str(cuba_data["VERSION"]).strip()
            root_node.version = version
        except (KeyError, TraitError):
            raise ParsingError("Invalid or missing value for VERSION "
                               "in {}".format(file_handle))

        if root_node.version not in self.SUPPORTED_VERSIONS:
            raise ParsingError(
                "Parser does not support version {}. "
                "Supported versions are {}".format(
                    root_node.version,
                    self.SUPPORTED_VERSIONS
                )
            )
        root_node.purpose = cuba_data.get("Purpose", "")

        if "CUBA" not in cuba_data:
            raise ParsingError("Missing key CUBA in file")

        root_node.type = "CUBA"

        try:
            cuba_keys = cuba_data["CUBA_KEYS"]
        except KeyError:
            raise ParsingError(
                "Missing key CUBA_KEYS in {}".format(
                    file_handle))

        if not isinstance(cuba_keys, dict):
            raise ParsingError(
                "CUBA_KEYS must contain a mapping in {}".format(
                    file_handle))

        entries = {}
        for name, data in cuba_keys.items():
            try:
                entries[name] = self._parse_raw_cuba_entry_data(name, data)
            except TraitError as e:
                raise ParsingError("Unable to parse entry {} "
                                   "in {}: {}".format(name,
                                                      file_handle,
                                                      str(e)))

        root_node.entries = entries

        return root_node


    def _parse_raw_cuba_entry_data(self, name, data):
        """Parses the content of the node from the direct yaml parsed content

        Parameters
        ----------
        name: str
            The name of the node

        data: dict
            The data _under_ the yaml node with the specified name

        Returns
        -------
        nodes.RawCUBAEntry
        """

        # Check if there are unrecognized keys in the entry
        unrecognized_keys = set(data.keys()).difference(
            self._RECOGNIZED_KEYS_CUBA_ENTRY_1_0)

        if len(unrecognized_keys) != 0:
            raise ParsingError(
                "Unrecognized key(s) in CUBA entry {}: {}".format(
                    name, unrecognized_keys)
            )

        entry = nodes.RawCUBAEntry()
        entry.name = name
        entry.definition = data.get("definition", "")
        try:
            entry.type = data["type"]
        except KeyError:
            raise ParsingError("Unable to parse entry {}: "
                               "missing 'type'".format(name))

        shape = data.get("shape", [1])

        entry.shape = shape

        for s in entry.shape:
            if s <= 0:
                raise ParsingError("Invalid value for shape in {}".format(name))

        length = data.get("length")

        if entry.type != "string" and length is not None:
            raise ParsingError("length cannot be present if "
                               "entry type is not string in {}".format(name))

        entry.length = length

        if length is not None and length <= 0:
            raise ParsingError("Invalid value for length in {}".format(name))

        return entry
