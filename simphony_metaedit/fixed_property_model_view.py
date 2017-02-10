from traitsui.api import ModelView, View, Item, VGroup


class FixedPropertyModelView(ModelView):
    """Model View for the FixedPropertyEntry."""

    traits_view = View(
        VGroup(
            Item("model.name",
                 enabled_when="False"),
            Item("model.scope",
                 enabled_when="False"),
            Item("model.default",
                 enabled_when="False",
                 visible_when="model.scope == 'CUBA.USER'",
                 full_size=True,
                 style="custom"),
        )
    )
