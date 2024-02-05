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

def get_component(name: str) -> Optional[fusion.Component]:
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent

    for occurrence in rootComp.occurrences:
        if name == occurrence.component.name.split(":")[0]:
            return occurrence.component

    return None

def get_occurrence(name: str) -> Optional[fusion.Sketch]:
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent

    for occurrence in rootComp.occurrences:
        if name == occurrence.component.name.split(":")[0]:
            return occurrence

    return None

def get_sketch(name: str) -> Optional[fusion.Sketch]:
    comp = get_component(name)

    sketch = comp.sketches.itemByName(name)
    return sketch


def get_body(name: str) -> Optional[fusion.BRepBody]:
    comp = get_component(name)
    body = comp.bRepBodies.itemByName(name)
    return body

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


def mirror(name: str, other_name: str, axis: str):
    body = get_body(name)
    bodyBoundBox = body.boundingBox

    other_body = get_body(other_name)
    otherBodyBoundBox = other_body.boundingBox

    centerBody = adsk.core.Point3D.create(
        (bodyBoundBox.minPoint.x + bodyBoundBox.maxPoint.x) / 2,
        (bodyBoundBox.minPoint.y + bodyBoundBox.maxPoint.y) / 2,
        (bodyBoundBox.minPoint.z + bodyBoundBox.maxPoint.z) / 2,
    )

    centerOtherBody = adsk.core.Point3D.create(
        (otherBodyBoundBox.minPoint.x + otherBodyBoundBox.maxPoint.x) / 2,
        (otherBodyBoundBox.minPoint.y + otherBodyBoundBox.maxPoint.y) / 2,
        (otherBodyBoundBox.minPoint.z + otherBodyBoundBox.maxPoint.z) / 2,
    )

    distanceBodyToOther = adsk.core.Point3D.create(
        centerOtherBody.x - centerBody.x,
        centerOtherBody.y - centerBody.y,
        centerOtherBody.z - centerBody.z,
    )

    import math

    distance = math.sqrt(
        (centerOtherBody.x - centerBody.x) ** 2 +
        (centerOtherBody.y - centerBody.y) ** 2 +
        (centerOtherBody.z - centerBody.z) ** 2
    )

    if axis == "x":
        if distanceBodyToOther.x + distance == 0:
            move = distanceBodyToOther.x - distance
        else:
            move = distanceBodyToOther.x + distance
        newPosition = adsk.core.Point3D.create(
            move,
            distanceBodyToOther.y,
            distanceBodyToOther.z,
        )
    elif axis == "y":
        if distanceBodyToOther.y + distance == 0:
            move = distanceBodyToOther.y - distance
        else:
            move = distanceBodyToOther.y + distance
        newPosition = adsk.core.Point3D.create(
            distanceBodyToOther.x,
            move,
            distanceBodyToOther.z,
        )
    elif axis == "z":
        if distanceBodyToOther.z + distance == 0:
            move = distanceBodyToOther.z - distance
        else:
            move = distanceBodyToOther.z + distance
        newPosition = adsk.core.Point3D.create(
            distanceBodyToOther.x,
            distanceBodyToOther.y,
            move,
        )

    newName = f"{body.name} clone"
    # clone_sketch(name, newName)
    # translate_sketch(newName, newPosition.x, newPosition.y, newPosition.z)
    clone_body(body.name, newName)
    translate_body(newName, newPosition.x, newPosition.y, newPosition.z)


def mirror_old(name: str, plane: str):
    comp = get_component(name)
    features = comp.features

    body = get_body(name)
    inputEntities = adsk.core.ObjectCollection.create()
    inputEntities.add(body)

    if plane == "x":
        mirrorPlane = comp.xYConstructionPlane
    elif plane == "z":
        mirrorPlane = comp.xZConstructionPlane
    elif plane == "y":
        mirrorPlane = comp.yZConstructionPlane

    mirrorFeatures = features.mirrorFeatures
    mirrorInput = mirrorFeatures.createInput(inputEntities, mirrorPlane)

    mirrorFeatures.add(mirrorInput)

def create_circular_pattern(name: str, count: int, angle: float, center_name: str, axis: str):
    comp = get_component(name)
    features = comp.features

    # must be a point comming from callee, implement in Entity.get_boundbox()
    center = get_body(center_name)
    boundBox = center.boundingBox
    origin = adsk.core.Point3D.create(
        (boundBox.minPoint.x + boundBox.maxPoint.x) / 2,
        (boundBox.minPoint.y + boundBox.maxPoint.y) / 2,
        (boundBox.minPoint.z + boundBox.maxPoint.z) / 2,
    )

    body = get_body(name)
    inputEntites = adsk.core.ObjectCollection.create()
    inputEntites.add(body)

    axisInput, sketch = make_axis(axis, origin)

    circularFeats = features.circularPatternFeatures
    circularFeatInput = circularFeats.createInput(inputEntites, axisInput)
    circularFeatInput.quantity = adsk.core.ValueInput.createByReal(count)
    circularFeatInput.totalAngle = adsk.core.ValueInput.createByReal(angle)
    circularFeatInput.isSymmetric = False

    circularFeature = circularFeats.add(circularFeatInput)

    translate_sketch(name, origin.x, origin.y, origin.z)

    sketch.deleteMe()


def create_rectangular_pattern(name: str, count: int, offset: float, axis: str):
    comp = get_component(name)
    features = comp.features

    occ = get_occurrence(name)

    inputEntites = adsk.core.ObjectCollection.create()
    inputEntites.add(occ)

    if axis == "x":
        axisInput = comp.xConstructionAxis
    elif axis == "y":
        axisInput = comp.yConstructionAxis
    elif axis == "z":
        axisInput = comp.zConstructionAxis

    quantity = adsk.core.ValueInput.createByReal(count)
    distance = adsk.core.ValueInput.createByReal(offset)
    one = adsk.core.ValueInput.createByReal(1)

    rectangularPatterns = features.rectangularPatternFeatures
    rectangularPatternInput = rectangularPatterns.createInput(
        inputEntites, axisInput,
        quantity, distance, adsk.fusion.PatternDistanceType.SpacingPatternDistanceType)
    rectangularPatternInput.setDirectionTwo(axisInput, one, one)

    rectangularFeature = rectangularPatterns.add(rectangularPatternInput)

def create_circular_pattern_sketch(name: str, count: int, angle: float, center_name: str, axis: str):
    comp = get_component(name)
    features = comp.features

    # must be a point comming from callee, implement in Entity.get_boundbox()
    center = get_body(center_name)
    boundBox = center.boundingBox
    origin = adsk.core.Point3D.create(
        (boundBox.minPoint.x + boundBox.maxPoint.x) / 2,
        (boundBox.minPoint.y + boundBox.maxPoint.y) / 2,
        (boundBox.minPoint.z + boundBox.maxPoint.z) / 2,
    )

    occ = get_occurrence(name)

    inputEntites = adsk.core.ObjectCollection.create()
    inputEntites.add(occ)

    axisInput, sketch = make_axis(axis, origin)

    circularFeats = features.circularPatternFeatures
    circularFeatInput = circularFeats.createInput(inputEntites, axisInput)
    circularFeatInput.quantity = adsk.core.ValueInput.createByReal(count)
    circularFeatInput.totalAngle = adsk.core.ValueInput.createByReal(angle)
    circularFeatInput.isSymmetric = True

    circularFeature = circularFeats.add(circularFeatInput)

    translate_sketch(name, origin.x, origin.y, origin.z)

    sketch.deleteMe()

def create_rectangular_pattern_sketch(name: str, count: int, offset: float, axis: str):
    comp = get_component(name)
    features = comp.features

    occ = get_occurrence(name)

    inputEntites = adsk.core.ObjectCollection.create()
    inputEntites.add(occ)

    if axis == "x":
        axisInput = comp.xConstructionAxis
    elif axis == "y":
        axisInput = comp.yConstructionAxis
    elif axis == "z":
        axisInput = comp.zConstructionAxis

    quantity = adsk.core.ValueInput.createByReal(count)
    distance = adsk.core.ValueInput.createByReal(offset)
    one = adsk.core.ValueInput.createByReal(1)

    rectangularPatterns = features.rectangularPatternFeatures
    rectangularPatternInput = rectangularPatterns.createInput(
        inputEntites, axisInput,
        quantity, distance, adsk.fusion.PatternDistanceType.SpacingPatternDistanceType)
    rectangularPatternInput.setDirectionTwo(axisInput, one, one)

    rectangularFeature = rectangularPatterns.add(rectangularPatternInput)

def combine(name: str, other_name: str):
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent
    features = rootComp.features

    body = get_body(name)
    otherBody = get_body(other_name)

    bodyCollection = adsk.core.ObjectCollection.create()
    bodyCollection.add(otherBody)

    combineFeatures = features.combineFeatures
    combineFeaturesInput = combineFeatures.createInput(body, bodyCollection)
    combineFeaturesInput.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
    combineFeaturesInput.isNewComponent = False
    combineFeaturesInput.isKeepToolBodies = False
    combine_feature = combineFeatures.add(combineFeaturesInput)

def subtract(name: str, other_name: str):
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent
    features = rootComp.features

    body = get_body(name)
    otherBody = get_body(other_name)

    bodyCollection = adsk.core.ObjectCollection.create()
    bodyCollection.add(otherBody)

    combineFeatures = features.combineFeatures
    combineFeaturesInput = combineFeatures.createInput(body, bodyCollection)
    combineFeaturesInput.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
    combineFeaturesInput.isNewComponent = False
    combineFeaturesInput.isKeepToolBodies = False
    combine_feature = combineFeatures.add(combineFeaturesInput)

def intersect(name: str, other_name: str, delete_after_intersect: bool):
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent
    features = rootComp.features

    body = get_body(name)
    otherBody = get_body(other_name)

    bodyCollection = adsk.core.ObjectCollection.create()
    bodyCollection.add(otherBody)

    combineFeatures = features.combineFeatures
    combineFeaturesInput = combineFeatures.createInput(body, bodyCollection)
    combineFeaturesInput.operation = adsk.fusion.FeatureOperations.IntersectFeatureOperation
    combineFeaturesInput.isNewComponent = False
    combineFeaturesInput.isKeepToolBodies = False
    combine_feature = combineFeatures.add(combineFeaturesInput)

def sweep(name: str, profile_name: str):
    comp = get_component(name)
    path_sketch = get_sketch(name)

    paths = adsk.core.ObjectCollection.create()

    if len(path_sketch.sketchCurves.sketchLines) > 0:
        for line in path_sketch.sketchCurves.sketchLines:
            paths.add(line)

    if len(path_sketch.sketchCurves.sketchArcs) > 0:
        for line in path_sketch.sketchCurves.sketchArcs:
            paths.add(line)

    if len(path_sketch.sketchCurves.sketchConicCurves) > 0:
        for line in path_sketch.sketchCurves.sketchConicCurves:
            paths.add(line)

    if len(path_sketch.sketchCurves.sketchFittedSplines) > 0:
        for line in path_sketch.sketchCurves.sketchFittedSplines:
            paths.add(line)

    if len(path_sketch.sketchCurves.sketchFixedSplines) > 0:
        for line in path_sketch.sketchCurves.sketchFixedSplines:
            paths.add(line)

    path = comp.features.createPath(paths)

    comp_profile = get_component(profile_name)
    profile_sketch = get_sketch(profile_name)

    prof = profile_sketch.profiles.item(0)

    sweeps = comp_profile.features.sweepFeatures
    sweepInput = sweeps.createInput(
        prof, path, adsk.fusion.FeatureOperations.NewComponentFeatureOperation)
    sweep = sweeps.add(sweepInput)

    component = comp_profile.occurrences.item(
        comp_profile.occurrences.count - 1
    )
    component.name = f"Sweep {profile_name}"

def create_text(name: str, text: str, font_size: float, bold: bool, italic: bool, underlined: bool, character_spainc: int, word_spacing: int, line_spacing: int, font_file_path: Optional[str] = None):
    app = adsk.core.Application.get()
    design = app.activeProduct
    newComp = design.rootComponent.occurrences.addNewComponent(adsk.core.Matrix3D.create()).component
    newComp.name = name

    sketch = newComp.sketches.add(newComp.xYConstructionPlane)
    sketch.name = name

    texts = sketch.sketchTexts

    line = sketch.sketchCurves.sketchLines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(len(text), 0, 0))
    textInput = texts.createInput2(text, font_size)
    textInput.setAsFitOnPath(line, True)

    textStyle = 0
    if bold:
        textStyle |= adsk.fusion.TextStyles.TextStyleBold
    if italic:
        textStyle |= adsk.fusion.TextStyles.TextStyleItalic
    if underlined:
        textStyle |= adsk.fusion.TextStyles.TextStyleUnderline

    textInput.textStyle = textStyle

    sketch_text = texts.add(textInput)

def clone_sketch(name: str, new_name: str):
    app = adsk.core.Application.get()
    design = app.activeProduct

    newComp = design.rootComponent.occurrences.addNewComponent(adsk.core.Matrix3D.create()).component
    newComp.name = new_name

    sketches = newComp.sketches
    xyPlane = newComp.xYConstructionPlane

    new_sketch = sketches.add(xyPlane)
    new_sketch.name = new_name

    old_sketch = get_sketch(name)

    entities = adsk.core.ObjectCollection.create()

    if len(old_sketch.sketchCurves.sketchLines) > 0:
        for line in old_sketch.sketchCurves.sketchLines:
            entities.add(line)

    if len(old_sketch.sketchCurves.sketchArcs) > 0:
        for line in old_sketch.sketchCurves.sketchArcs:
            entities.add(line)

    if len(old_sketch.sketchCurves.sketchConicCurves) > 0:
        for line in old_sketch.sketchCurves.sketchConicCurves:
            entities.add(line)

    if len(old_sketch.sketchCurves.sketchFittedSplines) > 0:
        for line in old_sketch.sketchCurves.sketchFittedSplines:
            entities.add(line)

    if len(old_sketch.sketchCurves.sketchFixedSplines) > 0:
        for line in old_sketch.sketchCurves.sketchFixedSplines:
            entities.add(line)

    if len(old_sketch.sketchTexts) > 0:
        for line in old_sketch.sketchTexts:
            entities.add(line)

    old_sketch.copy(entities, adsk.core.Matrix3D.create(), new_sketch)

def clone_body(name: str, new_name: str):
    # check if it should clone the sketch too, because it's needed for scale
    # and if needs to create a new component or
    # create a function get_or_create_component(name)
    app = adsk.core.Application.get()
    design = app.activeProduct

    newComp = design.rootComponent.occurrences.addNewComponent(adsk.core.Matrix3D.create()).component
    newComp.name = new_name

    old_body = get_body(name)

    newComp.features.copyPasteBodies.add(old_body)

    body = newComp.bRepBodies.itemByName(name)
    body.name = new_name

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
