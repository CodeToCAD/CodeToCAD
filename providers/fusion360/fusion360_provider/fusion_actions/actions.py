import adsk.core, adsk.fusion
from providers.fusion360.fusion360_provider.fusion_actions.base import get_body, get_occurrence
from providers.fusion360.fusion360_provider.fusion_actions.common import make_axis
from .fusion_interface import FusionInterface

def mirror(
    obj: FusionInterface,
    other: adsk.core.Point3D,
    axis: str
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
        (centerOtherBody.x - centerBody.x) ** 2 +
        (centerOtherBody.y - centerBody.y) ** 2 +
        (centerOtherBody.z - centerBody.z) ** 2
    )

    assert distance > 0.01, "Can't mirror an item that's at the same position!"

    def move(distance1: float, distance2: float) -> float:
        # known bug when it's a sketch and a body at same axis
        # the center height difference gives a "wrong" answer
        if distance1 + distance2 == 0:
            return distance1 - distance2
        return distance1 + distance2

    if axis == "x":
        adsk.core.Application.get().userInterface.messageBox(
            f"{distanceBodyToOther.x, distance}"
        )
        newPosition = adsk.core.Point3D.create(
            move(distanceBodyToOther.x, distance),
            distanceBodyToOther.y,
            distanceBodyToOther.z,
        )
    elif axis == "y":
        newPosition = adsk.core.Point3D.create(
            distanceBodyToOther.x,
            move(distanceBodyToOther.y, distance),
            distanceBodyToOther.z,
        )
    elif axis == "z":
        newPosition = adsk.core.Point3D.create(
            distanceBodyToOther.x,
            distanceBodyToOther.y,
            move(distanceBodyToOther.z, distance),
        )

    newName = f"{obj.instance.name} clone"
    newObj = obj.clone(newName, True)

    return newObj, newPosition


def clone_sketch(
    old_sketch: adsk.fusion.Sketch,
    new_name: str,
    copy_landmarks: bool = True,
):
    _ = copy_landmarks # @check how to implement

    app = adsk.core.Application.get()
    design = app.activeProduct

    newComp = design.rootComponent.occurrences.addNewComponent(adsk.core.Matrix3D.create()).component
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

    old_sketch.copy(entities, adsk.core.Matrix3D.create(), new_sketch)

    return new_sketch

def clone_body(
    old_body: adsk.fusion.BRepBody,
    new_name: str,
    copy_landmarks: bool = True,
) -> adsk.fusion.BRepBody:
    _ = copy_landmarks # @check how to implement

    app = adsk.core.Application.get()
    design = app.activeProduct

    newComp = design.rootComponent.occurrences.addNewComponent(adsk.core.Matrix3D.create()).component
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
    angle: float,
    axis: str
):
    features = component.features

    inputEntites = adsk.core.ObjectCollection.create()
    inputEntites.add(body)

    axisInput, sketch = make_axis(axis, center)

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
    axis: str
):
    features = component.features

    occ = get_occurrence(component.name)

    inputEntites = adsk.core.ObjectCollection.create()
    inputEntites.add(occ)

    if axis == "x":
        axisInput = component.xConstructionAxis
    elif axis == "y":
        axisInput = component.yConstructionAxis
    elif axis == "z":
        axisInput = component.zConstructionAxis

    quantity = adsk.core.ValueInput.createByReal(count)
    distance = adsk.core.ValueInput.createByReal(offset)
    one = adsk.core.ValueInput.createByReal(1)

    rectangularPatterns = features.rectangularPatternFeatures
    rectangularPatternInput = rectangularPatterns.createInput(
        inputEntites, axisInput,
        quantity, distance, adsk.fusion.PatternDistanceType.SpacingPatternDistanceType)
    rectangularPatternInput.setDirectionTwo(axisInput, one, one)

    rectangularFeature = rectangularPatterns.add(rectangularPatternInput)


def create_circular_pattern_sketch(
    component: adsk.fusion.Component,
    center: adsk.core.Point3D,
    count: int,
    angle: float,
    axis: str
):
    occ = get_occurrence(component.name)

    inputEntites = adsk.core.ObjectCollection.create()
    inputEntites.add(occ)

    axisInput, sketch = make_axis(axis, center)

    circularFeats = component.features.circularPatternFeatures
    circularFeatInput = circularFeats.createInput(inputEntites, axisInput)
    circularFeatInput.quantity = adsk.core.ValueInput.createByReal(count)
    circularFeatInput.totalAngle = adsk.core.ValueInput.createByReal(angle)
    circularFeatInput.isSymmetric = True

    circularFeature = circularFeats.add(circularFeatInput)

    sketch.deleteMe()

def create_rectangular_pattern_sketch(
    component: adsk.fusion.Component,
    count: int,
    offset: float,
    axis: str
):
    occ = get_occurrence(component.name)

    inputEntites = adsk.core.ObjectCollection.create()
    inputEntites.add(occ)

    if axis == "x":
        axisInput = component.xConstructionAxis
    elif axis == "y":
        axisInput = component.yConstructionAxis
    elif axis == "z":
        axisInput = component.zConstructionAxis

    quantity = adsk.core.ValueInput.createByReal(count)
    distance = adsk.core.ValueInput.createByReal(offset)
    one = adsk.core.ValueInput.createByReal(1)

    rectangularPatterns = component.features.rectangularPatternFeatures
    rectangularPatternInput = rectangularPatterns.createInput(
        inputEntites, axisInput,
        quantity, distance, adsk.fusion.PatternDistanceType.SpacingPatternDistanceType)
    rectangularPatternInput.setDirectionTwo(axisInput, one, one)

    rectangularFeature = rectangularPatterns.add(rectangularPatternInput)
