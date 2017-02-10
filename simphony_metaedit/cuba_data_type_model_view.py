from traits.api import on_trait_change
from traitsui.api import VGroup, View, Item, ModelView, CSVListEditor


class CUBADataTypeModelView(ModelView):
    """Wraps the CUBADataType node in a ModelView for easier representation
    and access.
    """
    traits_view = View(
            VGroup(
                Item(
                    "model.name",
                    resizable=True
                ),
                Item(
                    "model.definition",
                    resizable=True
                ),
                Item("model.type"),
                Item("model.shape", editor=CSVListEditor()),
                Item(
                    "model.length",
                    visible_when="model.type == 'string'"
                ),

                label="CUBA Data Type",
                show_border=True,
            ))

    @on_trait_change("model.type")
    def _type_updated(self, type_):
        if type_ == "string":
            self.model.length = 128
        else:
            self.model.length = None
