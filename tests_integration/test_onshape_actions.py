import os
import unittest
from providers.onshape import *
from providers.onshape.onshape_provider import *
from providers.onshape.onshape_provider.onshape_actions import *

from codetocad import *
from codetocad.core import Point, Dimension

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
        # Replace 'CodeToCAD-onshape_actions' with the actual document name
        onshape_document_name = "CodeToCAD-onshape_actions"

        # Get the URL of the Onshape document
        onshape_url = get_first_document_url_by_name(self.client, onshape_document_name)

        # Create a new tab in the part studio
        part_studio_id = create_tab_part_studios(
            self.client, onshape_url, Utilities.create_uuid_like_id()
        )

        # Set the tab_id for subsequent operations
        onshape_url.tab_id = part_studio_id

        # Define the location of the point in 3D space
        pointLocation = Dimension(15.0, "mm")

        # Create a point in the part studio
        create_point(
            self.client,
            onshape_url,
            "Test Point",
            Point(pointLocation, pointLocation, pointLocation),
        )

    def test_create_rect(self) -> None:
        # Get the URL of the Onshape document
        onshape_url = get_first_document_url_by_name(self.client, onshape_document_name)

        # Create a new tab in the part studio
        part_studio_id = create_tab_part_studios(
            self.client, onshape_url, Utilities.create_uuid_like_id()
        )

        # Set the tab_id for subsequent operations
        onshape_url.tab_id = part_studio_id

        # Define the location of the point in 3D space
        pointLocation1 = Dimension(15.0, "mm")
        pointLocation2 = Dimension(25.0, "mm")

        # Create a point in the part studio
        create_rect(
            self.client,
            onshape_url,
            "Test Point",
            Point(pointLocation1, pointLocation1, pointLocation1),
            Point(pointLocation2, pointLocation2, pointLocation2),
        )

    def test_extrude(self):
        onshape_document_name = "CodeToCAD-onshape_actions"

        # Get the URL of the Onshape document
        onshape_url = get_first_document_url_by_name(self.client, onshape_document_name)

        # Create a new tab in the part studio
        part_studio_id = create_tab_part_studios(
            self.client, onshape_url, Utilities.create_uuid_like_id()
        )

        # Set the tab_id for subsequent operations
        onshape_url.tab_id = part_studio_id

        # Define the location of the point in 3D space
        pointLocation1 = Dimension(15.0, "mm")
        pointLocation2 = Dimension(25.0, "mm")

        # Create a point in the part studio
        sketch_info = create_rect(
            self.client,
            onshape_url,
            "Test Point",
            Point(pointLocation1, pointLocation1, pointLocation1),
            Point(pointLocation2, pointLocation2, pointLocation2),
        )

        feature_id = json.loads(sketch_info.data)["feature"]["featureId"]
        create_extrude(self.client, onshape_url, feature_id)
