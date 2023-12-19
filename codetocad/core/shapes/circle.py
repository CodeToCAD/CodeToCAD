import math
from codetocad.core.dimension import Dimension
from codetocad.core.math_utils import linspace
from codetocad.core.point import Point


def get_circle_points(radius: Dimension, resolution: int):
    """
    Returns points that make up a circle.
    NOTE: The first and last points are the same to denote a closed shape.
    """
    return [
        Point(
            x=radius * math.cos(theta),
            y=radius * math.sin(theta),
            z=Dimension.zero(radius.unit),
        )
        for theta in linspace(0.0, math.pi * 2, resolution, endpoint=False)
    ] + [
        Point(
            x=radius * math.cos(0),
            y=radius * math.sin(0),
            z=Dimension.zero(radius.unit),
        )
    ]
