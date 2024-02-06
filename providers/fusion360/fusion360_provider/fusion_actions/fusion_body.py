from .actions import clone_body
from .common import make_axis, make_collection, make_matrix, make_vector
from .fusion_interface import FusionInterface

import adsk.core, adsk.fusion

from .base import delete_occurrence, get_or_create_component, get_or_create_sketch


class FusionBody(FusionInterface):
    component: adsk.fusion.Component
    instance: adsk.fusion.BRepBody = None
    sketch: adsk.fusion.Sketch
    def __init__(self, name):
        self.component = get_or_create_component(name)
        self.sketch = get_or_create_sketch(self.component, name)

    # def translate(self, x: float, y: float, z: float):
    def translate(self, x: float, y: float, z: float):
        features = self.component.features

        body = self.instance

        bodies = make_collection()
        bodies.add(body)

        transform = make_matrix()
        transform.translation = make_vector(x, y, z)

        moveFeats = features.moveFeatures
        moveFeatureInput = moveFeats.createInput2(bodies)
        moveFeatureInput.defineAsFreeMove(transform)
        moveFeats.add(moveFeatureInput)

    def rotate(self, axis_input: str, angle: float):
        import math

        features = self.component.features

        body = self.instance

        bodies = make_collection()
        bodies.add(body)

        origin = self.center

        axis, sketch = make_axis(axis_input, origin)

        angle = adsk.core.ValueInput.createByReal(math.radians(angle))

        moveFeats = features.moveFeatures
        moveFeatureInput = moveFeats.createInput2(bodies)
        moveFeatureInput.defineAsRotate(axis, angle)
        moveFeats.add(moveFeatureInput)

        sketch.deleteMe()

    def scale(self, x: float, y: float, z: float):
        body = self.instance
        sketch = self.sketch

        # diffent value when body is rotated first
        boundBox = body.boundingBox

        xFactor = 1
        yFactor = 1
        zFactor = 1

        distanceX = boundBox.maxPoint.x - boundBox.minPoint.x
        distanceY = boundBox.maxPoint.y - boundBox.minPoint.y
        distanceZ = boundBox.maxPoint.z - boundBox.minPoint.z

        if x > 0:
            if 0 > abs(distanceX) < 1:
                xFactor += (abs(distanceX) + x) * abs(distanceX)
            else:
                xFactor +=  abs(distanceX) / (abs(distanceX) + x)

        if y > 0:
            if 0 > abs(distanceY) < 1:
                yFactor += (abs(distanceY) + y) * abs(distanceY)
            else:
                yFactor += abs(distanceY) / (abs(distanceY) + y)

        if z > 0:
            if 0 > abs(distanceZ) < 1:
                zFactor += (abs(distanceZ) + z) * abs(distanceZ)
            else:
                zFactor += abs(distanceZ) / (abs(distanceZ) + z)

        inputColl = adsk.core.ObjectCollection.create()
        inputColl.add(body)

        basePt = self.sketch.sketchPoints.item(0)
        scaleFactor = adsk.core.ValueInput.createByReal(1)

        scales = self.component.features.scaleFeatures
        scaleInput = scales.createInput(inputColl, basePt, scaleFactor)

        xScale = adsk.core.ValueInput.createByReal(xFactor)
        yScale = adsk.core.ValueInput.createByReal(yFactor)
        zScale = adsk.core.ValueInput.createByReal(zFactor)
        scaleInput.setToNonUniform(xScale, yScale, zScale)

        scale = scales.add(scaleInput)

    def scale_by_factor(self, x: float, y: float, z: float):
        body = self.instance

        inputColl = adsk.core.ObjectCollection.create()
        inputColl.add(body)

        basePt = self.sketch.sketchPoints.item(0)
        scaleFactor = adsk.core.ValueInput.createByReal(1)

        scales = self.component.features.scaleFeatures
        scaleInput = scales.createInput(inputColl, basePt, scaleFactor)

        xScale = adsk.core.ValueInput.createByReal(x)
        yScale = adsk.core.ValueInput.createByReal(y)
        zScale = adsk.core.ValueInput.createByReal(z)
        scaleInput.setToNonUniform(xScale, yScale, zScale)

        scale = scales.add(scaleInput)

    def scale_uniform(self, scale: float):
        body = self.instance

        inputColl = adsk.core.ObjectCollection.create()
        inputColl.add(body)

        basePt = self.sketch.sketchPoints.item(0)
        scaleFactor = adsk.core.ValueInput.createByReal(scale)

        scales = self.component.features.scaleFeatures
        scaleInput = scales.createInput(inputColl, basePt, scaleFactor)

        scale = scales.add(scaleInput)

    def clone(self, new_name: str, copy_landmarks) -> adsk.fusion.BRepBody:
        body = clone_body(self.instance, new_name, copy_landmarks)
        return body

    def rename(self, new_name: str):
        self.component.name = new_name
        self.sketch.name = new_name

        if self.instance:
            self.instance.name = new_name

    def delete(self):
        delete_occurrence(self.component.name)

    @property
    def center(self):
        # boundBox = self.instance.boundingBox
        boundBox = self.sketch.boundingBox

        center = adsk.core.Point3D.create(
            (boundBox.minPoint.x + boundBox.maxPoint.x) / 2,
            (boundBox.minPoint.y + boundBox.maxPoint.y) / 2,
            (boundBox.minPoint.z + boundBox.maxPoint.z) / 2,
        )

        return center
