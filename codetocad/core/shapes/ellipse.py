from typing import List
from codetocad.core.dimension import Dimension
from codetocad.core.math_utils import linspace
from codetocad.core.point import Point


def _calculate_ellipse_point(x: Dimension, a: Dimension, b: Dimension) -> Point:
    """
    Using the equation x^2/a^2 + y^2/b^2 = 1, we will calculate a point on an elliptical path.
    """
    a_squared = a.raise_power(2)
    b_squared = b.raise_power(2)
    x_squared = x.raise_power(2)

    # y^2/b^2 = 1 - x^2/a^2
    y_squared_div_b_squared = Dimension(1, x.unit) - (x_squared / a_squared)
    y_squared = y_squared_div_b_squared * b_squared
    return Point(x=x, y=y_squared.raise_power(1 / 2), z=Dimension.zero())


def get_ellipse_points_in_fourth_quadrant(
    radius_x: Dimension, radius_y: Dimension, quadrant_resolution: int
) -> List[Point]:
    """
    Returns linspaced points making up an ellipse's fourth quadrant.
    """

    points: List[Point] = []

    first_point = Point(radius_x * -1, Dimension.zero(), Dimension.zero())
    middle_point = Point(Dimension.zero(), radius_y, Dimension.zero())

    for x in linspace(first_point.x.value, middle_point.x.value, quadrant_resolution):
        points.append(_calculate_ellipse_point(x=Dimension(x), a=radius_x, b=radius_y))

    return points


def get_ellipse_points(radius_x: Dimension, radius_y: Dimension, resolution: int):
    """
    Returns linspaced points making up a complete ellipse.
    NOTE: The first and last points are the same to denote a closed shape.
    """
    quadrant_resolution = int(resolution / 4) + 1

    fourth_quadrant = get_ellipse_points_in_fourth_quadrant(
        radius_x, radius_y, quadrant_resolution
    )

    first_quadrant = [
        Point(point.x * -1, point.y, point.z) for point in fourth_quadrant[-2::-1]
    ]

    fourth_first_quadrants = fourth_quadrant + first_quadrant

    second_third_quadrants = [
        Point(point.x, point.y * -1, point.z)
        for point in fourth_first_quadrants[-2::-1]
    ]

    return fourth_first_quadrants + second_third_quadrants
