import os

from setuptools import setup, find_packages

# Setup version
VERSION = '0.1.0.dev0'


# Read description
with open('README.rst', 'r') as readme:
    README_TEXT = readme.read()


def write_version_py():
    filename = os.path.join(
        os.path.dirname(__file__),
        'simphony_metaedit',
        'version.py')
    ver = "__version__ = '{}'"
    with open(filename, 'w') as fh:
        fh.write(ver.format(VERSION))

write_version_py()

# main setup configuration class
setup(
    name='simphony-metaedit',
    version=VERSION,
    author='SimPhoNy, EU FP7 Project (Nr. 604005) www.simphony-project.eu',
    description='Visualizer and editor for the metadata information',
    long_description=README_TEXT,
    install_requires=[
        'traitsui~=5.1',
        'pyyaml~=3.12'],
    packages=find_packages(),
    entry_points={
        'gui_scripts': [
            ('simphony-metaview = simphony_metaview.run:main')
        ]
    },
)
