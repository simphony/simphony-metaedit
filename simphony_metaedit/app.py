import logging

from traits.api import HasStrictTraits, Instance
from traitsui.api import View, TreeNode, TreeEditor, Item, Tabbed

from simphony_metaparser.yamldirparser import YamlDirParser
from simphony_metaparser import nodes


# An empty view to show when the node has no reasonable View to show.
no_view = View()


# Representation of the tree, with the details on how to present each node.
cuds_editor = TreeEditor(
    nodes=[
        TreeNode(
            node_for=[nodes.CUDSItem],
            auto_open=False,
            children="children",
            label='name',
            view=no_view
        ),
        TreeNode(
            node_for=[nodes.FixedPropertyEntry],
            auto_open=False,
            label='name',
            view=no_view
        ),
        TreeNode(
            node_for=[nodes.VariablePropertyEntry],
            auto_open=False,
            label='name',
            view=no_view
        ),
    ],
    editable=True,
    selected='selected',
)

cuba_editor = TreeEditor(
    nodes=[
        TreeNode(
            node_for=[nodes.Ontology],
            auto_open=False,
            label='=CUBA Types',
            children="data_types",
            view=no_view
        ),
        TreeNode(
            node_for=[nodes.CUBADataType],
            auto_open=False,
            label='name',
            view=no_view
        ),
    ],
    editable=True,
    selected='selected',
    hide_root=True,
)


class App(HasStrictTraits):
    """Main application class."""

    #: The main model, the root of the hierarchy.
    ontology = Instance(nodes.Ontology)

    view = \
        View(
            Tabbed(
                Item(
                    'object.ontology.root_cuds_item',
                    editor=cuds_editor,
                    resizable=True,
                    show_label=False,
                    label="CUDS"
                ),
                Item(
                    'ontology',
                    editor=cuba_editor,
                    resizable=True,
                    show_label=False,
                    label="CUBA"
                ),
            ),
            title='Simphony Metadata',
            resizable=True,
            style='custom',
            width=1.0,
            height=1.0
        )

    def _ontology_default(self):
        ontology = nodes.Ontology()
        ontology.root_cuds_item = nodes.CUDSItem(name="CUBA.ROOT")
        return ontology

    def __init__(self, directory):
        logging.debug("parsing directory {}".format(directory))

        parser = YamlDirParser()

        try:
            self.ontology = parser.parse(directory)
        except Exception as e:
            logging.exception("Could not parse {} : {}".format(
                directory,
                e)
            )
            self.reset_traits(['ontology'])

