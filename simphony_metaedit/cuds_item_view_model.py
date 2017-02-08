from traits.has_traits import on_trait_change
from traits.trait_types import Either
from traitsui.group import Tabbed
from traitsui.list_str_adapter import ListStrAdapter

from simphony_metaedit.variable_property_view_model import \
    VariablePropertyModelView
from simphony_metaparser.nodes import FixedPropertyEntry, VariablePropertyEntry
from traits.api import Property, List, Instance
from traitsui.api import VGroup, View, Item, ModelView, UItem, HGroup
from traitsui.editors import ListStrEditor

from simphony_metaparser.utils import traverse_to_root


class PropertyAdapter(ListStrAdapter):
    def get_text(self, object, trait, index):
        if self.item in object.inherited_properties:
            return self.item.name + " (inherited)"

        return self.item.name

    def get_text_color(self, object, trait, index):
        if self.item in object.inherited_properties:
            return "#FFC0C0"

        return super(PropertyAdapter, self).get_text_color(object,
                                                           trait,
                                                           index)


class CUDSItemViewModel(ModelView):
    traits_view = View(
        VGroup(
            VGroup(
                Item("model.name"),
                label="CUDS Item Data",
                show_border=True,
            ),
            Tabbed(
                HGroup(
                    VGroup(
                        UItem(
                            "fixed_properties",
                            editor=ListStrEditor(
                                adapter=PropertyAdapter(),
                                selected="selected_fixed_property"),
                        ),
                        UItem("selected_fixed_property", style="custom"),
                    ),
                    label="Fixed Properties",
                    show_border=True,
                ),
                HGroup(
                    VGroup(
                        UItem(
                            "variable_properties",
                            editor=ListStrEditor(
                                adapter=PropertyAdapter(),
                                selected="selected_variable_property"),
                        ),
                        UItem("selected_variable_property_model_view",
                              style="custom"),
                    ),
                    label="Variable Properties",
                    show_border=True,
                ),
            )
        )
    )

    fixed_properties = Property(List(FixedPropertyEntry))
    variable_properties = Property(List(VariablePropertyEntry))

    inherited_properties = Property(Either(
        List(FixedPropertyEntry),
        List(VariablePropertyEntry)))

    selected_fixed_property = Instance(FixedPropertyEntry)
    selected_variable_property = Instance(VariablePropertyEntry)

    selected_variable_property_model_view = Instance(VariablePropertyModelView)

    def _get_fixed_properties(self):
        return self._extract_properties_by_type(FixedPropertyEntry)

    def _get_variable_properties(self):
        return self._extract_properties_by_type(VariablePropertyEntry)

    def _get_inherited_properties(self):
        parent_classes = list(traverse_to_root(self.model))[1:]
        inherited_properties = []
        for parent in parent_classes:
            inherited_properties += [
                p for p in parent.property_entries.values()
            ]

        return inherited_properties

    def _extract_properties_by_type(self, prop_type):
        obj_properties = [
            p for p in self.model.property_entries.values()
            if isinstance(p, prop_type)]

        inherited_properties = [
            p for p in self.inherited_properties if isinstance(p, prop_type)]

        return obj_properties + inherited_properties

    @on_trait_change("selected_variable_property")
    def _update_selected_variable_property_model_view(self, value):
        self.selected_variable_property_model_view = VariablePropertyModelView(
            model=self.selected_variable_property)
