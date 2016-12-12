from __future__ import print_function
import sys

from . import app


def _usage():
    print("Please specify the directory of the metadata info")


def main():
    try:
        directory = sys.argv[1]
    except IndexError:
        _usage()
        sys.exit(0)

    a = app.App(directory=directory)
    a.configure_traits()
