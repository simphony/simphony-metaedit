import os
import logging

from traits.api import Any, HasTraits, Instance
from traitsui.api import View, TreeNode, Group, Item, TreeEditor

from simphony_metaedit.parsers.yamldirparser import YamlDirParser
from . import nodes


no_view = View()


tree_editor = TreeEditor(
    nodes=[
        TreeNode(
            node_for=[nodes.RootNode],
            auto_open=True,
            children='children',
            label='name',
            view=View(["name"]),
        ),
        TreeNode(
            node_for=[nodes.EntryNode],
            auto_open=False,
            children='children',
            label='name',
            view=View(["name"]),
        ),
    ],
    editable=True,
    selected='selected',
)


class App(HasTraits):
    root = Instance(nodes.RootNode)
    selected = Any

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
        return nodes.RootNode()

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
            root = parser.parse(directory)
        except Exception:
            logging.exception("Could not parse {}".format(directory))
        else:
            self.root = root


