from typing import Optional
from codetocad.interfaces.landmark_interface import LandmarkInterface
from codetocad.interfaces.part_interface import PartInterface
from codetocad.interfaces.sketch_interface import SketchInterface
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.codetocad_types import *
from providers.fusion360.fusion360_provider.fusion_actions.base import (
    get_body,
    get_component,
    get_sketch,
)
from .fusion_actions.fusion_body import FusionBody
from .fusion_actions.fusion_sketch import FusionSketch


class Entity(EntityInterface):

    def __init__(
        self, name: "str", description: "str| None" = None, native_instance=None
    ):
        self.name = name
        self.description = description
        self.native_instance = native_instance
        self.fusion_sketch = FusionSketch(name)
        self.fusion_body = FusionBody(name)

    @property
    def _center(self):
        if isinstance(self, PartInterface):
            return self.fusion_body.center
        if isinstance(self, SketchInterface):
            return self.fusion_sketch.center

    @supported(SupportLevel.PARTIAL, "Supports Part and Sketch entities.")
    def is_exists(self) -> bool:
        try:
            component = get_component(self.name)
            if isinstance(self, PartInterface):
                return get_body(component, self.name) != None
            elif isinstance(self, SketchInterface):
                return get_sketch(component, self.name) != None

            raise NotImplementedError()
        except:
            return False

    @supported(
        SupportLevel.PARTIAL,
        "Does not support the rename_linked_entities_and_landmarks parameter yet.",
    )
    def rename(
        self, new_name: "str", renamelinked_entities_and_landmarks: "bool" = True
    ):
        if isinstance(self, PartInterface):
            self.fusion_body.rename(new_name)
        if isinstance(self, SketchInterface):
            self.fusion_sketch.rename(new_name)
        if isinstance(self, LandmarkInterface):
            self.fusion_landmark.rename(new_name)

        self.name = new_name
        return self

    @supported(SupportLevel.PARTIAL, "Supports Part, Sketch and Landmark entities.")
    def delete(self, remove_children: "bool" = True):
        if isinstance(self, PartInterface):
            self.fusion_body.delete()
        if isinstance(self, SketchInterface):
            self.fusion_sketch.delete()
        if isinstance(self, LandmarkInterface):
            self.fusion_landmark.delete()
        return self

    @supported(SupportLevel.PLANNED)
    def is_visible(self) -> bool:
        raise NotImplementedError()
        return True

    @supported(SupportLevel.PLANNED)
    def set_visible(self, is_visible: "bool"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def apply(
        self,
        rotation: "bool" = True,
        scale: "bool" = True,
        location: "bool" = False,
        modifiers: "bool" = True,
    ):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PARTIAL, "Supports Part, Sketch and Landmark entities.")
    def get_native_instance(self) -> object:
        if isinstance(self, PartInterface):
            return self.fusion_body
        if isinstance(self, SketchInterface):
            return self.fusion_sketch
        if isinstance(self, LandmarkInterface):
            return self.fusion_landmark

        raise NotImplementedError()

    @supported(SupportLevel.PLANNED)
    def get_location_world(self) -> "Point":
        raise NotImplementedError()
        return Point.from_list_of_float_or_string([0, 0, 0])

    @supported(SupportLevel.PARTIAL, "Supports Part, Sketch and Landmark entities.")
    def get_location_local(self) -> "Point":
        if isinstance(self, PartInterface):
            pos = self.fusion_body.center
        elif isinstance(self, SketchInterface):
            pos = self.fusion_sketch.center
        elif isinstance(self, LandmarkInterface):
            pos = self.fusion_landmark.get_point()
        return Point(pos.x, pos.y, pos.z)

    @supported(SupportLevel.PLANNED)
    def select(self):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PARTIAL, "Supports Part, Sketch and Landmark entities.")
    def translate_xyz(
        self,
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ):
        if isinstance(self, PartInterface):
            self.fusion_body.translate(x, y, z)
        elif isinstance(self, SketchInterface):
            self.fusion_sketch.translate(x, y, z)
        elif isinstance(self, LandmarkInterface):
            self.fusion_landmark.translate(x, y, z)
        return self

    @supported(SupportLevel.PARTIAL, "Supports Part, Sketch and Landmark entities.")
    def translate_x(self, amount: "str|float|Dimension"):
        if isinstance(self, PartInterface):
            self.fusion_body.translate(amount, 0, 0)
        elif isinstance(self, SketchInterface):
            self.fusion_sketch.translate(amount, 0, 0)
        elif isinstance(self, LandmarkInterface):
            self.fusion_landmark.translate(amount, 0, 0)
        return self

    @supported(SupportLevel.PARTIAL, "Supports Part, Sketch and Landmark entities.")
    def translate_y(self, amount: "str|float|Dimension"):
        if isinstance(self, PartInterface):
            self.fusion_body.translate(0, amount, 0)
        elif isinstance(self, SketchInterface):
            self.fusion_sketch.translate(0, amount, 0)
        elif isinstance(self, LandmarkInterface):
            self.fusion_landmark.translate(0, amount, 0)
        return self

    @supported(SupportLevel.PARTIAL, "Supports Part, Sketch and Landmark entities.")
    def translate_z(self, amount: "str|float|Dimension"):

        if isinstance(self, PartInterface):
            self.fusion_body.translate(0, 0, amount)
        elif isinstance(self, SketchInterface):
            self.fusion_sketch.translate(0, 0, amount)
        elif isinstance(self, LandmarkInterface):
            self.fusion_landmark.translate(0, 0, amount)
        return self

    @supported(SupportLevel.PARTIAL, "Supports Part and Sketch entities.")
    def rotate_xyz(
        self, x: "str|float|Angle", y: "str|float|Angle", z: "str|float|Angle"
    ):
        self.rotate_x(x)
        self.rotate_y(y)
        self.rotate_z(z)
        return self

    @supported(SupportLevel.PARTIAL, "Supports Part and Sketch entities.")
    def rotate_x(self, rotation: "str|float|Angle"):

        if isinstance(self, PartInterface):
            self.fusion_body.rotate("x", rotation)
        elif isinstance(self, SketchInterface):
            self.fusion_sketch.rotate("x", rotation)
        else:
            raise NotImplementedError()
        return self

    @supported(SupportLevel.PARTIAL, "Supports Part and Sketch entities.")
    def rotate_y(self, rotation: "str|float|Angle"):

        if isinstance(self, PartInterface):
            self.fusion_body.rotate("y", rotation)
        elif isinstance(self, SketchInterface):
            self.fusion_sketch.rotate("y", rotation)
        else:
            raise NotImplementedError()
        return self

    @supported(SupportLevel.PARTIAL, "Supports Part and Sketch entities.")
    def rotate_z(self, rotation: "str|float|Angle"):

        if isinstance(self, PartInterface):
            self.fusion_body.rotate("z", rotation)
        elif isinstance(self, SketchInterface):
            self.fusion_sketch.rotate("z", rotation)
        else:
            raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED)
    def get_bounding_box(self) -> "BoundaryBox":

        if isinstance(self, PartInterface):
            boundaryBox = self.fusion_body.get_bounding_box()
        elif isinstance(self, SketchInterface):
            boundaryBox = self.fusion_sketch.get_bounding_box()
        else:
            raise NotImplementedError()
        return boundaryBox

    @supported(SupportLevel.SUPPORTED)
    def get_dimensions(self) -> "Dimensions":
        if isinstance(self, PartInterface):
            dimensions = self.fusion_body.get_dimensions()
        elif isinstance(self, SketchInterface):
            dimensions = self.fusion_sketch.get_dimensions()
        else:
            raise NotImplementedError()
        return dimensions
