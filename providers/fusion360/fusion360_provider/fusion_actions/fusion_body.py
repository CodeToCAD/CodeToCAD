from .common import make_axis2, make_collection, make_matrix, make_vector
from .fusion_interface import FusionInterface

import adsk.core, adsk.fusion

from .base import get_body, get_or_create_component, get_or_create_sketch


class FusionBody(FusionInterface):
    component: adsk.fusion.Component
    instance: adsk.fusion.BRepBody = None
    sketch: adsk.fusion.Sketch
    def __init__(self, name):
        self.component = get_or_create_component(name)
        # self.instance = get_body(self.component, name)
        self.sketch = get_or_create_sketch(self.component, name)

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

        if body is None:
            return

        bodies = make_collection()
        bodies.add(body)

        origin = self.center

        # @check
        axis, sketch = make_axis2(axis_input, origin)

        angle = adsk.core.ValueInput.createByReal(math.radians(angle))

        moveFeats = features.moveFeatures
        moveFeatureInput = moveFeats.createInput2(bodies)
        moveFeatureInput.defineAsRotate(axis, angle)
        moveFeats.add(moveFeatureInput)

        sketch.deleteMe()

    def scale(self, x: float, y: float, z: float):
        body = self.instance

        boundBox = body.boundingBox

        xFactor = 1
        yFactor = 1
        zFactor = 1

        if x > 0:
            if 0 > boundBox.minPoint.x < 1:
                xFactor += (abs(boundBox.minPoint.x) + x) * abs(boundBox.minPoint.x)
            else:
                xFactor +=  abs(boundBox.minPoint.x) / (abs(boundBox.minPoint.x) + x)

        if y > 0:
            if 0 > boundBox.minPoint.y < 1:
                yFactor += (abs(boundBox.minPoint.y) + y) * abs(boundBox.minPoint.y)
            else:
                yFactor += abs(boundBox.minPoint.y) / (abs(boundBox.minPoint.y) + y)

        if z > 0:
            if 0 > boundBox.minPoint.z < 1:
                zFactor += (abs(boundBox.minPoint.z) + z) * abs(boundBox.minPoint.z)
            else:
                zFactor += abs(boundBox.minPoint.z) / (abs(boundBox.minPoint.z) + z)


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

    @property
    def center(self):
        boundBox = self.instance.boundingBox

        center = adsk.core.Point3D.create(
            (boundBox.minPoint.x + boundBox.maxPoint.x) / 2,
            (boundBox.minPoint.y + boundBox.maxPoint.y) / 2,
            (boundBox.minPoint.z + boundBox.maxPoint.z) / 2,
        )

        return center
