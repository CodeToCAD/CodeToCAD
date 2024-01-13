# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from codetocad.interfaces import AnalyticsInterface

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Entity


class Analytics(AnalyticsInterface):
    def __init__(self):
        pass

    def measure_distance(
        self, entity1: EntityOrItsName, entity2: EntityOrItsName
    ) -> "Dimensions":
        print("measure_distance called:", entity1, entity2)
        return Dimensions.from_point(Point.from_list_of_float_or_string([0, 0, 0]))

    def measure_angle(
        self,
        entity1: EntityOrItsName,
        entity2: EntityOrItsName,
        pivot: Optional[EntityOrItsName] = None,
    ) -> "list[Angle]":
        print("measure_angle called:", entity1, entity2, pivot)
        return [Angle("90")]

    def get_world_pose(self, entity: EntityOrItsName) -> "list[float]":
        print("get_world_pose called:", entity)
        return [0.0]

    def get_bounding_box(self, entity_name: EntityOrItsName) -> "BoundaryBox":
        print("get_bounding_box called:", entity_name)
        return BoundaryBox(BoundaryAxis(0, 0), BoundaryAxis(0, 0), BoundaryAxis(0, 0))

    def get_dimensions(self, entity_name: EntityOrItsName) -> "Dimensions":
        print("get_dimensions called:", entity_name)
        return Dimensions.from_point(Point.from_list_of_float_or_string([0, 0, 0]))

    def log(self, message: str):
        print("log called:", message)
        return self
