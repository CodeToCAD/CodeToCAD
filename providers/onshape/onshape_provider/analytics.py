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
        raise NotImplementedError()

    def measure_angle(
        self,
        entity1: EntityOrItsName,
        entity2: EntityOrItsName,
        pivot: Optional[EntityOrItsName] = None,
    ) -> "list[Angle]":
        raise NotImplementedError()

    def get_world_pose(self, entity: EntityOrItsName) -> "list[float]":
        raise NotImplementedError()

    def get_bounding_box(self, entity_name: EntityOrItsName) -> "BoundaryBox":
        raise NotImplementedError()

    def get_dimensions(self, entity_name: EntityOrItsName) -> "Dimensions":
        raise NotImplementedError()

    def log(self, message: str):
        return self
