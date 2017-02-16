Simphony-metaedit
=================

A GUI visualizer for the SimPhoNy metadata files available at https://github.com/simphony/simphony-metadata

Installation
------------

To install simphony-metaedit, you need a working EDM deployment. You can download EDM from::

    https://www.enthought.com/products/edm/installers/

Once EDM is deployed on your machine, create and activate an appropriate virtual environment::

    edm environments create simphony-metaedit
    edm shell --environment=simphony-metaedit


 


Directory structure
-------------------

There are four subpackages:

- simphony_metaedit -- main package content
- doc -- Documentation related files

  - source -- Sphinx rst source files
  - build -- Documentation build directory, if documentation has been generated
    using the ``make`` script in the ``doc`` directory.

