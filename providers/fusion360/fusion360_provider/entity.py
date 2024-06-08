from typing import Optional
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.codetocad_types import *
from .fusion_actions.fusion_body import FusionBody
from .fusion_actions.fusion_sketch import FusionSketch


class Entity(EntityInterface):
    name: str
    description: Optional[str] = None
    native_instance = None

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
        from . import Part, Sketch

        if isinstance(self, Part):
            return self.fusion_body.center
        if isinstance(self, Sketch):
            return self.fusion_sketch.center

    @supported(SupportLevel.UNSUPPORTED)
    def is_exists(self) -> bool:
        print("is_exists called:")
        return True

    @supported(SupportLevel.UNSUPPORTED)
    def rename(
        self, new_name: "str", renamelinked_entities_and_landmarks: "bool" = True
    ):
        from . import Part, Sketch, Landmark

        if isinstance(self, Part):
            self.fusion_body.rename(new_name)
        if isinstance(self, Sketch):
            self.fusion_sketch.rename(new_name)
        if isinstance(self, Landmark):
            self.fusion_landmark.rename(new_name)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def delete(self, remove_children: "bool" = True):
        from . import Part, Sketch, Landmark

        if isinstance(self, Part):
            self.fusion_body.delete()
        if isinstance(self, Sketch):
            self.fusion_sketch.delete()
        if isinstance(self, Landmark):
            self.fusion_landmark.delete()
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def is_visible(self) -> bool:
        print("is_visible called:")
        return True

    @supported(SupportLevel.UNSUPPORTED)
    def set_visible(self, is_visible: "bool"):
        print("set_visible called:", is_visible)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def apply(
        self,
        rotation: "bool" = True,
        scale: "bool" = True,
        location: "bool" = False,
        modifiers: "bool" = True,
    ):
        print("apply called:", rotation, scale, location, modifiers)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def get_native_instance(self) -> object:
        print("get_native_instance called:")
        return "instance"

    @supported(SupportLevel.UNSUPPORTED)
    def get_location_world(self) -> "Point":
        print("get_location_world called:")
        return Point.from_list_of_float_or_string([0, 0, 0])

    @supported(SupportLevel.UNSUPPORTED)
    def get_location_local(self) -> "Point":
        # check the correct behavior
        from . import Part, Sketch, Landmark

        if isinstance(self, Part):
            pos = self.fusion_body.center
        elif isinstance(self, Sketch):
            pos = self.fusion_sketch.center
        elif isinstance(self, Landmark):
            pos = self.fusion_landmark.get_point()
        return Point(pos.x, pos.y, pos.z)

    @supported(SupportLevel.UNSUPPORTED)
    def select(self):
        print("select called:")
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def translate_xyz(
        self,
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ):
        from . import Part, Sketch, Landmark

        if isinstance(self, Part):
            self.fusion_body.translate(x, y, z)
        elif isinstance(self, Sketch):
            self.fusion_sketch.translate(x, y, z)
        elif isinstance(self, Landmark):
            self.fusion_landmark.translate(x, y, z)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def translate_x(self, amount: "str|float|Dimension"):
        from . import Part, Sketch, Landmark

        if isinstance(self, Part):
            self.fusion_body.translate(amount, 0, 0)
        elif isinstance(self, Sketch):
            self.fusion_sketch.translate(amount, 0, 0)
        elif isinstance(self, Landmark):
            self.fusion_landmark.translate(amount, 0, 0)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def translate_y(self, amount: "str|float|Dimension"):
        from . import Part, Sketch, Landmark

        if isinstance(self, Part):
            self.fusion_body.translate(0, amount, 0)
        elif isinstance(self, Sketch):
            self.fusion_sketch.translate(0, amount, 0)
        elif isinstance(self, Landmark):
            self.fusion_landmark.translate(0, amount, 0)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def translate_z(self, amount: "str|float|Dimension"):
        from . import Part, Sketch, Landmark

        if isinstance(self, Part):
            self.fusion_body.translate(0, 0, amount)
        elif isinstance(self, Sketch):
            self.fusion_sketch.translate(0, 0, amount)
        elif isinstance(self, Landmark):
            self.fusion_landmark.translate(0, 0, amount)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def rotate_xyz(
        self, x: "str|float|Angle", y: "str|float|Angle", z: "str|float|Angle"
    ):
        print("rotate_xyz called:", x, y, z)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def rotate_x(self, rotation: "str|float|Angle"):
        from . import Part

        if isinstance(self, Part):
            self.fusion_body.rotate("x", rotation)
        else:
            self.fusion_sketch.rotate("x", rotation)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def rotate_y(self, rotation: "str|float|Angle"):
        from . import Part

        if isinstance(self, Part):
            self.fusion_body.rotate("y", rotation)
        else:
            self.fusion_sketch.rotate("y", rotation)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def rotate_z(self, rotation: "str|float|Angle"):
        from . import Part

        if isinstance(self, Part):
            self.fusion_body.rotate("z", rotation)
        else:
            self.fusion_sketch.rotate("z", rotation)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def get_bounding_box(self) -> "BoundaryBox":
        from . import Part

        if isinstance(self, Part):
            boundaryBox = self.fusion_body.get_bounding_box()
        else:
            boundaryBox = self.fusion_sketch.get_bounding_box()
        return boundaryBox

    @supported(SupportLevel.UNSUPPORTED)
    def get_dimensions(self) -> "Dimensions":
        print("get_dimensions called:")
        return Dimensions.from_point(Point.from_list_of_float_or_string([0, 0, 0]))
