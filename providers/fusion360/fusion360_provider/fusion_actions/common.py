from typing import Optional

import adsk.core, adsk.fusion
from adsk import fusion

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *

def make_axis(axis_input: str):
    app = adsk.core.Application.get()
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    rootComp = design.rootComponent

    sketches = rootComp.sketches;
    xyPlane = rootComp.xYConstructionPlane
    sketch = sketches.add(xyPlane)

    if axis_input == "x":
        axis_point = adsk.core.Point3D.create(1, 0, 0)
    elif axis_input == "y":
        axis_point = adsk.core.Point3D.create(0, 1, 0)
    elif axis_input == "z":
        axis_point = adsk.core.Point3D.create(0, 0, 1)

    sketchLine = sketch.sketchCurves.sketchLines;
    axis = sketchLine.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), axis_point)
    return axis, sketch

def make_axis_vector(axis_input: str):
    if axis_input == "x":
        axis = adsk.core.Vector3D.create(1, 0, 0)
    elif axis_input == "y":
        axis = adsk.core.Vector3D.create(0, 1, 0)
    elif axis_input == "z":
        axis = adsk.core.Vector3D.create(0, 0, 1)
    return axis

def get_component(name: str) -> Optional[fusion.Sketch]:
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent

    for occurrence in rootComp.occurrences:
        if name == occurrence.component.name.split(":")[0]:
            return occurrence

    return None

def get_sketch(name: str) -> Optional[fusion.Sketch]:
    comp = get_component(name).component

    sketch = comp.sketches.itemByName(name)
    return sketch

def translate_sketch(name: str, x, y, z):
    sketch = get_sketch(name)

    for point in sketch.sketchPoints:
        transform = adsk.core.Vector3D.create(x, y, z)
        point.move(transform)

def rotate_sketch(name: str, axis_input: str, angle: float):
    import math
    sketch = get_sketch(name)

    entities = adsk.core.ObjectCollection.create()

    if len(sketch.sketchCurves.sketchLines) > 0:
        entities.add(sketch.sketchCurves.sketchLines[0])

    if len(sketch.sketchCurves.sketchArcs) > 0:
        entities.add(sketch.sketchCurves.sketchArcs[0])

    if len(sketch.sketchCurves.sketchConicCurves) > 0:
        entities.add(sketch.sketchCurves.sketchConicCurves[0])

    if len(sketch.sketchCurves.sketchFittedSplines) > 0:
        entities.add(sketch.sketchCurves.sketchFittedSplines[0])

    if len(sketch.sketchCurves.sketchFixedSplines) > 0:
        entities.add(sketch.sketchCurves.sketchFixedSplines[0])

    if len(sketch.sketchTexts) > 0:
        entities.add(sketch.sketchTexts[0])

    axis = make_axis_vector(axis_input)
    angle = math.radians(angle)

    origin = sketch.origin
    transform = adsk.core.Matrix3D.create()
    transform.setToRotation(angle, axis, origin)

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
    comp = get_component(name).component
    body = comp.bRepBodies.itemByName(name)
    return body

def translate_body(name: str, x: float, y: float, z: float):
    comp = get_component(name).component
    features = comp.features

    body = get_body(name)

    bodies = adsk.core.ObjectCollection.create()
    bodies.add(body)

    transform = adsk.core.Matrix3D.create()
    transform.translation = adsk.core.Vector3D.create(x, y, z)

    moveFeats = features.moveFeatures
    moveFeatureInput = moveFeats.createInput2(bodies)
    moveFeatureInput.defineAsFreeMove(transform)
    moveFeats.add(moveFeatureInput)

def rotate_body(name: str, axis_input: str, angle: float):
    import math
    app = adsk.core.Application.get()
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    rootComp = design.rootComponent
    features = rootComp.features

    body = get_body(name)

    bodies = adsk.core.ObjectCollection.create()
    bodies.add(body)

    axis, sketch = make_axis(axis_input)

    angle = adsk.core.ValueInput.createByReal(math.radians(angle))

    moveFeats = features.moveFeatures
    moveFeatureInput = moveFeats.createInput2(bodies)
    moveFeatureInput.defineAsRotate(axis, angle)
    moveFeats.add(moveFeatureInput)

def scale_body(name: str, x: float, y: float, z: float):
    comp = get_component(name).component
    body = get_body(name)

    xFactor = 1
    yFactor = 1
    zFactor = 1

    for point in body.vertices:
        if xFactor == 1 and point.geometry.x > 0 and x > 0:
            xFactor = (abs(point.geometry.x) + x) / abs(point.geometry.x)
        if yFactor == 1 and point.geometry.y > 0 and y > 0:
            yFactor = (abs(point.geometry.y) + y) / abs(point.geometry.y)
        if zFactor == 1 and point.geometry.z > 0 and z > 0:
            zFactor = (abs(point.geometry.z) + z) / abs(point.geometry.z)

    sketch = get_sketch(name)

    inputColl = adsk.core.ObjectCollection.create()
    inputColl.add(body)

    basePt = sketch.sketchPoints.item(0)
    scaleFactor = adsk.core.ValueInput.createByReal(1)

    scales = comp.features.scaleFeatures
    scaleInput = scales.createInput(inputColl, basePt, scaleFactor)

    xScale = adsk.core.ValueInput.createByReal(xFactor)
    yScale = adsk.core.ValueInput.createByReal(yFactor)
    zScale = adsk.core.ValueInput.createByReal(zFactor)
    scaleInput.setToNonUniform(xScale, yScale, zScale)

    scale = scales.add(scaleInput)

def scale_by_factor_body(name: str, x: float, y: float, z: float):
    comp = get_component(name).component

    body = get_body(name)
    sketch = get_sketch(name)

    inputColl = adsk.core.ObjectCollection.create()
    inputColl.add(body)

    basePt = sketch.sketchPoints.item(0)
    scaleFactor = adsk.core.ValueInput.createByReal(1)

    scales = comp.features.scaleFeatures
    scaleInput = scales.createInput(inputColl, basePt, scaleFactor)

    xScale = adsk.core.ValueInput.createByReal(x)
    yScale = adsk.core.ValueInput.createByReal(y)
    zScale = adsk.core.ValueInput.createByReal(z)
    scaleInput.setToNonUniform(xScale, yScale, zScale)

    scale = scales.add(scaleInput)

def scale_body_uniform(name: str, scale: float):
    comp = get_component(name).component

    body = get_body(name)
    sketch = get_sketch(name)

    inputColl = adsk.core.ObjectCollection.create()
    inputColl.add(body)

    basePt = sketch.sketchPoints.item(0)
    scaleFactor = adsk.core.ValueInput.createByReal(scale)

    scales = comp.features.scaleFeatures
    scaleInput = scales.createInput(inputColl, basePt, scaleFactor)

    scale = scales.add(scaleInput)

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

def mirror(name: str, plane: str):
    comp = get_component(name).component
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
    comp = get_component(name).component
    features = comp.features

    body = get_body(name)
    inputEntites = adsk.core.ObjectCollection.create()
    inputEntites.add(body)

    if axis == "x":
        axisInput = comp.xConstructionAxis
    elif axis == "y":
        axisInput = comp.yConstructionAxis
    elif axis == "z":
        axisInput = comp.zConstructionAxis

    circularFeats = features.circularPatternFeatures
    circularFeatInput = circularFeats.createInput(inputEntites, axisInput)
    circularFeatInput.quantity = adsk.core.ValueInput.createByReal(count)
    circularFeatInput.totalAngle = adsk.core.ValueInput.createByReal(angle)
    circularFeatInput.isSymmetric = False

    circularFeature = circularFeats.add(circularFeatInput)

# same as sketch pattern
def create_rectangular_pattern(name: str, count: int, offset: float, axis: str):
    comp = get_component(name).component
    features = comp.features

    inputEntites = adsk.core.ObjectCollection.create()
    occ = get_component(name)
    inputEntites.add(occ)

    if axis == "x":
        axisInput = comp.xConstructionAxis
    elif axis == "y":
        axisInput = comp.yConstructionAxis
    elif axis == "z":
        axisInput = comp.zConstructionAxis

    quantity = adsk.core.ValueInput.createByReal(count)
    distance = adsk.core.ValueInput.createByReal(offset)

    rectangularPatterns = features.rectangularPatternFeatures
    rectangularPatternInput = rectangularPatterns.createInput(
        inputEntites, axisInput,
        quantity, distance, adsk.fusion.PatternDistanceType.SpacingPatternDistanceType)

    rectangularFeature = rectangularPatterns.add(rectangularPatternInput)

def create_circular_pattern_sketch(name: str, count: int, angle: float, center_name: str, axis: str):
    comp = get_component(name).component
    features = comp.features

    occ = get_component(name)

    sketch = get_sketch(name)
    inputEntites = adsk.core.ObjectCollection.create()
    inputEntites.add(occ)

    if axis == "x":
        axisInput = comp.xConstructionAxis
    elif axis == "y":
        axisInput = comp.yConstructionAxis
    elif axis == "z":
        axisInput = comp.zConstructionAxis

    circularFeats = features.circularPatternFeatures
    circularFeatInput = circularFeats.createInput(inputEntites, axisInput)
    circularFeatInput.quantity = adsk.core.ValueInput.createByReal(count)
    circularFeatInput.totalAngle = adsk.core.ValueInput.createByReal(angle)
    circularFeatInput.isSymmetric = True

    circularFeature = circularFeats.add(circularFeatInput)

# creating more than expected (the positions are correct)
def create_retangular_pattern_sketch(name: str, count: int, offset: float, axis: str):
    comp = get_component(name).component
    features = comp.features

    occ = get_component(name)

    sketch = get_sketch(name)
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

    rectangularPatterns = features.rectangularPatternFeatures
    rectangularPatternInput = rectangularPatterns.createInput(
        inputEntites, axisInput,
        quantity, distance, adsk.fusion.PatternDistanceType.SpacingPatternDistanceType)

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
    comp = get_component(name).component
    path_sketch = get_sketch(name)

    paths = adsk.core.ObjectCollection.create()

    if len(path_sketch.sketchCurves.sketchLines) > 0:
        paths.add(path_sketch.sketchCurves.sketchLines[0])

    if len(path_sketch.sketchCurves.sketchArcs) > 0:
        paths.add(path_sketch.sketchCurves.sketchArcs[0])

    if len(path_sketch.sketchCurves.sketchConicCurves) > 0:
        paths.add(path_sketch.sketchCurves.sketchConicCurves[0])

    if len(path_sketch.sketchCurves.sketchFittedSplines) > 0:
        paths.add(path_sketch.sketchCurves.sketchFittedSplines[0])

    if len(path_sketch.sketchCurves.sketchFixedSplines) > 0:
        paths.add(path_sketch.sketchCurves.sketchFixedSplines[0])

    path = comp.features.createPath(paths)

    comp_profile = get_component(profile_name).component
    profile_sketch = get_sketch(profile_name)

    prof = profile_sketch.profiles.item(0)

    sweeps = comp_profile.features.sweepFeatures
    sweepInput = sweeps.createInput(
        prof, path, adsk.fusion.FeatureOperations.NewComponentFeatureOperation)
    sweep = sweeps.add(sweepInput)

    component = comp_profile.occurrences.item(
        comp_profile.occurrences.count - 1
    ).component
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
        entities.add(old_sketch.sketchCurves.sketchLines[0])

    if len(old_sketch.sketchCurves.sketchArcs) > 0:
        entities.add(old_sketch.sketchCurves.sketchArcs[0])

    if len(old_sketch.sketchCurves.sketchConicCurves) > 0:
        entities.add(old_sketch.sketchCurves.sketchConicCurves[0])

    if len(old_sketch.sketchCurves.sketchFittedSplines) > 0:
        entities.add(old_sketch.sketchCurves.sketchFittedSplines[0])

    if len(old_sketch.sketchCurves.sketchFixedSplines) > 0:
        entities.add(old_sketch.sketchCurves.sketchFixedSplines[0])

    if len(old_sketch.sketchTexts) > 0:
        entities.add(old_sketch.sketchTexts[0])

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
    comp = get_component(name).component
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

def hole(name: str):
    ...
