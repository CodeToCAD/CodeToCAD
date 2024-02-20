import adsk.core, adsk.fusion

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


def make_axis(
    axis_input: AxisOrItsIndexOrItsName,
    point: adsk.core.Point3D = adsk.core.Point3D.create(0, 0, 0),
) -> (adsk.fusion.SketchLine, adsk.fusion.Sketch):
    app = adsk.core.Application.get()
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    rootComp = design.rootComponent

    sketches = rootComp.sketches
    xyPlane = rootComp.xYConstructionPlane
    sketch = sketches.add(xyPlane)

    match Axis.from_string(axis_input).value:
        case Axis.X.value:
            axis_point = adsk.core.Point3D.create(point.x + 1, point.y, point.z)
        case Axis.Y.value:
            axis_point = adsk.core.Point3D.create(point.x, point.y + 1, point.z)
        case Axis.Z.value:
            axis_point = adsk.core.Point3D.create(point.x, point.y, point.z + 1)

    sketchLine = sketch.sketchCurves.sketchLines
    axis = sketchLine.addByTwoPoints(
        adsk.core.Point3D.create(point.x, point.y, point.z), axis_point
    )
    return axis, sketch


def make_axis_from_points(
    start: adsk.core.Point3D, end: adsk.core.Point3D
) -> (adsk.fusion.SketchLine, adsk.fusion.Sketch):
    app = adsk.core.Application.get()
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    rootComp = design.rootComponent

    sketches = rootComp.sketches
    xyPlane = rootComp.xYConstructionPlane
    sketch = sketches.add(xyPlane)

    sketchLine = sketch.sketchCurves.sketchLines
    axis = sketchLine.addByTwoPoints(start, end)
    return axis, sketch


def make_axis_vector(axis_input: AxisOrItsIndexOrItsName):
    match Axis.from_string(axis_input).value:
        case Axis.X.value:
            axis = adsk.core.Vector3D.create(1, 0, 0)
        case Axis.Y.value:
            axis = adsk.core.Vector3D.create(0, 1, 0)
        case Axis.Z.value:
            axis = adsk.core.Vector3D.create(0, 0, 1)
    return axis


def make_matrix():
    return adsk.core.Matrix3D.create()


def make_vector(x: float, y: float, z: float):
    return adsk.core.Vector3D.create(x, y, z)


def make_point3d(x: float, y: float, z: float):
    return adsk.core.Point3D.create(x, y, z)


def make_collection():
    return adsk.core.ObjectCollection.create()
