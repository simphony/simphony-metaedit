from traits.api import Instance, on_trait_change
from traitsui.api import (
    ModelView, View, Item, Tabbed, HGroup, UItem, TreeEditor, TreeNode)

from simphony_metaedit.cuds_item_model_view import CUDSItemModelView
from simphony_metaedit.cuba_data_type_model_view import CUBADataTypeModelView
from simphony_metaparser import nodes

cuds_editor = TreeEditor(
    nodes=[
        TreeNode(
            node_for=[nodes.CUDSItem],
            auto_open=True,
            children="children",
            label='name',
            menu=False,
            rename_me=False,
            delete_me=False,
        ),
    ],
    editable=False,
    selected='selected_cuds',
)


cuba_editor = TreeEditor(
    nodes=[
        TreeNode(
            node_for=[nodes.Ontology],
            auto_open=False,
            rename_me=False,
            delete_me=False,
            menu=False,
            label='=CUBA Data Types',
            children="data_types",
        ),
        TreeNode(
            node_for=[nodes.CUBADataType],
            rename_me=False,
            delete_me=False,
            menu=False,
            auto_open=False,
            label='name',
        ),
    ],
    editable=False,
    hide_root=True,
    selected="selected_cuba",
)


class App(ModelView):
    """Main application class."""

    #: The main model, the root of the hierarchy.
    model = Instance(nodes.Ontology)

    #: The associated view.
    selected_cuds = Instance(nodes.CUDSItem)
    selected_cuba = Instance(nodes.CUBADataType)

    #: Presenter for the selected CUDSItem
    selected_cuds_model_view = Instance(CUDSItemModelView)
    selected_cuba_model_view = Instance(CUBADataTypeModelView)

    #: The view
    traits_view = View(
        Tabbed(
            HGroup(
                Item(
                    'object.model.root_cuds_item',
                    editor=cuds_editor,
                    resizable=True,
                    show_label=False,
                ),
                UItem("selected_cuds_model_view"),
                label="CUDS Items"
            ),
            HGroup(
                Item(
                    'model',
                    editor=cuba_editor,
                    resizable=True,
                    show_label=False,
                ),
                UItem("selected_cuba_model_view"),
                label="CUBA Data Types",
            )
        ),
        title='Simphony Metadata',
        resizable=True,
        style='custom',
        width=1.0,
        height=1.0
    )

    @on_trait_change("selected_cuds")
    def _update_selected_cuds_model_view(self, value):
        """
        Syncs the selected_cuds_model_view with the newly selected
        selected_cuds
        """
        self.selected_cuds_model_view = CUDSItemModelView(model=value)

    @on_trait_change("selected_cuba")
    def _update_selected_cuba_model_view(self, value):
        """
        Syncs the selected_cuba_model_view with the newly selected
        selected_cuba
        """
        self.selected_cuba_model_view = CUBADataTypeModelView(model=value)
