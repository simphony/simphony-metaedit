from traitsui.api import ModelView, View, Item


class VariablePropertyModelView(ModelView):
    traits_view = View(
        Item("model.name"),
        Item("model.scope"),
        Item("model.shape",
             visible_when="model.scope == 'CUBA.USER'"),
        Item("model.default",
             visible_when="model.scope == 'CUBA.USER'"),
    )

