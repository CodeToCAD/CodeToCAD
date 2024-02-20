from typing import Optional
import adsk.core, adsk.fusion
from codetocad.codetocad_types import (
    AngleOrItsFloatOrStringValue,
    AxisOrItsIndexOrItsName,
    MaterialOrItsName,
)
from codetocad.core.angle import Angle
from codetocad.core.point import Point
from codetocad.enums.axis import Axis
from codetocad.enums.preset_material import PresetMaterial
from codetocad.providers_sample.vertex import Vertex
from .base import get_body, get_occurrence, get_root_component
from .common import make_axis
from .fusion_interface import FusionInterface


def mirror(
    obj: FusionInterface, other: adsk.core.Point3D, axis: AxisOrItsIndexOrItsName
):
    centerBody = obj.center
    centerOtherBody = other

    distanceBodyToOther = adsk.core.Point3D.create(
        centerOtherBody.x - centerBody.x,
        centerOtherBody.y - centerBody.y,
        centerOtherBody.z - centerBody.z,
    )

    import math

    distance = math.sqrt(
        (centerOtherBody.x - centerBody.x) ** 2
        + (centerOtherBody.y - centerBody.y) ** 2
        + (centerOtherBody.z - centerBody.z) ** 2
    )

    assert distance > 0.01, "Can't mirror an item that's at the same position!"

    def move(distance1: float, distance2: float) -> float:
        if distance1 + distance2 == 0:
            return distance1 - distance2
        return distance1 + distance2

    match Axis.from_string(axis).value:
        case Axis.X.value:
            newPosition = adsk.core.Point3D.create(
                move(distanceBodyToOther.x, distance),
                distanceBodyToOther.y,
                distanceBodyToOther.z,
            )
        case Axis.Y.value:
            newPosition = adsk.core.Point3D.create(
                distanceBodyToOther.x,
                move(distanceBodyToOther.y, distance),
                distanceBodyToOther.z,
            )
        case Axis.Z.value:
            newPosition = adsk.core.Point3D.create(
                distanceBodyToOther.x,
                distanceBodyToOther.y,
                move(distanceBodyToOther.z, distance),
            )
        case _:
            raise Exception(f"Invalid Axis! Got {Axis.from_string(axis).value}")

    newName = f"{obj.instance.name} clone"
    newObj = obj.clone(newName, True)

    return newObj, newPosition


def clone_sketch(
    old_sketch: adsk.fusion.Sketch,
    new_name: str,
    copy_landmarks: bool = True,
):
    app = adsk.core.Application.get()
    design = app.activeProduct

    newComp = design.rootComponent.occurrences.addNewComponent(
        adsk.core.Matrix3D.create()
    ).component
    newComp.name = new_name

    sketches = newComp.sketches
    xyPlane = newComp.xYConstructionPlane

    new_sketch = sketches.add(xyPlane)
    new_sketch.name = new_name

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

    if len(old_sketch.sketchPoints) > 0 and copy_landmarks:
        # @check creating 2 landmarks
        for landmark in old_sketch.sketchPoints:
            entities.add(landmark)

    old_sketch.copy(entities, adsk.core.Matrix3D.create(), new_sketch)

    return new_sketch


def clone_body(
    old_body: adsk.fusion.BRepBody,
    new_name: str,
    copy_landmarks: bool = True,
) -> adsk.fusion.BRepBody:
    _ = copy_landmarks

    app = adsk.core.Application.get()
    design = app.activeProduct

    newComp = design.rootComponent.occurrences.addNewComponent(
        adsk.core.Matrix3D.create()
    ).component
    newComp.name = new_name

    newComp.features.copyPasteBodies.add(old_body)

    body = get_body(newComp, old_body.name)
    body.name = new_name

    return body


def create_circular_pattern(
    component: adsk.fusion.Component,
    body: adsk.fusion.BRepBody,
    center: adsk.core.Point3D,
    count: int,
    angle: AngleOrItsFloatOrStringValue,
    axis: AxisOrItsIndexOrItsName,
):
    features = component.features

    inputEntites = adsk.core.ObjectCollection.create()
    inputEntites.add(body)

    axisInput, sketch = make_axis(axis, center)

    angle = Angle.from_angle_or_its_float_or_string_value(angle).to_radians().value

    circularFeats = features.circularPatternFeatures
    circularFeatInput = circularFeats.createInput(inputEntites, axisInput)
    circularFeatInput.quantity = adsk.core.ValueInput.createByReal(count)
    circularFeatInput.totalAngle = adsk.core.ValueInput.createByReal(angle)
    circularFeatInput.isSymmetric = False

    circularFeature = circularFeats.add(circularFeatInput)

    sketch.deleteMe()


def create_rectangular_pattern(
    component: adsk.fusion.Component,
    count: int,
    offset: float,
    axis: AxisOrItsIndexOrItsName,
):
    features = component.features

    occ = get_occurrence(component.name)

    inputEntites = adsk.core.ObjectCollection.create()
    inputEntites.add(occ)

    match Axis.from_string(axis).value:
        case Axis.X.value:
            axisInput = component.xConstructionAxis
        case Axis.Y.value:
            axisInput = component.yConstructionAxis
        case Axis.Z.value:
            axisInput = component.zConstructionAxis

    quantity = adsk.core.ValueInput.createByReal(count)
    distance = adsk.core.ValueInput.createByReal(offset)
    one = adsk.core.ValueInput.createByReal(1)

    rectangularPatterns = features.rectangularPatternFeatures
    rectangularPatternInput = rectangularPatterns.createInput(
        inputEntites,
        axisInput,
        quantity,
        distance,
        adsk.fusion.PatternDistanceType.SpacingPatternDistanceType,
    )
    rectangularPatternInput.setDirectionTwo(axisInput, one, one)

    rectangularFeature = rectangularPatterns.add(rectangularPatternInput)


def create_circular_pattern_sketch(
    fusion_interface: FusionInterface,
    center: adsk.core.Point3D,
    count: int,
    angle: AngleOrItsFloatOrStringValue,
    axis: AxisOrItsIndexOrItsName,
):
    occ = get_occurrence(fusion_interface.component.name)

    angle = Angle.from_angle_or_its_float_or_string_value(angle).to_radians().value

    inputEntites = adsk.core.ObjectCollection.create()
    inputEntites.add(occ)

    axisInput, sketch = make_axis(axis, center)
    circularFeats = fusion_interface.component.features.circularPatternFeatures
    circularFeatInput = circularFeats.createInput(inputEntites, axisInput)
    circularFeatInput.quantity = adsk.core.ValueInput.createByReal(count)
    circularFeatInput.totalAngle = adsk.core.ValueInput.createByReal(angle)
    circularFeatInput.isSymmetric = True

    circularFeature = circularFeats.add(circularFeatInput)

    # @check sphere with axis x and y
    fusion_interface.translate(center.x, center.y, center.z)

    sketch.deleteMe()


def create_rectangular_pattern_sketch(
    component: adsk.fusion.Component,
    count: int,
    offset: float,
    axis: AxisOrItsIndexOrItsName,
):
    occ = get_occurrence(component.name)

    inputEntites = adsk.core.ObjectCollection.create()
    inputEntites.add(occ)

    match Axis.from_string(axis).value:
        case Axis.X.value:
            axisInput = component.xConstructionAxis
        case Axis.Y.value:
            axisInput = component.yConstructionAxis
        case Axis.Z.value:
            axisInput = component.zConstructionAxis

    quantity = adsk.core.ValueInput.createByReal(count)
    distance = adsk.core.ValueInput.createByReal(offset)
    one = adsk.core.ValueInput.createByReal(1)

    rectangularPatterns = component.features.rectangularPatternFeatures
    rectangularPatternInput = rectangularPatterns.createInput(
        inputEntites,
        axisInput,
        quantity,
        distance,
        adsk.fusion.PatternDistanceType.SpacingPatternDistanceType,
    )
    rectangularPatternInput.setDirectionTwo(axisInput, one, one)

    rectangularFeature = rectangularPatterns.add(rectangularPatternInput)


def combine_action(
    body: adsk.fusion.BRepBody,
    otherBody: adsk.fusion.BRepBody,
    operation: adsk.fusion.FeatureOperations,
    deleteAfter: bool,
):
    rootComp = get_root_component()
    features = rootComp.features

    bodyCollection = adsk.core.ObjectCollection.create()
    bodyCollection.add(otherBody)

    combineFeatures = features.combineFeatures
    combineFeaturesInput = combineFeatures.createInput(body, bodyCollection)
    combineFeaturesInput.operation = operation
    combineFeaturesInput.isNewComponent = False
    combineFeaturesInput.isKeepToolBodies = False
    combine_feature = combineFeatures.add(combineFeaturesInput)

    if deleteAfter:
        otherBody.deleteMe()


def combine(
    body: adsk.fusion.BRepBody,
    otherBody: adsk.fusion.BRepBody,
    deleteAfter: bool,
):
    combine_action(
        body,
        otherBody,
        adsk.fusion.FeatureOperations.JoinFeatureOperation,
        deleteAfter,
    )


def subtract(
    body: adsk.fusion.BRepBody,
    otherBody: adsk.fusion.BRepBody,
    deleteAfter: bool,
):
    combine_action(
        body,
        otherBody,
        adsk.fusion.FeatureOperations.CutFeatureOperation,
        deleteAfter,
    )


def intersect(
    body: adsk.fusion.BRepBody,
    otherBody: adsk.fusion.BRepBody,
    deleteAfter: bool,
):
    combine_action(
        body,
        otherBody,
        adsk.fusion.FeatureOperations.IntersectFeatureOperation,
        deleteAfter,
    )


def sweep(
    path_component: adsk.fusion.Component,
    path_sketch: adsk.fusion.Sketch,
    profile_component: adsk.fusion.Component,
    profile_sketch: adsk.fusion.Sketch,
) -> str:
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

    path = path_component.features.createPath(paths)

    prof = profile_sketch.profiles.item(0)

    sweeps = profile_component.features.sweepFeatures
    sweepInput = sweeps.createInput(
        prof, path, adsk.fusion.FeatureOperations.NewComponentFeatureOperation
    )
    sweep = sweeps.add(sweepInput)

    rootComp = get_root_component()

    occurrence = rootComp.occurrences.item(rootComp.occurrences.count - 1)
    component = occurrence.component

    component.name = f"Sweep {profile_component.name}"

    return component.name


def create_text(
    sketch: adsk.fusion.Sketch,
    text: str,
    font_size: float,
    bold: bool,
    italic: bool,
    underlined: bool,
    character_spainc: int,
    word_spacing: int,
    line_spacing: int,
    font_file_path: Optional[str] = None,
):
    texts = sketch.sketchTexts

    line = sketch.sketchCurves.sketchLines.addByTwoPoints(
        adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(len(text), 0, 0)
    )
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


def hollow(
    component: adsk.fusion.Component, body: adsk.fusion.BRepBody, thickness: float
):
    entities = adsk.core.ObjectCollection.create()
    for face in body.faces:
        _, normal = face.evaluator.getNormalAtPoint(face.pointOnFace)
        if normal.z > 0:
            entities.add(face)

    shellFeatures = component.features.shellFeatures
    shellInput = shellFeatures.createInput(entities, False)
    thicknessInput = adsk.core.ValueInput.createByReal(thickness)
    shellInput.insideThickness = thicknessInput
    shellFeatures.add(shellInput)


def hole(
    component: adsk.fusion.Component, body: adsk.fusion.BRepBody, point, radius, depth
):
    # select the top face
    face_selected = None
    for face in body.faces:
        _, normal = face.evaluator.getNormalAtPoint(face.pointOnFace)
        if normal.z > 0:
            face_selected = face

    # holeDiam = adsk.core.ValueInput.createByString('20 mm')
    holeDiam = adsk.core.ValueInput.createByReal(radius)
    holeDepth = adsk.core.ValueInput.createByReal(depth)

    holeFeatures = component.features.holeFeatures

    input = holeFeatures.createSimpleInput(holeDiam)
    input.setDistanceExtent(holeDepth)
    input.setPositionByPoint(
        face_selected, adsk.core.Point3D.create(point.x, point.y, point.z)
    )
    holeFeature = holeFeatures.add(input)


def fillet_all_edges(
    component: adsk.fusion.Component, body: adsk.fusion.BRepBody, radius: float
):
    entities = adsk.core.ObjectCollection.create()
    for edge in body.edges:
        entities.add(edge)

    offset = adsk.core.ValueInput.createByReal(radius)

    fillets = component.features.filletFeatures
    filletInput = fillets.createInput()
    filletInput.addConstantRadiusEdgeSet(entities, offset, True)
    fillet = fillets.add(filletInput)


def chamfer_all_edges(
    component: adsk.fusion.Component, body: adsk.fusion.BRepBody, radius: float
):
    entities = adsk.core.ObjectCollection.create()
    for edge in body.edges:
        entities.add(edge)

    offset = adsk.core.ValueInput.createByReal(radius)

    chamfers = component.features.chamferFeatures
    chamferInput = chamfers.createInput2()
    chamferInput.chamferEdgeSets.addEqualDistanceChamferEdgeSet(entities, offset, True)
    chamfer = chamfers.add(chamferInput)


def set_material(fusion_interface: FusionInterface, material_name: MaterialOrItsName):
    body = fusion_interface.instance

    if isinstance(material_name, str):
        try:
            material_name = getattr(PresetMaterial, material_name)
        except:
            raise Exception(f"Preset {material_name} not found!")

    r, g, b, a = material_name.color
    color = adsk.core.Color.create(r, g, b, round(a * 255))

    appearance = body.appearance

    appearance.name = material_name.name

    colorProp = adsk.core.ColorProperty.cast(
        appearance.appearanceProperties.itemByName("Color")
    )
    colorProp.value = color
    roughnessProp = appearance.appearanceProperties.itemByName("Roughness")
    roughnessProp.value = material_name.roughness

    body.appearance = appearance
