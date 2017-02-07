import logging

from traits.api import HasStrictTraits, Instance

from simphony_metaedit.views.app_view import app_view
from simphony_metaparser.yamldirparser import YamlDirParser
from simphony_metaparser import nodes


class App(HasStrictTraits):
    """Main application class."""

    #: The main model, the root of the hierarchy.
    ontology = Instance(nodes.Ontology)

    view = app_view

    def _ontology_default(self):
        ontology = nodes.Ontology()
        ontology.root_cuds_item = nodes.CUDSItem(name="CUBA.ROOT")
        return ontology

    def __init__(self, directory):
        logging.debug("parsing directory {}".format(directory))

        parser = YamlDirParser()

        try:
            self.ontology = parser.parse(directory)
        except Exception as e:
            logging.exception("Could not parse {} : {}".format(
                directory,
                e)
            )
            self.reset_traits(['ontology'])
