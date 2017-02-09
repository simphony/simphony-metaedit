import unittest

from simphony_metaedit.variable_property_model_view import \
    VariablePropertyModelView
from simphony_metaparser.nodes import VariableProperty


class TestVariablePropertyModelView(unittest.TestCase):
    def test_no_default(self):
        variable_property = VariableProperty(name="CUBA.NAME",
                                             shape=[1],
                                             scope="CUBA.USER",
                                             default="hello")
        mv = VariablePropertyModelView(model=variable_property)
        self.assertTrue(mv.has_default)
