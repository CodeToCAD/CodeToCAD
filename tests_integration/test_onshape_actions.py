import os
import unittest
from providers.onshape import *
from providers.onshape.onshape_provider import *
from providers.onshape.onshape_provider.onshape_actions import *

from codetocad import *
from codetocad.utilities import Point

configPath = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "../providers/onshape/.onshape_client_config.yaml",
)

# Note: you must create a "CodeToCAD-onshape_actions" document to run tests that use it.
onshape_document_name = "CodeToCAD-onshape_actions"


class TestOnshapeActions(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = get_onshape_client_with_config_file(config_filepath=configPath)

        # from onshape_provider import injectonshape_provider
        # injectonshape_provider(globals())

    def setUp(self) -> None:
        pass

    def test_read_document_url_by_name(self) -> None:
        documentUrl = get_first_document_url_by_name(self.client, onshape_document_name)

        assert documentUrl is not None

        print("documentUrl", documentUrl)

    def test_create_part_studio_tab(self) -> None:
        documentUrl = get_first_document_url_by_name(self.client, onshape_document_name)

        partStudioId = create_tab_part_studios(
            self.client, documentUrl, Utilities.create_uuid_like_id()
        )

        assert partStudioId is not None

    def test_create_point(self) -> None:
        onshapeUrl = get_first_document_url_by_name(self.client, onshape_document_name)

        partStudioId = create_tab_part_studios(
            self.client, onshapeUrl, Utilities.create_uuid_like_id()
        )

        onshapeUrl.tab_id = partStudioId

        pointLocation = Dimension(1.5, "m")

        create_point(
            self.client,
            onshapeUrl,
            "Test Point",
            Point(pointLocation, pointLocation, pointLocation),
        )
