import unittest
import os

from simphony_metaedit.app import App
from simphony_metaparser import nodes


class TestApp(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "fixtures",
            "yaml_files"
        )

    def test_initialization(self):
        app = App(self.path)
        self.assertIsInstance(app.ontology, nodes.Ontology)
        self.assertNotEqual(len(app.ontology.data_types), 0)
