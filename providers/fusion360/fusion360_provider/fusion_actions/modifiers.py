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
    # @check this point must be an landmark or center of and object
    resolveAxis, sketchAxis = make_axis(axis, adsk.core.Point3D.create(0, 0, 0))

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

def make_loft(
    component: adsk.fusion.Component,
    sketch1: adsk.fusion.Sketch,
    sketch2: adsk.fusion.Sketch,
) -> adsk.fusion.BRepBody:
    loftFeats = component.features.loftFeatures
    loftInput = loftFeats.createInput(
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    )
    loftSectionsObj = loftInput.loftSections
    loftSectionsObj.add(sketch1.profiles.item(0))
    loftSectionsObj.add(sketch2.profiles.item(0))
    loftInput.isSolid = True
    loftInput.isClosed = True
    _ = loftFeats.add(loftInput)

    body = component.bRepBodies.item(component.bRepBodies.count - 1)
    body.name = component.name.split(":")[0]

    return body
