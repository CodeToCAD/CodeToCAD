import json
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

# Note: you must create a "CodeToCAD-onshape_actions" document and "test_onshape_actions" tab to run tests that use it.
ONSHAPE_DOCUMENT_NAME = "CodeToCAD-onshape_actions"
ONSHAPE_TAB_NAME = "test_onshape_actions"


class TestOnshapeActions(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = get_onshape_client_with_config_file(config_filepath=configPath)

        document = get_document_by_name_or_none(cls.client, ONSHAPE_DOCUMENT_NAME)
        if document is None:
            document = create_document(cls.client, ONSHAPE_DOCUMENT_NAME)

        document_id = document["id"]

        workspace_id = get_workspaces(cls.client, document_id)[0]["id"]

        if (
            get_tab_by_name_or_none(
                cls.client, document_id, workspace_id, ONSHAPE_TAB_NAME
            )
            is None
        ):
            create_tab_part_studios(
                cls.client, document_id, workspace_id, ONSHAPE_TAB_NAME
            )

        cls.onshape_url = get_tab_url_by_name(
            cls.client, ONSHAPE_DOCUMENT_NAME, ONSHAPE_TAB_NAME
        )

    def test_create_point(self) -> None:
        # Define the location of the point in 3D space
        pointLocation = Dimension(15.0, "mm")

        sketch_name = "a point"

        # Create a point in the part studio
        sketch_info = create_point(
            self.client,
            self.onshape_url,
            sketch_name,
            Point(pointLocation, pointLocation, pointLocation),
        )

        assert sketch_info.status == 200

        data = json.loads(sketch_info.data)

        assert (
            data["name"] == sketch_name
        ), f"Unexpected sketch name: {data['name']}. Expected {sketch_name}"

    def test_create_rect(self) -> None:
        # Define the location of the point in 3D space
        pointLocation1 = Dimension(0.1, "inch")
        pointLocation2 = Dimension(0.3, "inch")

        sketch_name = "a rectangle"

        sketch_info = create_rect(
            self.client,
            self.onshape_url,
            sketch_name,
            Point(pointLocation1, pointLocation1, pointLocation1),
            Point(pointLocation2, pointLocation2, pointLocation2),
        )

        assert sketch_info.status == 200

        data = json.loads(sketch_info.data)

        assert (
            data["name"] == sketch_name
        ), f"Unexpected sketch name: {data['name']}. Expected {sketch_name}"

    def test_create_circle(self):
        # Define the location of the point in 3D space
        pointLocation1 = Dimension(0.1, "inch")
        pointLocation2 = Dimension(0.3, "inch")

        sketch_name = "a circle"

        sketch_info = create_circle(
            self.client,
            self.onshape_url,
            sketch_name,
            0.05,
            Point(pointLocation1, pointLocation2, pointLocation2),
        )

        assert sketch_info.status == 200

        data = json.loads(sketch_info.data)
        feature_name = data["feature"]["name"]
        assert (
            feature_name == sketch_name
        ), f"Unexpected sketch name: {feature_name}. Expected {sketch_name}"

    def test_update_sketch(self):
        # Define the location of the point in 3D space
        pointLocation1 = Dimension(0.1, "inch")
        pointLocation2 = Dimension(0.3, "inch")

        sketch_name = "a circle and a rect"

        sketch_info = create_circle(
            self.client,
            self.onshape_url,
            sketch_name,
            0.05,
            Point(pointLocation1, pointLocation2, pointLocation2),
        )
        # sketch_info = create_rect(
        #     self.client,
        #     self.onshape_url,
        #     sketch_name,
        #     Point(pointLocation1, pointLocation1, pointLocation1),
        #     Point(pointLocation2, pointLocation2, pointLocation2),
        # )

        assert sketch_info.status == 200

        data = json.loads(sketch_info.data)
        feature_name = data["feature"]["name"]
        assert (
            feature_name == sketch_name
        ), f"Unexpected sketch name: {feature_name}. Expected {sketch_name}"

        sketch_info = create_rect(
            self.client,
            self.onshape_url,
            sketch_name,
            Point(pointLocation1, pointLocation1, pointLocation1),
            Point(pointLocation2, pointLocation2, pointLocation2),
        )

        assert sketch_info.status == 200

        data = json.loads(sketch_info.data)
        feature_name = data["feature"]["name"]
        assert (
            feature_name == sketch_name
        ), f"Unexpected sketch name: {feature_name}. Expected {sketch_name}"

    def test_extrude(self):
        # Define the location of the point in 3D space
        pointLocation1 = Dimension(15.0, "mm")
        pointLocation2 = Dimension(25.0, "mm")

        extrude_amount = Dimension.from_string("2in")

        # Create a point in the part studio
        sketch_info = create_rect(
            self.client,
            self.onshape_url,
            "Cube Sketch",
            Point(pointLocation1, pointLocation1, pointLocation1),
            Point(pointLocation2, pointLocation2, pointLocation2),
        )

        feature_id = json.loads(sketch_info.data)["feature"]["featureId"]

        create_extrude(self.client, self.onshape_url, feature_id, f"{extrude_amount}")
