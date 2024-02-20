from typing import Optional

import adsk.core, adsk.fusion


# https://modthemachine.typepad.com/my_weblog/2021/03/log-debug-messages-in-fusion-360.html
class UiLogger:
    def __init__(self, forceUpdate=True):
        app = adsk.core.Application.get()
        ui = app.userInterface
        palettes = ui.palettes
        self.textPalette = palettes.itemById("TextCommands")
        self.forceUpdate = forceUpdate
        self.textPalette.isVisible = True

    def print(self, text):
        self.textPalette.writeText(text)
        if self.forceUpdate:
            adsk.doEvents()


def get_root_component() -> adsk.fusion.Component:
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent
    return rootComp


def get_or_create_component(name: str) -> adsk.fusion.Component:
    rootComp = get_root_component()

    for occurrence in rootComp.occurrences:
        if name == occurrence.component.name:
            return occurrence.component

    component = rootComp.occurrences.addNewComponent(
        adsk.core.Matrix3D.create()
    ).component
    component.name = name

    return component


def get_component(name: str) -> adsk.fusion.Component:
    rootComp = get_root_component()

    for occurrence in rootComp.occurrences:
        if name == occurrence.component.name:
            return occurrence.component

    raise Exception(f"Component {name} not found!")


def get_or_create_sketch(component, name: str) -> adsk.fusion.Sketch:
    sketch = component.sketches.itemByName(name)
    if sketch:
        return sketch

    sketches = component.sketches
    xyPlane = component.xYConstructionPlane

    sketch = sketches.add(xyPlane)
    sketch.name = name

    return sketch


def get_sketch(component, name: str) -> adsk.fusion.Sketch:
    sketch = component.sketches.itemByName(name)
    if sketch:
        return sketch

    raise Exception(f"Sketch {name} not found!")


def get_occurrence(name: str) -> Optional[adsk.fusion.Occurrence]:
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent

    for occurrence in rootComp.occurrences:
        if name == occurrence.component.name:
            return occurrence

    return None


def delete_occurrence(name: str):
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent

    for occurrence in rootComp.occurrences:
        if name == occurrence.component.name:
            occurrence.deleteMe()


def delete_all_occurrence():
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent

    for occurrence in rootComp.occurrences:
        occurrence.deleteMe()


def get_body(component, name: str) -> Optional[adsk.fusion.BRepBody]:
    body = component.bRepBodies.itemByName(name)
    return body
