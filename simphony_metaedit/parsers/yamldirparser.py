import os
import yaml
from .. import nodes


class YamlDirParser:
    """Parser for the current format of metadata as two files in a directory"""

    def parse(self, directory):
        """Parses a directory containing file and extracts the tree."""

        root = nodes.RootNode()
        nodemap = {'': root}

        with open(os.path.join(directory, "cuba.yml")) as f:
            cuba_data = yaml.safe_load(f)

        nodemap.update(
            {"CUBA."+name: nodes.EntryNode(name="CUBA."+name)
             for name, _ in cuba_data.get("CUBA_KEYS", {}).items()})

        with open(os.path.join(directory, "simphony_metadata.yml")) as f:
            cuds_data = yaml.safe_load(f)

        # We need to collect all cuds entities first, because in the file
        # they are a dictionary, and they can be recovered in arbitrary order.
        nodemap.update(
            {"CUBA."+name: nodes.EntryNode(name="CUBA."+name)
             for name, class_data in cuds_data.get("CUDS_KEYS", {}).items()})

        # Second pass to set the parent-child relationship
        for name, class_info in cuds_data.get("CUDS_KEYS", {}).items():
            name = "CUBA."+name
            parent_name = class_info.get("parent")
            if not parent_name:
                parent_name = ""
            parent_name = parent_name.strip()
            parent = nodemap[parent_name]
            node = nodemap[name]
            parent.children.append(node)

        return root
