from typing import Optional

import adsk.core, adsk.fusion
from adsk import fusion

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *

def make_axis(
    axis_input: str,
    point: adsk.core.Point3D = adsk.core.Point3D.create(0, 0, 0)
):
    app = adsk.core.Application.get()
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    rootComp = design.rootComponent

    sketches = rootComp.sketches;
    xyPlane = rootComp.xYConstructionPlane
    sketch = sketches.add(xyPlane)
    if axis_input == "x":
        axis_point = adsk.core.Point3D.create(point.x + 1, point.y, point.z)
    elif axis_input == "y":
        axis_point = adsk.core.Point3D.create(point.x, point.y + 1, point.z)
    elif axis_input == "z":
        axis_point = adsk.core.Point3D.create(point.x, point.y, point.z + 1)

    sketchLine = sketch.sketchCurves.sketchLines;
    axis = sketchLine.addByTwoPoints(adsk.core.Point3D.create(point.x, point.y, point.z), axis_point)
    return axis, sketch

def make_axis_vector(axis_input: str):
    if axis_input == "x":
        axis = adsk.core.Vector3D.create(1, 0, 0)
    elif axis_input == "y":
        axis = adsk.core.Vector3D.create(0, 1, 0)
    elif axis_input == "z":
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

# not working
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





def hollow(name: str, thickness: float):
    comp = get_component(name)
    features = comp.features

    body = get_body(name)

    entities = adsk.core.ObjectCollection.create()
    for face in body.faces:
        _, normal = face.evaluator.getNormalAtPoint(face.pointOnFace)
        if normal.z > 0:
            entities.add(face)

    shellFeatures = features.shellFeatures
    shellInput = shellFeatures.createInput(entities, False)
    thicknessInput = adsk.core.ValueInput.createByReal(thickness)
    shellInput.insideThickness = thicknessInput
    shellFeatures.add(shellInput)

def hole(name: str, point, radius, depth):
    # the point should be a list of landmarks (sketch points)
    # and always use the points feature
    # or it should be called from the callee which would loop over
    # the point list
    comp = get_component(name)
    features = comp.features

    body = get_body(name)

    face_selected = None
    for face in body.faces:
        _, normal = face.evaluator.getNormalAtPoint(face.pointOnFace)
        if normal.z > 0:
            face_selected = face

    # holeDiam = adsk.core.ValueInput.createByString('20 mm')
    holeDiam = adsk.core.ValueInput.createByReal(radius)
    holeDepth = adsk.core.ValueInput.createByReal(depth)

    holeFeatures = comp.features.holeFeatures

    input = holeFeatures.createSimpleInput(holeDiam)
    input.setDistanceExtent(holeDepth)
    input.setPositionByPoint(face_selected, adsk.core.Point3D.create(point.x, point.y, point.z))
    holeFeature = holeFeatures.add(input)

def fillet_all_edges(name: str, radius: float):
    comp = get_component(name)
    features = comp.features

    body = get_body(name)

    entities = adsk.core.ObjectCollection.create()
    for edge in body.edges:
        entities.add(edge)

    offset = adsk.core.ValueInput.createByReal(radius)

    fillets = features.filletFeatures
    filletInput = fillets.createInput()
    filletInput.addConstantRadiusEdgeSet(entities, offset, True)
    fillet = fillets.add(filletInput)

def chamfer_all_edges(name: str, radius: float):
    comp = get_component(name)
    features = comp.features

    body = get_body(name)

    entities = adsk.core.ObjectCollection.create()
    for edge in body.edges:
        entities.add(edge)

    offset = adsk.core.ValueInput.createByReal(radius)

    chamfers = features.chamferFeatures
    chamferInput = chamfers.createInput2()
    chamferInput.chamferEdgeSets.addEqualDistanceChamferEdgeSet(entities, offset, True)
    chamfer = chamfers.add(chamferInput)
