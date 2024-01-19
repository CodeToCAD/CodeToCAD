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

    # Get the root component of the active design.
    rootComp = design.rootComponent
    features = rootComp.features

    body = get_body(name)

    bodies = adsk.core.ObjectCollection.create()
    bodies.add(body)

    transform = adsk.core.Matrix3D.create()
    transform.translation = vector

    # Create a move feature
    moveFeats = features.moveFeatures
    moveFeatureInput = moveFeats.createInput2(bodies)
    moveFeatureInput.defineAsFreeMove(transform)
    moveFeats.add(moveFeatureInput)

def rotate_body(name: str, axis: adsk.core.Vector3D, angle: float):
    app = adsk.core.Application.get()
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    rootComp = design.rootComponent

    # TODO
