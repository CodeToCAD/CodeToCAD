from typing import Optional

from codetocad.interfaces import EdgeInterface

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from . import Entity

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Vertex
    from . import Sketch


class Edge(Entity, EdgeInterface):
    def mirror(
        self,
        mirror_across_entity: EntityOrItsName,
        axis: AxisOrItsIndexOrItsName,
        resulting_mirrored_entity_name: Optional[str] = None,
    ):
        return self

    def linear_pattern(
        self,
        instance_count: "int",
        offset: DimensionOrItsFloatOrStringValue,
        direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        return self

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: AngleOrItsFloatOrStringValue,
        center_entity_or_landmark: EntityOrItsName,
        normal_direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        return self

    def remesh(self, strategy: str, amount: float):
        return self

    def subdivide(self, amount: float):
        return self

    def decimate(self, amount: float):
        return self

    def project(self, project_onto: "Sketch") -> "Projectable":
        raise NotImplementedError()

    v1: "Vertex"
    v2: "Vertex"
    parent_entity: Optional[EntityOrItsName] = None
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self,
        v1: "Vertex",
        v2: "Vertex",
        name: str,
        parent_entity: Optional[EntityOrItsName] = None,
        description: Optional[str] = None,
        native_instance=None,
    ):
        self.v1 = v1
        self.v2 = v2
        self.parent_entity = parent_entity
        self.name = name
        self.description = description
        self.native_instance = native_instance

    def offset(self, distance: DimensionOrItsFloatOrStringValue) -> "Edge":
        raise NotImplementedError()

    def fillet(self, other_edge: "Edge", amount: AngleOrItsFloatOrStringValue):
        return self

    def set_is_construction(self, is_construction: bool):
        return self

    def get_is_construction(self) -> bool:
        raise NotImplementedError()



"""
sample native_instance data
{
        "btType": "BTMSketchCurveSegment-155",
        "startPointId": "",
        "endPointId": "",
        "offsetCurveExtensions": [],
        "startParam": 0,
        "endParam": 1,
        "geometry": {
          "btType": "BTCurveGeometryLine-117",
          "pntX": 15,
          "pntY": 15,
          "dirX": 10,
          "dirY": 10
        },
        "centerId": "",
        "internalIds": [],
        "parameters": [],
        "isConstruction": false,
        "isFromSplineHandle": false,
        "isFromEndpointSplineHandle": false,
        "isFromSplineControlPolygon": false,
        "nodeId": "Mkn74T5u3XMgmy8T7",
        "namespace": "",
        "entityId": ""
}
"""