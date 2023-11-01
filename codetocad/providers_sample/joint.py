# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from codetocad.interfaces import JointInterface

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Entity


class Joint(JointInterface):
    entity1: EntityOrItsName
    entity2: EntityOrItsName

    def __init__(self, entity1: EntityOrItsName, entity2: EntityOrItsName):
        self.entity1 = entity1
        self.entity2 = entity2

    def translate_landmark_onto_another(self):
        return self

    def pivot(self):
        return self

    def gear_ratio(self, ratio: float):
        return self

    def limit_location_xyz(
        self,
        x: Optional[DimensionOrItsFloatOrStringValue] = None,
        y: Optional[DimensionOrItsFloatOrStringValue] = None,
        z: Optional[DimensionOrItsFloatOrStringValue] = None,
    ):
        return self

    def limit_location_x(
        self,
        min: Optional[DimensionOrItsFloatOrStringValue] = None,
        max: Optional[DimensionOrItsFloatOrStringValue] = None,
    ):
        return self

    def limit_location_y(
        self,
        min: Optional[DimensionOrItsFloatOrStringValue] = None,
        max: Optional[DimensionOrItsFloatOrStringValue] = None,
    ):
        return self

    def limit_location_z(
        self,
        min: Optional[DimensionOrItsFloatOrStringValue] = None,
        max: Optional[DimensionOrItsFloatOrStringValue] = None,
    ):
        return self

    def limit_rotation_xyz(
        self,
        x: Optional[AngleOrItsFloatOrStringValue] = None,
        y: Optional[AngleOrItsFloatOrStringValue] = None,
        z: Optional[AngleOrItsFloatOrStringValue] = None,
    ):
        return self

    def limit_rotation_x(
        self,
        min: Optional[AngleOrItsFloatOrStringValue] = None,
        max: Optional[AngleOrItsFloatOrStringValue] = None,
    ):
        return self

    def limit_rotation_y(
        self,
        min: Optional[AngleOrItsFloatOrStringValue] = None,
        max: Optional[AngleOrItsFloatOrStringValue] = None,
    ):
        return self

    def limit_rotation_z(
        self,
        min: Optional[AngleOrItsFloatOrStringValue] = None,
        max: Optional[AngleOrItsFloatOrStringValue] = None,
    ):
        return self
