import os
import unittest
from simphony_metaedit.parsers.cuba_file_parser import (
    CubaFileParser, _parse_raw_cuba_type_data)


class TestCubaFileParser(unittest.TestCase):
    def setUp(self):
        self.yamldir = os.path.join(
            os.path.dirname(__file__),
            'fixtures',
            'yaml_files')

    def test_parse_cuba_file(self):
        parser = CubaFileParser()
        with open(os.path.join(self.yamldir, "cuba.yml")) as f:
            nodes = parser.parse(f)
        self.assertEqual(len(nodes), 116)

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
