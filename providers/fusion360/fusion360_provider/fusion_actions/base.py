from typing import Optional

import adsk.core, adsk.fusion


def get_or_create_component(name: str) -> adsk.fusion.Component:
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent

    for occurrence in rootComp.occurrences:
        # if name == occurrence.component.name.split(":")[0]:
        if name == occurrence.component.name:
            return occurrence.component

    component = rootComp.occurrences.addNewComponent(
        adsk.core.Matrix3D.create()
    ).component
    component.name = name

    return component


def get_or_create_sketch(component, name: str) -> adsk.fusion.Sketch:
    sketch = component.sketches.itemByName(name)
    if sketch:
        return sketch

    sketches = component.sketches
    xyPlane = component.xYConstructionPlane

    sketch = sketches.add(xyPlane)
    sketch.name = name

    return sketch

def get_occurrence(name: str) -> Optional[adsk.fusion.Occurrence]:
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent

    for occurrence in rootComp.occurrences:
        # if name == occurrence.component.name.split(":")[0]:
        if name == occurrence.component.name:
            return occurrence

    return None


def get_body(component, name: str) -> Optional[adsk.fusion.BRepBody]:
    body = component.bRepBodies.itemByName(name)
    return body


# should be in common.py
def axis_vector(axis_input: str):
    if axis_input == "x":
        axis = adsk.core.Vector3D.create(1, 0, 0)
    elif axis_input == "y":
        axis = adsk.core.Vector3D.create(0, 1, 0)
    elif axis_input == "z":
        axis = adsk.core.Vector3D.create(0, 0, 1)
    return axis
