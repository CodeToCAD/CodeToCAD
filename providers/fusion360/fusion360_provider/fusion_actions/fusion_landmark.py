from providers.fusion360.fusion360_provider.fusion_actions.common import make_point3d
from .actions import clone_sketch
from .fusion_interface import FusionInterface

from .base import delete_occurrence, get_or_create_component, get_or_create_sketch

import adsk.core


class FusionLandmark(FusionInterface):
    def __init__(self, name):
        self.component = get_or_create_component(name)
        self.instance = get_or_create_sketch(self.component, name)

    def create_landmark(self, x: float, y: float, z: float):
        point = make_point3d(x, y, z)
        self.instance.sketchPoints.add(point)

    def translate(self, x: float, y: float, z: float):
        matrix = adsk.core.Matrix3D.create()
        matrix.translation = adsk.core.Vector3D.create(x, y, z)

        sketch = self.instance

        entities = adsk.core.ObjectCollection.create()

        if len(sketch.sketchPoints) > 0:
            for line in sketch.sketchPoints:
                entities.add(line)

        sketch.move(entities, matrix)

    def clone(self, new_name: str, copy_landmarks) -> adsk.fusion.Sketch:
        sketch = clone_sketch(self.instance, new_name, copy_landmarks)
        return sketch

    def rename(self, new_name: str):
        self.component.name = new_name
        self.instance.name = new_name

    def delete(self):
        delete_occurrence(self.component.name)

    @property
    def center(self):
        boundBox = self.instance.boundingBox

        center = adsk.core.Point3D.create(
            (boundBox.minPoint.x + boundBox.maxPoint.x) / 2,
            (boundBox.minPoint.y + boundBox.maxPoint.y) / 2,
            (boundBox.minPoint.z + boundBox.maxPoint.z) / 2,
        )

        return center

    def scale(self, x: float, y: float, z: float):
        ...

    def scale_by_factor(self, x: float, y: float, z: float):
        ...

    def scale_uniform(self, scale: float):
        ...

    def extrude(self, length: float) -> str:
        ...
