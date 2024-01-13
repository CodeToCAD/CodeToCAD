# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from codetocad.interfaces import EntityInterface

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from typing import TYPE_CHECKING

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
        print("translate_xyz called:", x, y, z)
        return self

    def translate_x(self, amount: DimensionOrItsFloatOrStringValue):
        print("translate_x called:", amount)
        return self

    def translate_y(self, amount: DimensionOrItsFloatOrStringValue):
        print("translate_y called:", amount)
        return self

    def translate_z(self, amount: DimensionOrItsFloatOrStringValue):
        print("translate_z called:", amount)
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
        print("rotate_x called:", rotation)
        return self

    def rotate_y(self, rotation: AngleOrItsFloatOrStringValue):
        print("rotate_y called:", rotation)
        return self

    def rotate_z(self, rotation: AngleOrItsFloatOrStringValue):
        print("rotate_z called:", rotation)
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
        landmark_name: str,
        x: DimensionOrItsFloatOrStringValue,
        y: DimensionOrItsFloatOrStringValue,
        z: DimensionOrItsFloatOrStringValue,
    ) -> "Landmark":
        print("create_landmark called:", landmark_name, x, y, z)
        from . import Landmark

        return Landmark("name", "parent")

    def get_landmark(self, landmark_name: PresetLandmarkOrItsName) -> "Landmark":
        print("get_landmark called:", landmark_name)
        from . import Landmark

        return Landmark("name", "parent")
