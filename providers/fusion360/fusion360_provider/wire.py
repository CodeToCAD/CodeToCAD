from typing import Optional
from codetocad.interfaces.wire_interface import WireInterface

from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.interfaces.vertex_interface import VertexInterface
from codetocad.interfaces.landmark_interface import LandmarkInterface
from codetocad.interfaces.part_interface import PartInterface
from codetocad.interfaces.edge_interface import EdgeInterface
from providers.fusion360.fusion360_provider.entity import Entity
from providers.fusion360.fusion360_provider.vertex import Vertex
from providers.fusion360.fusion360_provider.landmark import Landmark
from providers.fusion360.fusion360_provider.part import Part
from providers.fusion360.fusion360_provider.edge import Edge

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *
from providers.fusion360.fusion360_provider.fusion_actions.modifiers import make_loft
from providers.fusion360.fusion360_provider.fusion_actions.normals import (
    calculate_normal,
)
from . import Entity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Edge
    from . import Entity
    from . import Vertex
    from . import Part


class Wire(WireInterface, Entity):
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

    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":
        from . import Sketch

        print("project called:", project_from)
        return Sketch("a projected sketch")

    edges: "list[Edge]"
    parent_entity: Optional[EntityOrItsName] = None
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self,
        name: "str",
        edges: "list[Edge]",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "EntityOrItsName| None" = None,
    ):
        if isinstance(parent_entity, str):
            parent_entity = Entity(parent_entity)
        self.edges = edges
        self.parent_entity = parent_entity
        self.name = name
        self.description = description
        self.native_instance = native_instance

    def get_normal(self, flip: "bool| None" = False) -> "Point":
        vertices = self.get_vertices()
        num_vertices = len(vertices)
        normal = calculate_normal(
            vertices[0].location,
            vertices[int(num_vertices * 1 / 3)].location,
            vertices[int(num_vertices * 2 / 3)].location,
        )
        return normal

    def get_vertices(self) -> "list[Vertex]":
        if len(self.edges) == 0:
            return []
        all_vertices = [self.edges[0].v1, self.edges[0].v2]
        for edge in self.edges:
            all_vertices.append(edge.v2)
        return all_vertices

    def get_is_closed(self) -> bool:
        print("is_closed called:")
        return True

    def loft(self, other: "WireInterface", new_part_name: "str| None" = None) -> "Part":
        new_name = new_part_name if new_part_name else self.parent_entity.name
        component = self.parent_entity.fusion_sketch.component
        sketch = self.parent_entity.fusion_sketch.instance
        other_sketch = other.parent_entity.fusion_sketch.instance
        from . import Part

        part = Part(new_name)
        part.fusion_body.instance = make_loft(component, sketch, other_sketch)
        return part

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

    def union(
        self,
        other: "BooleanableOrItsName",
        delete_after_union: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        print("union called", f": {other}, {delete_after_union}, {is_transfer_data}")
        return self

    def subtract(
        self,
        other: "BooleanableOrItsName",
        delete_after_subtract: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        print(
            "subtract called", f": {other}, {delete_after_subtract}, {is_transfer_data}"
        )
        return self

    def intersect(
        self,
        other: "BooleanableOrItsName",
        delete_after_intersect: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        print(
            "intersect called",
            f": {other}, {delete_after_intersect}, {is_transfer_data}",
        )
        return self
