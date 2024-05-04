import adsk.core
import adsk.fusion

from codetocad.core.dimension import Dimension
from codetocad.core.point import Point
from providers.fusion360.fusion360_provider.fusion_actions.common import make_point3d


def make_point(sketch: adsk.fusion.Sketch, x: float, y: float, z: float) -> Point:
    somePoint = adsk.core.Point3D.create(x, y, z)
    sketchPoints = sketch.sketchPoints
    _ = sketchPoints.add(somePoint)
    return Point(x, y, z)


def make_line(
    sketch: adsk.fusion.Sketch, start: adsk.core.Point3D, end: adsk.core.Point3D
) -> list[Point]:
    sketchLines = sketch.sketchCurves.sketchLines
    sketchLines.addByTwoPoints(start, end)
    points = [Point(start.x, start.y, start.z), Point(end.x, end.y, end.z)]
    return points


def make_circle(
    sketch: adsk.fusion.Sketch,
    radius: str | float | Dimension,
    resolution: float,
) -> list[Point]:
    from .circle import get_circle_points

    radius = Dimension.from_dimension_or_its_float_or_string_value(radius)
    points_ = get_circle_points(radius, resolution)
    points = [
        adsk.core.Point3D.create(point.x.value, point.y.value, point.z.value)
        for point in points_
    ]

    control_points = adsk.core.ObjectCollection_create()
    for point in points:
        control_points.add(point)

    _ = sketch.sketchCurves.sketchFittedSplines.add(control_points)
    return points_


def make_arc(
    sketch: adsk.fusion.Sketch,
    start: adsk.core.Point3D,
    end: adsk.core.Point3D,
    radius: str | float | Dimension,
    closed: bool = False,
) -> list[Point]:
    along = adsk.core.Point3D.create((start.x + end.x) / 2, start.y + radius, start.z)
    arcs = sketch.sketchCurves.sketchArcs
    arcs = arcs.addByThreePoints(start, along, end)

    points = [
        Point(start.x, start.y, start.z),
        Point(along.x, along.y, along.z),
        Point(end.x, end.y, end.z),
    ]

    if closed:
        lines = sketch.sketchCurves.sketchLines
        _ = lines.addByTwoPoints(start, end)

    return points


def make_rectangle(
    sketch: adsk.fusion.Sketch,
    length: float,
    width: float,
) -> list[Point]:
    half_length = length / 2
    half_width = width / 2

    left_top = Point(half_length * -1, half_width, 0)
    left_bottom = Point(half_length * -1, half_width * -1, 0)
    right_bottom = Point(half_length, half_width * -1, 0)
    right_top = Point(half_length, half_width, 0)

    points = [left_top, left_bottom, right_bottom, right_top, left_top]

    sketchLines = sketch.sketchCurves.sketchLines

    for i in range(len(points) - 1):
        start = make_point3d(
            points[i].x,
            points[i].y,
            points[i].z,
        )
        end = make_point3d(
            points[i + 1].x,
            points[i + 1].y,
            points[i + 1].z,
        )
        sketchLines.addByTwoPoints(start, end)

    return points[:-1]


def make_lines(sketch: adsk.fusion.Sketch, points: list[Point]) -> list[Point]:
    sketchLines = sketch.sketchCurves.sketchLines
    for i in range(len(points) - 1):
        start = points[i]
        end = points[i + 1]
        sketchLines.addByTwoPoints(start, end)

    return points
