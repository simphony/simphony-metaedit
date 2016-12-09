import os
import unittest
from simphony_metaedit.parsers.yamldirparser import YamlDirParser
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
        self.assertEqual(type(root), nodes.RootNode)

        self.assertEqual(len(list(nodes.traverse(root))), 100)

