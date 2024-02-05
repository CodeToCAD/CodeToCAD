from codetocad import *

import adsk.core, adsk.fusion
from providers.fusion360.fusion360_provider.fusion_actions.common import make_axis

def make_revolve(
    component: adsk.fusion.Component,
    sketch: adsk.fusion.Sketch,
    angle: AngleOrItsFloatOrStringValue,
    about_entity_or_landmark: EntityOrItsName,
    axis: AxisOrItsIndexOrItsName
) -> adsk.fusion.BRepBody:
    resolveAxis, sketchAxis = make_axis(axis)

    operation = adsk.fusion.FeatureOperations.NewBodyFeatureOperation

    revolveFeatures = component.features.revolveFeatures
    input = revolveFeatures.createInput(sketch.profiles.item(0), resolveAxis, operation)
    angle = adsk.core.ValueInput.createByReal(angle)
    input.setAngleExtent(False, angle)
    _ = revolveFeatures.add(input)

    sketchAxis.deleteMe()

    body = component.bRepBodies.item(component.bRepBodies.count - 1)
    body.name = sketch.name

    return body
