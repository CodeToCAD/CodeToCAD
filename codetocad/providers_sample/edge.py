# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

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
    from . import Entity


class Edge(Entity, EdgeInterface):
    def mirror(
        self,
        mirror_across_entity: EntityOrItsName,
        axis: AxisOrItsIndexOrItsName,
        resulting_mirrored_entity_name: Optional[str] = None,
    ):
        print(
            "mirror called:", mirror_across_entity, axis, resulting_mirrored_entity_name
        )
        return self

    def linear_pattern(
        self,
        instance_count: "int",
        offset: DimensionOrItsFloatOrStringValue,
        direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        print("linear_pattern called:", instance_count, offset, direction_axis)
        return self

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: AngleOrItsFloatOrStringValue,
        center_entity_or_landmark: EntityOrItsName,
        normal_direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        print(
            "circular_pattern called:",
            instance_count,
            separation_angle,
            center_entity_or_landmark,
            normal_direction_axis,
        )
        return self

    def remesh(self, strategy: str, amount: float):
        print("remesh called:", strategy, amount)
        return self

    def subdivide(self, amount: float):
        print("subdivide called:", amount)
        return self

    def decimate(self, amount: float):
        print("decimate called:", amount)
        return self

    def project(self, project_onto: "Sketch") -> "Projectable":
        print("project called:", project_onto)
        from . import Sketch

        return Sketch("a projected sketch")

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
        print("offset called:", distance)
        from . import Vertex

        from . import Edge

        return Edge(
            v1=Vertex(Point.from_list_of_float_or_string([0, 0, 0]), "a vertex"),
            v2=Vertex(Point.from_list_of_float_or_string([0, 0, 0]), "a vertex"),
            name="an edge",
        )

    def fillet(self, other_edge: "Edge", amount: AngleOrItsFloatOrStringValue):
        print("fillet called:", other_edge, amount)
        return self

    def set_is_construction(self, is_construction: bool):
        print("set_is_construction called:", is_construction)
        return self

    def get_is_construction(self) -> bool:
        print(
            "get_is_construction called:",
        )
        return True
