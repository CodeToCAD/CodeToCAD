import unittest
from codetocad.core.dimension import Dimension
from codetocad.core.point import Point
from codetocad.core.shapes.circle import get_circle_points

from codetocad.core.shapes.ellipse import (
    get_ellipse_points,
    get_ellipse_points_in_fourth_quadrant,
)


class TestUtilities(unittest.TestCase):
    def test_ellipse(self):
        radius_x = Dimension(0.25)
        radius_y = Dimension(0.5)

        # First Quadrant
        quadrant_points = get_ellipse_points_in_fourth_quadrant(
            radius_x, radius_y, int(12 / 4)
        )

        start_point = Point.from_list_of_float_or_string([radius_x * -1, 0, 0])
        end_point = Point.from_list_of_float_or_string([0, radius_y, 0])
        assert len(quadrant_points) == 3, "Unexcepted quadrant length"
        assert quadrant_points[0] == start_point, "Wrong value on curve"
        assert quadrant_points[2] == end_point, "Wrong value on curve"

        ellipse_points = get_ellipse_points(
            radius_x=radius_x, radius_y=radius_y, resolution=64
        )
        assert len(ellipse_points) == 65, "Unexpected ellipse points length"
        assert (
            ellipse_points[0] == ellipse_points[-1]
        ), "First and last points are not equal"

    def test_circle(self):
        radius = Dimension(0.5)

        points = get_circle_points(radius, 64)

        assert points[0] == points[-1], "First and last points are not equal"
