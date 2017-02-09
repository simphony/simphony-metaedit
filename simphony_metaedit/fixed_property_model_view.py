from traitsui.api import ModelView, View, Item


class FixedPropertyModelView(ModelView):
    """Model View for the FixedPropertyEntry."""

    traits_view = View(
        Item("model.name"),
        Item("model.scope"),
        Item("model.default", visible_when="model.scope == 'CUBA.USER'"),
    )
