import os
import unittest
from simphony_metaedit.parsers.yamldirparser import YamlDirParser, \
    parse_cuba_type_data
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
        for entry, level in nodes.traverse(root):
            print "  "*level, entry
        self.assertEqual(len(list(nodes.traverse(root))), 100)

    def test_parse_cuba_type(self):
        res = parse_cuba_type_data("POSITION", {
            "definition": "position",
            "shape": [3],
            "type": "string",
        })

        self.assertEqual(res.name, "POSITION")
        self.assertEqual(res.definition, "position")
        self.assertEqual(res.shape, [3])
        self.assertEqual(res.type, "double")

