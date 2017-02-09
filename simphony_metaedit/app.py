from traits.api import Instance, on_trait_change
from traitsui.api import ModelView
from traitsui.api import View, Item, Tabbed, HGroup, UItem

from simphony_metaedit.cuds_item_model_view import CUDSItemModelView
from simphony_metaedit.views.app_view import cuds_editor, cuba_editor
from simphony_metaparser import nodes


class App(ModelView):
    """Main application class."""

    #: The main model, the root of the hierarchy.
    model = Instance(nodes.Ontology)

    #: The associated view.
    selected_cuds = Instance(nodes.CUDSItem)

    #: Presenter for the selected CUDSItem
    selected_cuds_view_model = Instance(CUDSItemModelView)

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
                UItem("selected_cuds_view_model"),
                label="CUDS Items"
            ),
            HGroup(
                Item(
                    'model',
                    editor=cuba_editor,
                    resizable=True,
                    show_label=False,
                ),
                label="CUBA Data Types"
            )
        ),
        title='Simphony Metadata',
        resizable=True,
        style='custom',
        width=1.0,
        height=1.0
    )

    @on_trait_change("selected_cuds")
    def _update_selected_cuds_view_model(self, value):
        """
        Syncs the selected_cuds_view_model with the newly selected
        selected_cuds
        """
        self.selected_cuds_view_model = CUDSItemModelView(model=value)
