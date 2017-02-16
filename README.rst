Simphony-metaedit
=================

A GUI visualizer for the SimPhoNy metadata files available at https://github.com/simphony/simphony-metadata
Currently, it is only a visualizer. All data is available as readonly. Edit functionality will be added at a
later stage.

 
Installation
------------

To install simphony-metaedit, you need a working EDM deployment. You can download EDM from::

    https://www.enthought.com/products/edm/installers/

Once EDM is deployed on your machine, create and activate an appropriate virtual environment::

    edm environments create simphony-metaedit -r edm_requirements.txt
    edm shell --environment=simphony-metaedit

proceed to install dependencies with pip::

    pip install -r requirements.txt

and finally metaedit itself::

    python setup.py install

You can now start the application with::

    $ simphony-metaedit path_to/metadata_yaml_directory

Usage
-----

Simphony-metaedit presents two tab panes: the "CUDS Items" pane, and the "CUBA data types" pane.

The ``CUDS Items`` pane displays the CUDS Items. The parent hierarchy is represented as a tree on the
left hand side. Clicking on individual items will reveal more information about the specific item, 
together with the carried properties, either fixed or variable. Inherited properties, coming from 
the parent hierarchy, are also displayed in a light blue color.

The ``CUBA data type`` pane display the CUBA data types. Once again, they are presented on the left
hand side, as a list. Each individual data type information can be seen on the right by selecting 
the desired type.


Directory structure
-------------------

There are four subpackages:

- simphony_metaedit -- main package content
- doc -- Documentation related files
  - source -- Sphinx rst source files
  - build -- Documentation build directory, if documentation has been generated
    using the ``make`` script in the ``doc`` directory.

