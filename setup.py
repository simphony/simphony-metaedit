import os
import contextlib
import textwrap
from subprocess import check_call, CalledProcessError

from setuptools import setup, find_packages
from distutils.cmd import Command

# Read description
with open('README.rst', 'r') as readme:
    README_TEXT = readme.read()

# Setup version
VERSION = '0.1.0.dev0'


@contextlib.contextmanager
def cd(path):
    """Change directory and returns back to cwd once the operation is done."""
    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def write_version_py(filename=None):
    if filename is None:
        filename = os.path.join(
            os.path.dirname(__file__), 'simphony_metaedit', 'version.py')
    ver = """\
version = '%s'
"""
    fh = open(filename, 'wb')
    try:
        fh.write(ver % VERSION)
    finally:
        fh.close()
write_version_py()

# main setup configuration class
setup(
    name='simphony-metaedit',
    version=VERSION,
    author='SimPhoNy, EU FP7 Project (Nr. 604005) www.simphony-project.eu',
    description='Visualizer and editor for the metadata information',
    long_description=README_TEXT,
    install_requires=['traitsui', 'pyyaml'],
    packages=find_packages(),
    entry_points={
        'gui_scripts': [
            ('simphony-metaview = simphony_metaview.run:main')]},
    )
