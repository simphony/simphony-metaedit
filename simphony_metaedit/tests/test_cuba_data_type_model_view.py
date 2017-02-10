import unittest

from pyface.ui.qt4.util.gui_test_assistant import GuiTestAssistant

from simphony_metaedit.cuba_data_type_model_view import CUBADataTypeModelView
from simphony_metaparser.nodes import CUBADataType


class TestCUBADataTypeModelView(GuiTestAssistant, unittest.TestCase):
    def test_view(self):
        model = CUBADataType(type="string",
                             shape=[1],
                             length=128,
                             name="CUBA.FOO")

        ui = None
        try:
            with self.event_loop_with_timeout(timeout=10):
                ui = CUBADataTypeModelView(model=model).edit_traits()
        finally:
            if ui is not None:
                with self.event_loop():
                    ui.dispose()

    def test_type_change(self):
        model = CUBADataType(type="string",
                             shape=[1],
                             length=128,
                             name="CUBA.FOO")

        mv = CUBADataTypeModelView(model=model)

        model.type = "integer"
        self.assertEqual(model.length, None)

        model.type = "string"
        self.assertEqual(model.length, 128)
