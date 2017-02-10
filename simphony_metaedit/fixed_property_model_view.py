from traitsui.api import ModelView, View, Item, VGroup


class FixedPropertyModelView(ModelView):
    """Model View for the FixedPropertyEntry."""

    traits_view = View(
        VGroup(
            Item("model.name"),
            Item("model.scope"),
            Item("model.default",
                 visible_when="model.scope == 'CUBA.USER'",
                 full_size=True,
                 style="custom"),
        )
    )
