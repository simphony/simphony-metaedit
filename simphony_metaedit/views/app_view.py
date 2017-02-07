from traitsui.api import View, TreeEditor, TreeNode, Item, Tabbed
from traitsui.group import VGroup

from simphony_metaedit.views.no_view import no_view
from simphony_metaparser import nodes


# Visualization of the CUDS Items internal data
cuds_item_view = View(
    VGroup(
        VGroup(
            Item("name", full_size=True),
            label="CUDS Item Data",
            show_border=True,
        ),
        VGroup(
            label="Fixed Properties",
            show_border=True,
        ),
        VGroup(
            label="Variable Properties",
            show_border=True,
        ),
    )
)

# Representation of the CUDS Items tree
cuds_editor = TreeEditor(
    nodes=[
        TreeNode(
            node_for=[nodes.CUDSItem],
            auto_open=True,
            children="children",
            label='name',
            view=cuds_item_view
        ),
    ],
    editable=True,
    selected='selected',
)

# Representation of the CUBA Data types
cuba_data_view = View(
    VGroup(
        Item("name"),
        Item("definition"),
        Item("type"),
        Item("shape"),
        Item("length"),
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
            view=no_view
        ),
        TreeNode(
            node_for=[nodes.CUBADataType],
            auto_open=False,
            label='name',
            view=cuba_data_view
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
