import adsk.core, adsk.fusion

from codetocad import *

def make_point(
    sketch: adsk.fusion.Sketch, x: float, y: float, z: float
) -> adsk.fusion.SketchCurve:
    somePoint = adsk.core.Point3D.create(x, y, z)
    sketchPoints = sketch.sketchPoints
    _ = sketchPoints.add(somePoint)
    return sketchPoints

def make_line(
    sketch: adsk.fusion.Sketch, start: adsk.core.Point3D, end: adsk.core.Point3D
) -> adsk.fusion.SketchLines:
    sketchLines = sketch.sketchCurves.sketchLines
    sketchLines.addByTwoPoints(start, end)
    return sketchLines

def make_circle(
    sketch: adsk.fusion.Sketch,
    radius: DimensionOrItsFloatOrStringValue,
    resolution: float
) -> adsk.fusion.SketchFittedSplines:
    from .circle import get_circle_points
    radius = Dimension.from_dimension_or_its_float_or_string_value(radius)
    points = get_circle_points(radius, resolution)
    points = [adsk.core.Point3D.create(point.x.value, point.y.value, point.z.value) for point in points]

    control_points = adsk.core.ObjectCollection_create()
    for point in points:
        control_points.add(point)

    _ = sketch.sketchCurves.sketchFittedSplines.add(control_points)
    return sketch.sketchCurves.sketchFittedSplines

def make_arc(
    sketch: adsk.fusion.Sketch,
    start: adsk.core.Point3D,
    end: adsk.core.Point3D,
    radius: DimensionOrItsFloatOrStringValue,
    closed: bool = False,
) -> adsk.fusion.SketchArcs:
    along = adsk.core.Point3D.create((start.x + end.x) / 2, start.y + radius, start.z)
    arcs = sketch.sketchCurves.sketchArcs
    _ = arcs.addByThreePoints(start, along, end)

    if closed:
        lines = sketch.sketchCurves.sketchLines
        _ = lines.addByTwoPoints(start, end)

    return arcs

def make_rectangle(
    sketch: adsk.fusion.Sketch, points: list[Point]
) -> adsk.fusion.SketchLines:
    sketchLines = sketch.sketchCurves.sketchLines

    for i in range(len(points) - 1):
        start = adsk.core.Point3D.create(points[i].x.value, points[i].y.value, points[i].z.value)
        end = adsk.core.Point3D.create(points[i + 1].x.value, points[i + 1].y.value, points[i + 1].z.value)
        sketchLines.addByTwoPoints(start, end)

    return sketchLines

def make_lines(
    sketch: adsk.fusion.Sketch, points: list[Point]
) -> adsk.fusion.SketchLines:
    sketchLines = sketch.sketchCurves.sketchLines
    for i in range(len(points) - 1):
        start = points[i]
        end = points[i + 1]
        sketchLines.addByTwoPoints(start, end)

    return sketchLines
