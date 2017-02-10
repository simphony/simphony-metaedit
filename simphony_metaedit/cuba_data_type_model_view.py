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
                    resizable=True,
                    enabled_when="False"
                ),
                Item(
                    "model.definition",
                    resizable=True,
                    enabled_when="False"
                ),
                Item("model.type",
                     enabled_when="False"
                     ),
                Item("model.shape",
                     editor=CSVListEditor(),
                     enabled_when="False"
                     ),
                Item(
                    "model.length",
                    visible_when="model.type == 'string'",
                    enabled_when="False"
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
