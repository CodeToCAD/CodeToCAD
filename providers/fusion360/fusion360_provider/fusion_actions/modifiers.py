from codetocad import *

import adsk.core, adsk.fusion
from .common import make_axis, make_axis_from_points

def make_revolve(
    component: adsk.fusion.Component,
    sketch: adsk.fusion.Sketch,
    angle: AngleOrItsFloatOrStringValue,
    start: adsk.core.Point3D = adsk.core.Point3D.create(0, 0, 0),
    end: adsk.core.Point3D = adsk.core.Point3D.create(0, 0, 0),
) -> adsk.fusion.BRepBody:
    resolveAxis, sketchAxis = make_axis_from_points(start, end)

    revolveFeatures = component.features.revolveFeatures
    input = revolveFeatures.createInput(
        sketch.profiles.item(0),
        resolveAxis,
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    )
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
