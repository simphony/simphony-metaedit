from __future__ import print_function
import logging
import sys

from simphony_metaparser.yamldirparser import YamlDirParser
from simphony_metaparser import nodes

from . import app


def _usage():
    print("Please specify the directory of the metadata info")


def main():
    try:
        directory = sys.argv[1]
    except IndexError:
        _usage()
        sys.exit(0)

    parser = YamlDirParser()

    try:
        model = parser.parse(directory)
    except Exception as e:
        logging.exception("Could not parse {} : {}".format(
            directory,
            e)
        )
        model = nodes.Ontology()
        model.root_cuds_item = nodes.CUDSItem(name="CUBA.ROOT")

    a = app.App(model=model)
    a.configure_traits()
