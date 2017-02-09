from traits.has_traits import on_trait_change
from traits.trait_types import Either
from traitsui.group import Tabbed
from traitsui.list_str_adapter import ListStrAdapter

from simphony_metaedit.fixed_property_model_view import FixedPropertyModelView
from simphony_metaedit.variable_property_model_view import \
    VariablePropertyModelView
from simphony_metaparser.nodes import FixedPropertyEntry, VariablePropertyEntry
from traits.api import Property, List, Instance
from traitsui.api import VGroup, View, Item, ModelView, UItem, HGroup
from traitsui.editors import ListStrEditor

from simphony_metaparser.utils import traverse_to_root


class PropertyAdapter(ListStrAdapter):
    """Used to adapt the property nodes to something visually representable
    as a list of strings.
    """
    def get_text(self, object, trait, index):
        if self.item in object.inherited_properties:
            return self.item.name + " (from {})".format()

        return self.item.name

    def get_text_color(self, object, trait, index):
        # Paint the inherited properties pink
        if self.item in object.inherited_properties:
            return "#FFC0C0"

        return super(PropertyAdapter, self).get_text_color(object,
                                                           trait,
                                                           index)


class CUDSItemModelView(ModelView):
    """Wraps the CUDSItem node in a ModelView for easier representation
    and access."""
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
                                selected="selected_fixed_property"
                            ),
                        ),
                        UItem("selected_fixed_property_model_view",
                              style="custom"),
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

    #: A list of the fixed and variable properties.
    fixed_properties = Property(List(FixedPropertyEntry),
                                depends_on="model")
    variable_properties = Property(List(VariablePropertyEntry),
                                   depends_on="model")

    inherited_properties = Property(
        Either(
            List(FixedPropertyEntry),
            List(VariablePropertyEntry)
        ),
        depends_on="model"
    )

    selected_fixed_property = Instance(FixedPropertyEntry)
    selected_variable_property = Instance(VariablePropertyEntry)

    selected_variable_property_model_view = Instance(VariablePropertyModelView)
    selected_fixed_property_model_view = Instance(FixedPropertyModelView)

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

    @on_trait_change("selected_variable_property")
    def _update_selected_variable_property_model_view(self, value):
        """Syncs the modelview with the changed selected property"""
        self.selected_variable_property_model_view = VariablePropertyModelView(
            model=self.selected_variable_property)

    @on_trait_change("selected_fixed_property")
    def _update_selected_fixed_property_model_view(self, value):
        """Syncs the modelview with the changed selected property"""
        self.selected_fixed_property_model_view = FixedPropertyModelView(
            model=self.selected_fixed_property)

    def _extract_properties_by_type(self, prop_type):
        """Helper method. Extracts the properties (both inherited
        and defined on the object) of a given type (e.g. either
        FixedPropertyEntry or VariablePropertyEntry).

        Parameters
        ----------
        prop_type: nodes.FixedPropertyEntry or nodes.VariablePropertyEntry

        Returns
        -------
        list of nodes.
        """
        obj_properties = [
            p for p in self.model.property_entries.values()
            if isinstance(p, prop_type)]

        inherited_properties = [
            p for p in self.inherited_properties if isinstance(p, prop_type)]

        return obj_properties + inherited_properties
