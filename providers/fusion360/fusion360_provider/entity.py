from typing import Optional

from codetocad.interfaces import EntityInterface

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from typing import TYPE_CHECKING

from .fusion_actions.fusion_body import FusionBody

from .fusion_actions.fusion_sketch import FusionSketch

if TYPE_CHECKING:
    from . import Landmark


class Entity(EntityInterface):
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self, name: str, description: Optional[str] = None, native_instance=None
    ):
        self.name = name
        self.description = description
        self.native_instance = native_instance
        self.fusion_sketch = FusionSketch(name)
        self.fusion_body = FusionBody(name)

    @property
    def center(self):
        from . import Part, Sketch
        if isinstance(self, Part):
            return self.fusion_body.center
        if isinstance(self, Sketch):
            return self.fusion_sketch.center

    def is_exists(self) -> bool:
        print(
            "is_exists called:",
        )
        return True

    def rename(self, new_name: str, renamelinked_entities_and_landmarks: bool = True):
        print("rename called:", new_name, renamelinked_entities_and_landmarks)
        return self

    def delete(self, remove_children: bool = True):
        print("delete called:", remove_children)
        return self

    def is_visible(self) -> bool:
        print(
            "is_visible called:",
        )
        return True

    def set_visible(self, is_visible: bool):
        print("set_visible called:", is_visible)
        return self

    def apply(
        self,
        rotation: bool = True,
        scale: bool = True,
        location: bool = False,
        modifiers: bool = True,
    ):
        print("apply called:", rotation, scale, location, modifiers)
        return self

    def get_native_instance(self) -> object:
        print(
            "get_native_instance called:",
        )
        return "instance"

    def get_location_world(self) -> "Point":
        print(
            "get_location_world called:",
        )
        return Point.from_list_of_float_or_string([0, 0, 0])

    def get_location_local(self) -> "Point":
        print(
            "get_location_local called:",
        )
        return Point.from_list_of_float_or_string([0, 0, 0])

    def select(self):
        print(
            "select called:",
        )
        return self

    def translate_xyz(
        self,
        x: DimensionOrItsFloatOrStringValue,
        y: DimensionOrItsFloatOrStringValue,
        z: DimensionOrItsFloatOrStringValue,
    ):
        from . import Part
        if isinstance(self, Part):
            self.fusion_body.translate(x, y, z)
        else:
            self.fusion_sketch.translate(x, y, z)
        return self

    def translate_x(self, amount: DimensionOrItsFloatOrStringValue):
        from . import Part
        if isinstance(self, Part):
            self.fusion_body.translate(amount, 0, 0)
        else:
            self.fusion_sketch.translate(amount, 0, 0)
        return self

    def translate_y(self, amount: DimensionOrItsFloatOrStringValue):
        from . import Part
        if isinstance(self, Part):
            self.fusion_body.translate(0, amount, 0)
        else:
            self.fusion_sketch.translate(0, amount, 0)
        return self

    def translate_z(self, amount: DimensionOrItsFloatOrStringValue):
        from . import Part
        if isinstance(self, Part):
            self.fusion_body.translate(0, 0, amount)
        else:
            self.fusion_sketch.translate(0, 0, amount)
        return self

    def rotate_xyz(
        self,
        x: AngleOrItsFloatOrStringValue,
        y: AngleOrItsFloatOrStringValue,
        z: AngleOrItsFloatOrStringValue,
    ):
        print("rotate_xyz called:", x, y, z)
        return self

    def rotate_x(self, rotation: AngleOrItsFloatOrStringValue):
        from . import Part
        if isinstance(self, Part):
            self.fusion_body.rotate("x", rotation)
        else:
            self.fusion_sketch.rotate("x", rotation)
        return self

    def rotate_y(self, rotation: AngleOrItsFloatOrStringValue):
        from . import Part
        if isinstance(self, Part):
            self.fusion_body.rotate("y", rotation)
        else:
            self.fusion_sketch.rotate("y", rotation)
        return self

    def rotate_z(self, rotation: AngleOrItsFloatOrStringValue):
        from . import Part
        if isinstance(self, Part):
            self.fusion_body.rotate("z", rotation)
        else:
            self.fusion_sketch.rotate("z", rotation)
        return self

    def get_bounding_box(self) -> "BoundaryBox":
        print(
            "get_bounding_box called:",
        )
        return BoundaryBox(BoundaryAxis(0, 0), BoundaryAxis(0, 0), BoundaryAxis(0, 0))

    def get_dimensions(self) -> "Dimensions":
        print(
            "get_dimensions called:",
        )
        return Dimensions.from_point(Point.from_list_of_float_or_string([0, 0, 0]))

    def create_landmark(
        self,
        landmark_name: "str",
        x: DimensionOrItsFloatOrStringValue,
        y: DimensionOrItsFloatOrStringValue,
        z: DimensionOrItsFloatOrStringValue,
    ) -> "Landmark":
        from . import Landmark

        print("create_landmark called:", landmark_name, x, y, z)
        return Landmark("name", "parent")

    def get_landmark(self, landmark_name: PresetLandmarkOrItsName) -> "Landmark":
        from . import Landmark

        print("get_landmark called:", landmark_name)
        return Landmark("name", "parent")
