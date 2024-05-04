import json
import os
import unittest
from providers.onshape import *
from providers.onshape.onshape_provider import *
from providers.onshape.onshape_provider.onshape_actions import *

from codetocad import *

from providers.onshape.onshape_provider.utils import get_polygon_points

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

    def setUp(self) -> None:
        self.onshape_url = self.get_onshape_url()

    def get_onshape_url(self):
        documentUrl = get_first_document_url_by_name(self.client, onshape_document_name)
        assert documentUrl is not None
        return documentUrl

    def create_tab_and_set_tab_id(self):
        partStudioId = create_tab_part_studios(
            self.client, self.onshape_url, Utilities.create_uuid_like_id()
        )
        assert partStudioId is not None
        self.onshape_url.tab_id = partStudioId

    def test_read_document_url_by_name(self) -> None:
        documentUrl = self.get_onshape_url()
        print("documentUrl", documentUrl)

    def test_create_part_studio_tab(self) -> None:
        self.create_tab_and_set_tab_id()

    def test_create_point(self) -> None:
        self.create_tab_and_set_tab_id()
        pointLocation = Dimension(15.0, "mm")
        create_point(
            self.client,
            self.onshape_url,
            "Test Point",
            Point(pointLocation, pointLocation, pointLocation),
        )

    def test_create_line(self) -> None:
        self.create_tab_and_set_tab_id()
        pointLocation1 = Dimension(0.1, "inch")
        pointLocation2 = Dimension(0.3, "inch")
        create_line(
            self.client,
            self.onshape_url,
            "Test Line",
            Point(pointLocation1, pointLocation1, pointLocation1),
            Point(pointLocation2, pointLocation2, pointLocation2),
        )

    def test_create_rect(self) -> None:
        self.create_tab_and_set_tab_id()
        pointLocation1 = Dimension(0.1, "inch")
        pointLocation2 = Dimension(0.3, "inch")
        create_rect(
            self.client,
            self.onshape_url,
            "Test Point",
            Point(pointLocation1, pointLocation1, pointLocation1),
            Point(pointLocation2, pointLocation2, pointLocation2),
        )

    def test_create_circle(self):
        self.create_tab_and_set_tab_id()
        pointLocation1 = Dimension(0.1, "inch")
        pointLocation2 = Dimension(0.3, "inch")
        create_circle(
            self.client,
            self.onshape_url,
            "Test Point",
            0.05,
            Point(pointLocation1, pointLocation2, pointLocation2),
            False,
        )

    def test_create_ellipse(self):
        self.create_tab_and_set_tab_id()
        pointLocation1 = Dimension(0.0, "inch")
        pointLocation2 = Dimension(0.0, "inch")
        create_ellipse(
            self.client,
            self.onshape_url,
            "Test Ellipse",
            0.02,
            0.05,
            Point(pointLocation1, pointLocation2, pointLocation2),
            True,
        )

    def test_create_arc(self):
        self.create_tab_and_set_tab_id()
        start_point = Point(
            Dimension(0.014, "meter"), Dimension(0.009, "inch"), Dimension(0.0, "meter")
        )
        end_point = Point(
            Dimension(0.00, "meter"),
            Dimension(-0.041, "meter"),
            Dimension(0.0, "meter"),
        )
        create_arc(
            self.client,
            self.onshape_url,
            "Test Arc Sketch",
            0.035,
            start_point,
            end_point,
            False,
        )

    def test_create_trapezoid(self):
        self.create_tab_and_set_tab_id()
        create_trapezoid(
            self.client, self.onshape_url, "Test Trapezoid Sketch", 0.5, 1.0, 0.3
        )

    def test_create_polygon(self):
        self.create_tab_and_set_tab_id()
        points = get_polygon_points(10, 0.02)
        new_points: list[Point] = []
        for point in points:
            new_points.append(
                Point(
                    Dimension(point[0], "m"),
                    Dimension(point[1], "m"),
                    Dimension(0.0, "m"),
                )
            )
        create_polygon(self.client, self.onshape_url, "Test Polygon Sketch", new_points)

    def test_create_text(self):
        self.create_tab_and_set_tab_id()
        pointLocation1 = Dimension(0.1, "mm")
        pointLocation2 = Dimension(0.3, "mm")
        create_text(
            self.client,
            self.onshape_url,
            "Test Text Sketch",
            "Hello World!",
            Point(pointLocation1, pointLocation1, pointLocation1),
            Point(pointLocation2, pointLocation2, pointLocation2),
            bold=True,
            italic=True,
        )

    def test_extrude(self):
        self.create_tab_and_set_tab_id()
        pointLocation1 = Dimension(15.0, "mm")
        pointLocation2 = Dimension(25.0, "mm")
        sketch_info = create_rect(
            self.client,
            self.onshape_url,
            "Test Point",
            Point(pointLocation1, pointLocation1, pointLocation1),
            Point(pointLocation2, pointLocation2, pointLocation2),
        )
        feature_id = json.loads(sketch_info.data)["feature"]["featureId"]
        create_extrude(self.client, self.onshape_url, feature_id)

    def test_create_spiral(self):
        self.create_tab_and_set_tab_id()
        create_spiral(
            self.client,
            self.onshape_url,
            "Test Sprial Sketch",
            5,
            Dimension(1, "inch"),
            Dimension(2, "inch"),
            True,
            radius_end=Dimension(3, "inch"),
        )
