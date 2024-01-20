from typing import Optional

import adsk.core, adsk.fusion
from adsk import fusion

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


def get_sketch(name: str) -> Optional[fusion.Sketch]:
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent

    sketch = rootComp.sketches.itemByName(name)
    return sketch

def translate_sketch(name: str, x, y, z):
    sketch = get_sketch(name)
    # @check: That's sounds better but it's not working
    # entities = adsk.core.ObjectCollection.create()
    # entities.add(sketch)
    # transform = adsk.core.Matrix3D.create()
    # transform.translation = adsk.core.Vector3D.create(x, y, z)
    # sketch.move(entities, transform)

    for point in sketch.sketchPoints:
        transform = adsk.core.Vector3D.create(x, y, z)
        point.move(transform)

def rotate_sketch(name: str, x: float, y: float, z: float, angle: float):
    import math
    sketch = get_sketch(name)

    entities = adsk.core.ObjectCollection.create()
    entities.add(sketch)

    axis = adsk.core.Vector3D.create(x, y, z)
    angle = math.radians(angle)

    # not working
    origin = sketch.origin
    transform = adsk.core.Matrix3D.create()
    transform.setToRotation(angle, axis, origin)
    # sketch.transform.transformBy(transform)
    transform.transformBy(sketch.transform)

    sketch.move(entities, transform)


def scale_sketch(name: str, x: float, y: float, z: float):
    sketch = get_sketch(name)

    for point in sketch.sketchPoints:
        xFactor = abs(point.geometry.x) / (abs(point.geometry.x) + x) if x > 0 else 0
        yFactor = abs(point.geometry.y) / (abs(point.geometry.y) + y) if y > 0 else 0
        zFactor = abs(point.geometry.z) / (abs(point.geometry.z) + z) if z > 0 else 0
        transform = adsk.core.Vector3D.create(
            point.geometry.x * xFactor, point.geometry.y * yFactor, point.geometry.z * zFactor)
        point.move(transform)


def scale_by_factor_sketch(name: str, x: float, y: float, z: float):
    sketch = get_sketch(name)

    for point in sketch.sketchPoints:
        transform = adsk.core.Vector3D.create(
            point.geometry.x * x, point.geometry.y * y, point.geometry.z * z)
        point.move(transform)

def scale_sketch_uniform(name: str, scale: float):
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent

    sketch = get_sketch(name)

    inputColl = adsk.core.ObjectCollection.create()
    inputColl.add(sketch)

    scaleFactor = adsk.core.ValueInput.createByReal(scale)
    basePt = sketch.sketchPoints.item(0)

    scales = rootComp.features.scaleFeatures
    scaleInput = scales.createInput(inputColl, basePt, scaleFactor)

    scale = scales.add(scaleInput)


def get_body(name: str) -> Optional[fusion.BRepBody]:
    app = adsk.core.Application.get()

    design = app.activeProduct
    rootComp = design.rootComponent

    body = rootComp.bRepBodies.itemByName(name)
    return body

def translate_body(name: str, vector: adsk.core.Vector3D):
    app = adsk.core.Application.get()

    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)

    rootComp = design.rootComponent
    features = rootComp.features

    body = get_body(name)

    bodies = adsk.core.ObjectCollection.create()
    bodies.add(body)

    transform = adsk.core.Matrix3D.create()
    transform.translation = vector

    moveFeats = features.moveFeatures
    moveFeatureInput = moveFeats.createInput2(bodies)
    moveFeatureInput.defineAsFreeMove(transform)
    moveFeats.add(moveFeatureInput)

def rotate_body(name: str, axis_point: adsk.core.Point3D, angle: float):
    import math
    app = adsk.core.Application.get()
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    rootComp = design.rootComponent
    features = rootComp.features

    body = get_body(name)

    bodies = adsk.core.ObjectCollection.create()
    bodies.add(body)

    sketches = rootComp.sketches;
    xyPlane = rootComp.xYConstructionPlane
    sketch = sketches.add(xyPlane)

    sketchLine = sketch.sketchCurves.sketchLines;
    axis = sketchLine.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), axis_point)

    angle = adsk.core.ValueInput.createByReal(math.radians(angle))

    moveFeats = features.moveFeatures
    moveFeatureInput = moveFeats.createInput2(bodies)
    moveFeatureInput.defineAsRotate(axis, angle)
    moveFeats.add(moveFeatureInput)



def scale_body(name: str, x: float, y: float, z: float):
    body = get_body(name)

    # @check both not working

    # for point in body.edges:
    #     xFactor = abs(point.geometry.x) / (abs(point.geometry.x) + x) if x > 0 else 0
    #     yFactor = abs(point.geometry.y) / (abs(point.geometry.y) + y) if y > 0 else 0
    #     zFactor = abs(point.geometry.z) / (abs(point.geometry.z) + z) if z > 0 else 0
    #     transform = adsk.core.Vector3D.create(
    #         point.geometry.x * xFactor, point.geometry.y * yFactor, point.geometry.z * zFactor)
    #     point.geometry.set(point.geometry.x + transform.x, point.geometry.y + transform.y, point.geometry.z + transform.z)

    # for point in body.edges:
    #     if type(point) == adsk.fusion.BRepEdge.classType():
    #         transform = adsk.core.Point3D.create(
    #                 point.geometry.x + 10, point.geometry.y + 0, point.geometry.z + 5)
    #         # point.geometry = transform
    #         point.geometry.set(transform.x, transform.y, transform.z)


def scale_by_factor_body(name: str, x: float, y: float, z: float):
    body = get_body(name)
    sketch = get_sketch(name)

    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent

    inputColl = adsk.core.ObjectCollection.create()
    inputColl.add(body)

    basePt = sketch.sketchPoints.item(0)
    scaleFactor = adsk.core.ValueInput.createByReal(1)

    scales = rootComp.features.scaleFeatures
    scaleInput = scales.createInput(inputColl, basePt, scaleFactor)

    # Set the scale to be non-uniform
    xScale = adsk.core.ValueInput.createByReal(x)
    yScale = adsk.core.ValueInput.createByReal(y)
    zScale = adsk.core.ValueInput.createByReal(z)
    scaleInput.setToNonUniform(xScale, yScale, zScale)

    scale = scales.add(scaleInput)

def scale_body_uniform(name: str, scale: float):
    body = get_body(name)
    sketch = get_sketch(name)

    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent

    inputColl = adsk.core.ObjectCollection.create()
    inputColl.add(body)

    basePt = sketch.sketchPoints.item(0)
    scaleFactor = adsk.core.ValueInput.createByReal(scale)

    scales = rootComp.features.scaleFeatures
    scaleInput = scales.createInput(inputColl, basePt, scaleFactor)

    scale = scales.add(scaleInput)

def set_material(name: str, material_name):
    body = get_body(name)

    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent

    if rootComp.customGraphicsGroups.count > 0:
        rootComp.customGraphicsGroups.item(0).deleteMe()
        app.activeViewport.refresh()

    graphics = rootComp.customGraphicsGroups.add()
    bodyMesh = body.meshManager.createMeshCalculator()
    bodyMesh = body.meshManager.displayMeshes.bestMesh

    if isinstance(material_name, str):
        material_name = getattr(PresetMaterial, material_name)

    if isinstance(material_name, PresetMaterial):
        r, g, b, a = material_name.color
        color = adsk.core.Color.create(r, g, b, round(a * 255))
        # body.material.appearence = adsk.fusion.CustomGraphicsBasicMaterialColorEffect.create(color)
        # body.material.appearence = color
        # solidColor = adsk.fusion.CustomGraphicsSolidColorEffect.create(color)
        coords = adsk.fusion.CustomGraphicsCoordinates.create(bodyMesh.nodeCoordinatesAsDouble)
        mesh = graphics.addMesh(coords, bodyMesh.nodeIndices,
                                bodyMesh.normalVectorsAsDouble, bodyMesh.nodeIndices)

        # mesh.color = solidColor
        mesh.color = adsk.fusion.CustomGraphicsBasicMaterialColorEffect.create(color)

