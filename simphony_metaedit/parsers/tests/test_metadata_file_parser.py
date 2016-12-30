import os
import unittest
from simphony_metaedit import nodes
from simphony_metaedit.parsers.metadata_file_parser import (
    MetadataFileParser,
    _parse_raw_concept)


class TestYamlDirParser(unittest.TestCase):
    def setUp(self):
        self.yamldir = os.path.join(
            os.path.dirname(__file__),
            'fixtures',
            'yaml_files')

    def test_parse_metadata_file(self):
        parser = MetadataFileParser()
        with open(os.path.join(self.yamldir, "simphony_metadata.yml")) as f:
            nodes = parser.parse(f)
        self.assertEqual(len(nodes), 99)

    def test_parse_raw_concept(self):
        node = _parse_raw_concept("MIXTURE_MODEL", {
            "definition": "mixture (drift flux) model",
            "parent": "CUBA.PHYSICS_EQUATION",
            "models": ["CUBA.CONTINUUM"]
        })

        self.assertIsInstance(node, nodes.RawConcept)
        self.assertEqual(node.name, "MIXTURE_MODEL")
