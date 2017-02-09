from traits.has_traits import on_trait_change
from traits.trait_types import Either, Bool
from traitsui.group import Tabbed
from traitsui.list_str_adapter import ListStrAdapter

from simphony_metaedit.fixed_property_model_view import FixedPropertyModelView
from simphony_metaedit.variable_property_model_view import \
    VariablePropertyModelView
from simphony_metaparser.nodes import FixedProperty, VariableProperty
from traits.api import Property, List, Instance
from traitsui.api import VGroup, View, Item, ModelView, UItem, HGroup
from traitsui.editors import ListStrEditor

from simphony_metaparser.utils import traverse_to_root


class PropertyAdapter(ListStrAdapter):
    """Used to adapt the property nodes to something visually representable
    as a list of strings.
    """
    def get_text(self, object, trait, index):
        # To reduce confusion
        prop = self.item

        if prop in object.inherited_properties:
            return prop.name + " (from {})".format(prop.item.name)

        return prop.name

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
                            "all_fixed_properties",
                            editor=ListStrEditor(
                                adapter=PropertyAdapter(),
                                selected="selected_fixed_property"
                            ),
                        ),
                        UItem(
                            "selected_fixed_property_model_view",
                            style="custom",
                            enabled_when="fixed_property_model_view_enabled"
                        ),
                    ),
                    label="Fixed Properties",
                    show_border=True,
                ),
                HGroup(
                    VGroup(
                        UItem(
                            "all_variable_properties",
                            editor=ListStrEditor(
                                adapter=PropertyAdapter(),
                                selected="selected_variable_property"),
                        ),
                        UItem(
                            "selected_variable_property_model_view",
                            style="custom",
                            enabled_when="variable_property_model_view_enabled"
                        ),
                    ),
                    label="Variable Properties",
                    show_border=True,
                ),
            )
        )
    )

    #: A list of the fixed and variable properties on the CUDSItem
    #: we are visualising, and only that object.
    obj_fixed_properties = Property(
        List(FixedProperty),
        depends_on="model")
    obj_variable_properties = Property(
        List(VariableProperty),
        depends_on="model")

    #: A list of the fixed and variable properties on the CUDSItem
    #: we are visualising. This includes all those that we inherit
    all_fixed_properties = Property(
        List(FixedProperty),
        depends_on="model")
    all_variable_properties = Property(
        List(VariableProperty),
        depends_on="model")

    #: The properties that we inherit from the base CUDSItems.
    inherited_properties = Property(
        Either(
            List(FixedProperty),
            List(VariableProperty)
        ),
        depends_on="model"
    )

    #: The properties that are selected by the user when they click
    selected_fixed_property = Instance(FixedProperty)
    selected_variable_property = Instance(VariableProperty)

    #: The ModelViews of the above, to allow controlled presentation.
    selected_variable_property_model_view = Instance(VariablePropertyModelView)
    selected_fixed_property_model_view = Instance(FixedPropertyModelView)

    #: State that says if the editor window should be enabled or not
    #: Inherited variables cannot be edited on a derived class.
    fixed_property_model_view_enabled = Bool()
    variable_property_model_view_enabled = Bool()

    def _get_obj_fixed_properties(self):
        """Gets the fixed properties, only local to the object"""
        return [
            p for p in self.model.properties.values()
            if isinstance(p, FixedProperty)
            ]

    def _get_obj_variable_properties(self):
        """Gets the variable properties, only local to the object"""
        return [
            p for p in self.model.properties.values()
            if isinstance(p, VariableProperty)
            ]

    def _get_all_fixed_properties(self):
        """Gets all the fixed properties, both local to the object
        and from its hierarchy"""
        inherited_properties = [
            p for p in self.inherited_properties
            if isinstance(p, FixedProperty)]

        return self.obj_fixed_properties + inherited_properties

    def _get_all_variable_properties(self):
        """Gets all the variable properties, both local to the object
        and from its hierarchy"""
        inherited_properties = [
            p for p in self.inherited_properties
            if isinstance(p, VariableProperty)]
        return self.obj_variable_properties + inherited_properties

    def _get_inherited_properties(self):
        """Gets all the inherited properties."""
        parent_classes = list(traverse_to_root(self.model))[1:]
        inherited_properties = []
        for parent in parent_classes:
            inherited_properties += [
                p for p in parent.properties.values()
            ]

        return inherited_properties

    @on_trait_change("selected_variable_property")
    def _update_selected_variable_property_model_view(self, value):
        """Syncs the modelview with the changed selected property"""
        self.selected_variable_property_model_view = VariablePropertyModelView(
            model=self.selected_variable_property)
        self.variable_property_model_view_enabled = \
            self.selected_variable_property in self.obj_variable_properties

    @on_trait_change("selected_fixed_property")
    def _update_selected_fixed_property_model_view(self, value):
        """Syncs the modelview with the changed selected property"""
        self.selected_fixed_property_model_view = FixedPropertyModelView(
            model=self.selected_fixed_property)
        self.fixed_property_model_view_enabled = \
            self.selected_fixed_property in self.obj_fixed_properties
