from traits.has_traits import on_trait_change

from simphony_metaparser.flags import NoDefault
from traits.api import Bool
from traitsui.api import ModelView, View, Item, TextEditor
import ast


# evaluate/format routines for some traits.
def shape_evaluate_func(value):
    """Converts the string value to an appropriate python entity.
    In this case, it must be a list"""
    return ast.literal_eval(value)


def shape_format_func(value):
    """Converts the value into a string so that the user can specify
    the value"""
    return str(list(value))


def default_evaluate_func(value):
    """Converts the string passed for the default value to
    an appropriate python entry.
    """
    return ast.literal_eval(value)


def default_format_func(value):
    """Converts the value into a string so that the user can specify
    the value"""
    return str(value)


class VariablePropertyModelView(ModelView):
    #: Presents the checkbox for setting the presence of a default.
    has_default = Bool(tooltip="Enabled if the value has a "
                               "specified default.")

    def default_traits_view(self):
        return View(
            Item("model.name",
                 enabled_when="False"),
            Item("model.scope",
                 enabled_when="False"),
            Item("model.shape",
                 visible_when="model.scope == 'CUBA.USER'",
                 enabled_when="False",
                 editor=TextEditor(
                     evaluate=shape_format_func,
                     format_func=shape_format_func,
                     )
                 ),
            Item(
                "has_default",
                enabled_when="False",
            ),
            Item(
                "model.default",
                visible_when="model.scope == 'CUBA.USER' "
                             "and has_default",
                enabled_when="False",
                editor=TextEditor(
                    evaluate=default_evaluate_func,
                    format_func=default_format_func
                    ),
                style="custom"
            ),
        )

    def _has_default_default(self):
        return self.model.default is not NoDefault

    @on_trait_change("has_default")
    def _update_default(self, value):
        if value is False:
            self.model.default = NoDefault
        else:
            self.model.default = None
