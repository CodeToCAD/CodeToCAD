from typing import List
from codetocad.core.dimension import Dimension
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


def calculate_ellipse_quadrant_points(
    start_point: Point, end_point: Point, quadrant_resolution: int
) -> List[Point]:
    if start_point.x > end_point.x:
        temp_start_point = start_point
        start_point = end_point
        end_point = temp_start_point

    radius_x = end_point.x - start_point.x
    radius_y = end_point.y - start_point.y

    def frange(start: float, stop: float, step: float):
        value = start
        while value < stop:
            yield value
            value += step
            if value >= stop:
                return stop

    points: List[Point] = []

    for x in frange(
        start_point.x.value, end_point.x.value, radius_x.value / quadrant_resolution
    ):
        points.append(_calculate_ellipse_point(x=Dimension(x), a=radius_x, b=radius_y))

    return points


def calculate_ellipse_points(radius_x: Dimension, radius_y: Dimension, resolution: int):
    quadrant_resolution = int(resolution / 4)
    first_point = Point(radius_x * -1, Dimension.zero(), Dimension.zero())
    middle_point = Point(Dimension.zero(), radius_y, Dimension.zero())

    fourth_quadrant = calculate_ellipse_quadrant_points(
        first_point, middle_point, quadrant_resolution
    )

    first_quadrant = [
        Point(point.x * -1, point.y, point.z) for point in fourth_quadrant[::-1]
    ]

    fourth_first_quadrants = fourth_quadrant + first_quadrant

    second_third_quadrants = [
        Point(point.x, point.y * -1, point.z) for point in fourth_first_quadrants[::-1]
    ]

    return fourth_first_quadrants + second_third_quadrants
