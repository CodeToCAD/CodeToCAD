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
