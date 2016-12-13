import os
import logging

from traits.api import Any, HasTraits, Instance
from traitsui.api import View, TreeNode, Item, TreeEditor

from simphony_metaedit.parsers.yamldirparser import YamlDirParser
from . import nodes


# An empty view to show when the node has no reasonable View to show.
no_view = View()


# Representation of the tree, with the details on how to present each node.
tree_editor = TreeEditor(
    nodes=[
        TreeNode(
            node_for=[nodes.Root],
            auto_open=True,
            children='children',
            label='name',
            view=View(["path"]),
        ),
        TreeNode(
            node_for=[nodes.CubaTypes],
            auto_open=False,
            children='children',
            label='=CUBA Types',
            view=no_view
        ),
        TreeNode(
            node_for=[nodes.CubaType],
            auto_open=False,
            label='name',
            view=View(["name",
                       "definition",
                       "shape",
                       "type",
                       ]),
        ),
        TreeNode(
            node_for=[nodes.Concepts],
            auto_open=False,
            children='children',
            label='=Concepts',
            view=no_view
        ),
        TreeNode(
            node_for=[nodes.Concept],
            auto_open=False,
            children='children',
            label='name',
            view=View([
                "name",
                "definition"]),
        ),
        TreeNode(
            node_for=[nodes.Model],
            auto_open=False,
            icon_item="<list_editor>",
            label='ref',
            view=View([
                "ref",
            ]),
        ),
        TreeNode(
            node_for=[nodes.Variable],
            auto_open=False,
            label='ref',
            view=View([
                "ref",
            ]),
        ),
        TreeNode(
            node_for=[nodes.Property],
            icon_item="<object>",
            auto_open=False,
            label='ref',
            view=View([
                "ref",
                "default",
                "shape"
                ]),
        ),
    ],
    editable=True,
    selected='selected',
)


class App(HasTraits):
    """Main application class."""

    #: The main model, the root of the hierarchy.
    root = Instance(nodes.Root)

    view = View(
        Item('root',
             editor=tree_editor,
             resizable=True,
             show_label=False
             ),
        title='Simphony Metadata',
        resizable=True,
        style='custom',
        width=0.5,
        height=0.5
    )

    def _root_default(self):
        return nodes.Root()

    def __init__(self, directory):
        logging.debug("parsing directory {}".format(directory))

        try:
            files = os.listdir(directory)
        except OSError:
            logging.exception("Could not open directory {}".format(directory))
            return

        if "cuba.yml" in files and "simphony_metadata.yml" in files:
            parser = YamlDirParser()
        else:
            logging.error("Cannot find files for "
                          "directory {}".format(directory))
            return

        try:
            self.root = parser.parse(directory)
        except Exception:
            logging.exception("Could not parse {}".format(directory))
