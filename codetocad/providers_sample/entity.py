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
        raise NotImplementedError()

    def rename(self, new_name: str, renamelinked_entities_and_landmarks: bool = True):
        return self

    def delete(self, remove_children: bool):
        return self

    def is_visible(self) -> bool:
        raise NotImplementedError()

    def set_visible(self, is_visible: bool):
        return self

    def apply(
        self,
        rotation: bool = True,
        scale: bool = True,
        location: bool = False,
        modifiers: bool = True,
    ):
        return self

    def get_native_instance(self) -> object:
        raise NotImplementedError()

    def get_location_world(self) -> "Point":
        raise NotImplementedError()

    def get_location_local(self) -> "Point":
        raise NotImplementedError()

    def select(self):
        return self

    def export(self, file_path: str, overwrite: bool = True, scale: float = 1.0):
        return self

    def translate_xyz(
        self,
        x: DimensionOrItsFloatOrStringValue,
        y: DimensionOrItsFloatOrStringValue,
        z: DimensionOrItsFloatOrStringValue,
    ):
        return self

    def translate_x(self, amount: DimensionOrItsFloatOrStringValue):
        return self

    def translate_y(self, amount: DimensionOrItsFloatOrStringValue):
        return self

    def translate_z(self, amount: DimensionOrItsFloatOrStringValue):
        return self

    def scale_xyz(
        self,
        x: DimensionOrItsFloatOrStringValue,
        y: DimensionOrItsFloatOrStringValue,
        z: DimensionOrItsFloatOrStringValue,
    ):
        return self

    def scale_x(self, scale: DimensionOrItsFloatOrStringValue):
        return self

    def scale_y(self, scale: DimensionOrItsFloatOrStringValue):
        return self

    def scale_z(self, scale: DimensionOrItsFloatOrStringValue):
        return self

    def scale_x_by_factor(self, scale_factor: float):
        return self

    def scale_y_by_factor(self, scale_factor: float):
        return self

    def scale_z_by_factor(self, scale_factor: float):
        return self

    def scale_keep_aspect_ratio(
        self, scale: DimensionOrItsFloatOrStringValue, axis: AxisOrItsIndexOrItsName
    ):
        return self

    def rotate_xyz(
        self,
        x: AngleOrItsFloatOrStringValue,
        y: AngleOrItsFloatOrStringValue,
        z: AngleOrItsFloatOrStringValue,
    ):
        return self

    def rotate_x(self, rotation: AngleOrItsFloatOrStringValue):
        return self

    def rotate_y(self, rotation: AngleOrItsFloatOrStringValue):
        return self

    def rotate_z(self, rotation: AngleOrItsFloatOrStringValue):
        return self

    def get_bounding_box(self) -> "BoundaryBox":
        raise NotImplementedError()

    def get_dimensions(self) -> "Dimensions":
        raise NotImplementedError()

    def create_landmark(
        self,
        landmark_name: str,
        x: DimensionOrItsFloatOrStringValue,
        y: DimensionOrItsFloatOrStringValue,
        z: DimensionOrItsFloatOrStringValue,
    ) -> "LandmarkInterface":
        raise NotImplementedError()

    def get_landmark(
        self, landmark_name: PresetLandmarkOrItsName
    ) -> "LandmarkInterface":
        raise NotImplementedError()
