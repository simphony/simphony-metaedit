from traitsui.api import (
    View, TreeEditor, TreeNode, Item, VGroup,
    CSVListEditor)

from simphony_metaparser import nodes


# Visualization of the CUDS Items internal data
# Representation of the CUDS Items tree
cuds_editor = TreeEditor(
    nodes=[
        TreeNode(
            node_for=[nodes.CUDSItem],
            auto_open=True,
            children="children",
            label='name',
        ),
    ],
    editable=False,
    selected='selected_cuds',
)

# Representation of the CUBA Data types
cuba_data_view = View(
    VGroup(
        Item("name"),
        Item("definition"),
        Item("type"),
        Item("shape", editor=CSVListEditor()),
        Item("length", visible_when="type == 'string'"),
        label="CUBA Data Types",
        show_border=True
    )
)

# Representation of the CUBA Data Types.
cuba_editor = TreeEditor(
    nodes=[
        TreeNode(
            node_for=[nodes.Ontology],
            auto_open=False,
            label='=CUBA Data Types',
            children="data_types",
        ),
        TreeNode(
            node_for=[nodes.CUBADataType],
            auto_open=False,
            label='name',
        ),
    ],
    editable=False,
    hide_root=True,
)
