from typing import Optional
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.interfaces.vertex_interface import VertexInterface
from codetocad.interfaces.landmark_interface import LandmarkInterface
from providers.fusion360.fusion360_provider.entity import Entity
from providers.fusion360.fusion360_provider.vertex import Vertex
from providers.fusion360.fusion360_provider.landmark import Landmark
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


class Edge(EdgeInterface, Entity):
    def mirror(
        self,
        mirror_across_entity: "EntityOrItsName",
        axis: "AxisOrItsIndexOrItsName",
        resulting_mirrored_entity_name: "str| None" = None,
    ):
        print(
            "mirror called:", mirror_across_entity, axis, resulting_mirrored_entity_name
        )
        return self

    def linear_pattern(
        self,
        instance_count: "int",
        offset: "DimensionOrItsFloatOrStringValue",
        direction_axis: "AxisOrItsIndexOrItsName" = "z",
    ):
        print("linear_pattern called:", instance_count, offset, direction_axis)
        return self

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "AngleOrItsFloatOrStringValue",
        center_entity_or_landmark: "EntityOrItsName",
        normal_direction_axis: "AxisOrItsIndexOrItsName" = "z",
    ):
        print(
            "circular_pattern called:",
            instance_count,
            separation_angle,
            center_entity_or_landmark,
            normal_direction_axis,
        )
        return self

    def remesh(self, strategy: "str", amount: "float"):
        print("remesh called:", strategy, amount)
        return self

    def subdivide(self, amount: "float"):
        print("subdivide called:", amount)
        return self

    def decimate(self, amount: "float"):
        print("decimate called:", amount)
        return self

    def project(self, project_onto: "ProjectableInterface") -> "Projectable":
        from . import Sketch

        print("project called:", project_onto)
        return Sketch("a projected sketch")

    v1: "Vertex"
    v2: "Vertex"
    parent_entity: Optional[EntityOrItsName] = None
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self,
        name: "str",
        v1: "VertexInterface",
        v2: "VertexInterface",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "EntityOrItsName| None" = None,
    ):
        self.v1 = v1
        self.v2 = v2
        self.parent_entity = parent_entity
        self.name = name
        self.description = description
        self.native_instance = native_instance

    def offset(self, distance: "DimensionOrItsFloatOrStringValue") -> "Edge":
        print("offset called:", distance)
        return Edge.get_dummy_edge()

    def fillet(
        self, other_edge: "EdgeInterface", amount: "AngleOrItsFloatOrStringValue"
    ):
        print("fillet called:", other_edge, amount)
        return self

    def set_is_construction(self, is_construction: "bool"):
        print("set_is_construction called:", is_construction)
        return self

    def get_is_construction(self) -> bool:
        print("get_is_construction called:")
        return True

    def create_landmark(
        self,
        landmark_name: "str",
        x: "DimensionOrItsFloatOrStringValue",
        y: "DimensionOrItsFloatOrStringValue",
        z: "DimensionOrItsFloatOrStringValue",
    ) -> "LandmarkInterface":
        print("create_landmark called", f": {landmark_name}, {x}, {y}, {z}")
        return Landmark("name", "parent")

    def get_landmark(
        self, landmark_name: "PresetLandmarkOrItsName"
    ) -> "LandmarkInterface":
        print("get_landmark called", f": {landmark_name}")
        return Landmark("name", "parent")
