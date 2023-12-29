import math
from codetocad.core.dimension import Dimension
from codetocad.core.math_utils import linspace
from codetocad.core.point import Point


def get_point_on_circle_at_angle(theta_radians: float, radius: Dimension):
    return Point(
        x=radius * math.cos(theta_radians),
        y=radius * math.sin(theta_radians),
        z=Dimension.zero(radius.unit),
    )


def get_circle_points(radius: Dimension, resolution: int):
    """
    Returns points that make up a circle.
    NOTE: The first and last points are the same to denote a closed shape.
    """
    return [
        get_point_on_circle_at_angle(theta, radius)
        for theta in linspace(0.0, math.pi * 2, resolution, endpoint=False)
    ] + [get_point_on_circle_at_angle(0.0, radius)]


def get_center_of_circle(point1: Point, point2: Point, radius: Dimension):
    # references https://rosettacode.org/wiki/Circles_of_given_radius_through_two_points#Python
    (x1, y1), (x2, y2) = (point1.x, point1.y), (point2.x, point2.y)

    dx, dy = x2 - x1, y2 - y1

    cord_length = (dx.raise_power(2) + dy.raise_power(2)).raise_power(1 / 2)

    # halfway point
    x3, y3 = (x1 + x2) / 2, (y1 + y2) / 2

    mirror_line_distance = (
        radius.raise_power(2) - (cord_length / 2).raise_power(2)
    ).raise_power(1 / 2)

    # # The other answer
    # c2 = Cir(x=x3 + d*dy/q,
    #          y=y3 - d*dx/q,
    #          r=abs(r))

    return Point(
        x=x3 - mirror_line_distance * dy / cord_length,
        y=y3 + mirror_line_distance * dx / cord_length,
        z=Dimension.zero(),
    )
