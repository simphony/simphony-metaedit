import unittest
import os

from simphony_metaedit.app import App
from simphony_metaparser import nodes
from simphony_metaparser.yamldirparser import YamlDirParser


class TestApp(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "fixtures",
            "yaml_files"
        )
        parser = YamlDirParser()
        self.ontology = parser.parse(self.path)

    def test_initialization(self):
        app = App(model=self.ontology)
        self.assertIsInstance(app.model, nodes.Ontology)
        self.assertNotEqual(len(app.model.data_types), 0)
