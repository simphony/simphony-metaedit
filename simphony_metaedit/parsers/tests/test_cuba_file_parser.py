import os
import unittest

from simphony_metaedit import nodes
from simphony_metaedit.parsers.exceptions import ParsingError
from simphony_metaedit.parsers.cuba_file_parser import (
    CUBAFileParser)

import StringIO

# Basic, working document that complies with the spec
TEMPLATE = """---
VERSION: 1.0

CUBA: Common Unified Base Attributes

Purpose: CUBA provides

CUBA_KEYS:
    UUID:
        definition: unique id
        length: 32
        type: string

    POSITION:
        definition: Position of a point or node or atom
        shape: [3]
        type: double

    MATRIX:
        definition: A Matrix
        shape: [3, 3]
        type: double

    SIMPLE_DOUBLE:
        type: double
"""


class TestCUBAFileParser(unittest.TestCase):
    def setUp(self):
        self.yamldir = os.path.join(
            os.path.dirname(__file__),
            'fixtures',
            'yaml_files')
        self.parser = CUBAFileParser()

    def test_parse_cuba_real_file(self):
        with open(os.path.join(self.yamldir, "cuba.yml")) as f:
            root = self.parser.parse(f)
        self.assertEqual(len(root.entries), 116)

    def test_trivial_content(self):
        content = StringIO.StringIO(TEMPLATE)
        root = self.parser.parse(content)

        self.assertIsInstance(root, nodes.RawRootNode)
        self.assertEqual(root.version, "1.0")
        self.assertEqual(root.purpose, "CUBA provides")
        self.assertEqual(root.type, "CUBA")
        self.assertEqual(len(root.entries), 4)
        self.assertEqual(root.entries["UUID"].length, 32)
        self.assertEqual(root.entries["UUID"].type, "string")
        self.assertEqual(root.entries["UUID"].definition, "unique id")
        self.assertEqual(root.entries["UUID"].shape, [1])

        self.assertEqual(root.entries["POSITION"].shape, [3])
        self.assertEqual(root.entries["MATRIX"].shape, [3, 3])

    def test_parse_incorrect_version(self):
        content = StringIO.StringIO(
            _change_lines_starting_with(TEMPLATE, "VERSION", ""))
        with self.assertRaisesRegexp(ParsingError,
                                     "Invalid or missing value for VERSION"):
            self.parser.parse(content)

        for version in ["hello", "[]"]:
            content = StringIO.StringIO(
                _change_lines_starting_with(
                    TEMPLATE,
                    "VERSION",
                    "VERSION: {}".format(version)))
            with self.assertRaisesRegexp(
                    ParsingError,
                    "Invalid or missing value for VERSION"):
                self.parser.parse(content)

        for version in ["1.1", "0.9"]:
            content = StringIO.StringIO(
                _change_lines_starting_with(
                    TEMPLATE,
                    "VERSION",
                    "VERSION: {}".format(version)))
            with self.assertRaisesRegexp(ParsingError, "does not support"):
                self.parser.parse(content)

    def test_parse_incorrect_cuba_marker(self):
        content = StringIO.StringIO(
            _change_lines_starting_with(TEMPLATE, "CUBA:", "")
        )

        with self.assertRaisesRegexp(ParsingError,
                                     "Missing key CUBA"):
            self.parser.parse(content)

    def test_no_cuba_keys(self):
        content = StringIO.StringIO(_extract_lines(TEMPLATE, 0, 7))
        with self.assertRaisesRegexp(ParsingError, "Missing key CUBA_KEYS"):
            self.parser.parse(content)

    def test_unrecognized_root_key(self):
        content = StringIO.StringIO(TEMPLATE+"\nunrecognized: 1\n")
        with self.assertRaisesRegexp(ParsingError, "Unrecognized key"):
            self.parser.parse(content)

    def test_invalid_cuba_name(self):
        content = StringIO.StringIO(
            TEMPLATE+"""
    whatever:
        definition: Position of a point or node or atom
        shape: [3]
        type: double
""")
        with self.assertRaisesRegexp(ParsingError, "matching the pattern"):
            self.parser.parse(content)

    def test_no_type(self):
        content = StringIO.StringIO(
            TEMPLATE+"""
    WHATEVER:
        definition: Position of a point or node or atom
        shape: [3]
""")
        with self.assertRaisesRegexp(ParsingError, "missing 'type'"):
            self.parser.parse(content)

    def test_unrecognized_type(self):
        content = StringIO.StringIO(
            TEMPLATE+"""
    WHATEVER:
        definition: Position of a point or node or atom
        shape: [3]
        type: floatingpoint
""")
        with self.assertRaisesRegexp(ParsingError,
                                     "but a value of 'floatingpoint'"):
            self.parser.parse(content)

    def test_length_in_non_string(self):
        content = StringIO.StringIO(
            TEMPLATE+"""
    WHATEVER:
        definition: Position of a point or node or atom
        type: integer
        length: 5
""")
        with self.assertRaisesRegexp(ParsingError, "length cannot be present"):
            self.parser.parse(content)

    def test_unrecognized_key_in_entry(self):
        content = StringIO.StringIO(
            TEMPLATE+"""
    WHATEVER:
        definition: Position of a point or node or atom
        unrecognized: XXX
        type: integer
""")
        with self.assertRaisesRegexp(ParsingError, "Unrecognized key"):
            self.parser.parse(content)


def _change_lines_starting_with(text, start, new_line_content):
    """changes the line in text starting with a given string start.
    Replaces it with new_line_content. Return the altered text."""
    return "\n".join(
        line if not line.startswith(start) else new_line_content
        for line in text.splitlines())


def _extract_lines(text, from_line, to_line):
    """Extracts the lines from the text, and return a new text"""
    return "\n".join(text.splitlines()[from_line:to_line])
