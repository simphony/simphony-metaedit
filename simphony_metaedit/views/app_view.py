from traitsui.api import View, TreeEditor, TreeNode, Item, Tabbed
from simphony_metaparser import nodes

from .no_view import no_view

# Representation of the CUDS Items tree
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


# Representation of the CUBA Data Types.
cuba_editor = TreeEditor(
    nodes=[
        TreeNode(
            node_for=[nodes.Ontology],
            auto_open=False,
            label='=CUBA Data Types',
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


# The application view
app_view = View(
    Tabbed(
        Item(
            'object.ontology.root_cuds_item',
            editor=cuds_editor,
            resizable=True,
            show_label=False,
            label="CUDS Items"
        ),
        Item(
            'ontology',
            editor=cuba_editor,
            resizable=True,
            show_label=False,
            label="CUBA Data Types"
        ),
    ),
    title='Simphony Metadata',
    resizable=True,
    style='custom',
    width=1.0,
    height=1.0
)

