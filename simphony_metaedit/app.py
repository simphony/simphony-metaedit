import os
from traits.api import Any, HasTraits, Instance
from traitsui.api import View, TreeNode, Group, Item, TreeEditor
# import yaml
import logging

from . import nodes

no_view = View()


def _tree_editor(selected):
    """Return a TreeEditor specifically for HDF5 file trees."""
    return TreeEditor(
        nodes=[
            TreeNode(
                node_for=[nodes.RootNode],
                auto_open=True,
                children='children',
                label='name',
                view=no_view,
            ),
            TreeNode(
                node_for=[nodes.FileNode],
                auto_open=True,
                children='children',
                label='name',
                view=no_view,
            ),
            TreeNode(
                node_for=[nodes.EntryNode],
                auto_open=False,
                children='children',
                label='name',
                view=no_view,
            ),
        ],
        editable=False,
        selected=selected,
    )


def _tree_from_file(filename):
    file_node = nodes.FileNode(name=os.path.basename(filename))
    # with open(filename) as f:
    #    yml_data = yaml.safe_load(f)

    # cuds_entries = []
    # cuba_entries = []
    # cuds_roots = []

    # for key, class_data in yml_data.get('CUDS_KEYS', {}).items():
    #    parent = class_data.get("parent")
    #
    #    if not parent:
    #        cuds_roots.append(key)

    #    cuds_entries.append((key, parent))

    # for key, class_data in yml_data.get('CUBA_KEYS', {}).items():
    #    cuba_entries.append(key)

    # Reorganize
    # file_node.children = entries
    return file_node


class App(HasTraits):
    root = Instance(nodes.RootNode)
    selected = Any

    traits_view = View(
        Group(
            Item('root',
                 editor=_tree_editor(selected='selected'),
                 resizable=True
                 ),
            orientation='vertical',
        ),
        title='Simphony Metadata',
        buttons=['Undo', 'OK', 'Cancel'],
        resizable=True,
        width=.3,
        height=.3
    )

    def _selected_changed(self):
        print(self.selected.path)

    def _root_default(self):
        return nodes.RootNode()

    def __init__(self, directory):
        logging.debug("parsing directory {}".format(directory))

        try:
            files = os.listdir(directory)
        except OSError as e:
            logging.exception("Could not open directory {}".format(directory))
            return

        for filename in files:
            if filename.endswith(".yml"):
                try:
                    tree = _tree_from_file(os.path.join(directory, filename))
                except Exception as e:
                    logging.exception("Could not parse {}".format(filename))
                else:
                    self.root.children.append(tree)
