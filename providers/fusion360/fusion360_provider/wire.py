from typing import Optional

from codetocad.interfaces import WireInterface, ProjectableInterface

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *
from providers.fusion360.fusion360_provider.fusion_actions.modifiers import make_loft
from providers.fusion360.fusion360_provider.fusion_actions.normals import calculate_normal


from . import Entity

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Edge
    from . import Entity
    from . import Vertex
    from . import Part


class Wire(Entity, WireInterface):
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

    def project(self, project_onto: "Sketch") -> "ProjectableInterface":
        from . import Sketch

        print("project called:", project_onto)
        return Sketch("a projected sketch")

    edges: "list[Edge]"
    parent_entity: Optional[EntityOrItsName] = None
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self,
        edges: "list[Edge]",
        name: str,
        parent_entity: Optional[EntityOrItsName] = None,
        description: Optional[str] = None,
        native_instance=None,
    ):
        if isinstance(parent_entity, str):
            parent_entity = Entity(parent_entity)
        self.edges = edges
        self.parent_entity = parent_entity
        self.name = name
        self.description = description
        self.native_instance = native_instance

    def clone(
        self, new_name: str, new_parent: Optional[SketchOrItsName] = None
    ) -> "Wire":
        from . import Sketch
        parent = new_parent or self.parent_entity

        if isinstance(parent, str):
            parent = Sketch(parent)

        if isinstance(parent, Sketch):
            points = self.get_vertices()
            points = [point.location for point in points]
            points.append(points[0].copy())
            wire = parent.create_from_vertices(points)
            wire.name = new_name
            return wire

        raise Exception(f"Parent of type {type(parent)} is not supported.")

    def get_normal(self, flip: Optional[bool] = False) -> "Point":
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
        print(
            "is_closed called:",
        )
        return True

    def loft(self, other: "Wire", new_part_name: Optional[str] = None) -> "Part":
        new_name = new_part_name if new_part_name else self.parent_entity.name

        component = self.parent_entity.fusion_sketch.component
        sketch = self.parent_entity.fusion_sketch.instance
        other_sketch = other.parent_entity.fusion_sketch.instance

        from . import Part

        part = Part(new_name)

        part.fusion_body.instance = make_loft(
            component,
            sketch,
            other_sketch,
        )

        return part
