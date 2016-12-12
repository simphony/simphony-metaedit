import os
import unittest
from simphony_metaedit.parsers.yamldirparser import (
    YamlDirParser,
    _parse_raw_cuba_type_data,
    _parse_cuba_file,
    _parse_metadata_file,
    _parse_raw_concept)

from simphony_metaedit import nodes


class TestYamlDirParser(unittest.TestCase):
    def setUp(self):
        self.yamldir = os.path.join(
            os.path.dirname(__file__),
            'fixtures',
            'yaml_files')

    def test_initialization(self):
        parser = YamlDirParser()

        root = parser.parse(self.yamldir)
        self.assertEqual(type(root), nodes.Root)
        self.assertEqual(len(list(nodes.traverse(root))), 218)

    def test_parse_raw_cuba_type(self):
        res = _parse_raw_cuba_type_data("POSITION", {
            "definition": "position",
            "shape": [3],
            "type": "double",
        })

        self.assertEqual(res.name, "POSITION")
        self.assertEqual(res.definition, "position")
        self.assertEqual(res.shape, [3])
        self.assertEqual(res.type, "double")

    def test_parse_cuba_file(self):
        nodes = _parse_cuba_file(os.path.join(self.yamldir, "cuba.yml"))
        self.assertEqual(len(nodes), 116)

    def test_parse_metadata_file(self):
        nodes = _parse_metadata_file(
            os.path.join(self.yamldir, "simphony_metadata.yml")
            )
        self.assertEqual(len(nodes), 99)

    def test_parse_raw_concept(self):
        node = _parse_raw_concept("MIXTURE_MODEL", {
            "definition": "mixture (drift flux) model",
            "parent": "CUBA.PHYSICS_EQUATION",
            "models": ["CUBA.CONTINUUM"]
        })

        self.assertIsInstance(node, nodes.RawConcept)
        self.assertEqual(node.name, "MIXTURE_MODEL")
