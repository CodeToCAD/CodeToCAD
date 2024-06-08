from typing import Optional
from typing import Self
from codetocad.interfaces.vertex_interface import VertexInterface
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.interfaces.edge_interface import EdgeInterface
from codetocad.interfaces.projectable_interface import ProjectableInterface
from codetocad.interfaces.booleanable_interface import BooleanableInterface
from codetocad.proxy.edge import Edge
from codetocad.proxy.vertex import Vertex
from codetocad.proxy.landmark import Landmark
from codetocad.proxy.part import Part
from providers.fusion360.fusion360_provider.sketch import Sketch
from codetocad.interfaces.wire_interface import WireInterface
from codetocad.interfaces.landmark_interface import LandmarkInterface
from providers.fusion360.fusion360_provider.entity import Entity
from providers.fusion360.fusion360_provider.vertex import Vertex
from providers.fusion360.fusion360_provider.landmark import Landmark
from providers.fusion360.fusion360_provider.part import Part
from providers.fusion360.fusion360_provider.edge import Edge
from codetocad.codetocad_types import *
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
        mirror_across_entity: "str|EntityInterface",
        axis: "str|int|Axis",
        resulting_mirrored_entity_name: "str| None" = None,
    ):
        print(
            "mirror called:", mirror_across_entity, axis, resulting_mirrored_entity_name
        )
        return self

    def linear_pattern(
        self,
        instance_count: "int",
        offset: "str|float|Dimension",
        direction_axis: "str|int|Axis" = "z",
    ):
        print("linear_pattern called:", instance_count, offset, direction_axis)
        return self

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "str|float|Angle",
        center_entity_or_landmark: "str|EntityInterface",
        normal_direction_axis: "str|int|Axis" = "z",
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
    parent_entity: Optional[str | Entity] = None
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self,
        name: "str",
        edges: "list[EdgeInterface]",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "str|EntityInterface| None" = None,
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
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ) -> "LandmarkInterface":
        print("create_landmark called", f": {landmark_name}, {x}, {y}, {z}")
        return Landmark("name", "parent")

    def get_landmark(self, landmark_name: "str|PresetLandmark") -> "LandmarkInterface":
        print("get_landmark called", f": {landmark_name}")
        return Landmark("name", "parent")

    def union(
        self,
        other: "str|BooleanableInterface",
        delete_after_union: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        print("union called", f": {other}, {delete_after_union}, {is_transfer_data}")
        return self

    def subtract(
        self,
        other: "str|BooleanableInterface",
        delete_after_subtract: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        print(
            "subtract called", f": {other}, {delete_after_subtract}, {is_transfer_data}"
        )
        return self

    def intersect(
        self,
        other: "str|BooleanableInterface",
        delete_after_intersect: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        print(
            "intersect called",
            f": {other}, {delete_after_intersect}, {is_transfer_data}",
        )
        return self

    def revolve(
        self,
        angle: "str|float|Angle",
        about_entity_or_landmark: "str|EntityInterface",
        axis: "str|int|Axis" = "z",
    ) -> "Part":
        from . import Part

        if isinstance(about_entity_or_landmark, str):
            component = get_component(about_entity_or_landmark)
            if get_body(component, about_entity_or_landmark):
                about_entity_or_landmark = Part(about_entity_or_landmark).fusion_body
            else:
                about_entity_or_landmark = Sketch(
                    about_entity_or_landmark
                ).fusion_sketch
        body = make_revolve(
            self.fusion_sketch.component,
            self.fusion_sketch.instance,
            angle,
            axis,
            start=about_entity_or_landmark.center,
        )
        part = Part(body.name)
        part.fusion_body.instance = body
        return part

    def twist(
        self,
        angle: "str|float|Angle",
        screw_pitch: "str|float|Dimension",
        iterations: "int" = 1,
        axis: "str|int|Axis" = "z",
    ):
        print("twist called:", angle, screw_pitch, iterations, axis)
        return self

    def extrude(self, length: "str|float|Dimension") -> "Part":
        from . import Part

        length = Dimension.from_dimension_or_its_float_or_string_value(length, None)
        body = self.fusion_sketch.extrude(length.value)
        part = Part(body.name)
        part.fusion_body.instance = body
        return part

    def sweep(
        self, profile_name_or_instance: "str|WireInterface", fill_cap: "bool" = True
    ) -> "Part":
        from . import Part

        name = sweep(
            self.fusion_sketch.component,
            self.fusion_sketch.instance,
            profile_name_or_instance.fusion_sketch.component,
            profile_name_or_instance.fusion_sketch.instance,
        )
        return Part(name)

    def offset(self, radius: "str|float|Dimension"):
        print("offset called:", radius)
        return self

    def profile(self, profile_curve_name: "str"):
        print("profile called:", profile_curve_name)
        return self

    def get_edges(self) -> "list[EdgeInterface]":
        print("get_edges called")
        return [
            Edge(
                v1=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
                v2=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
                name="an edge",
            )
        ]

    def remesh(self, strategy: "str", amount: "float"):
        print("remesh called", f": {strategy}, {amount}")
        return self

    def subdivide(self, amount: "float"):
        print("subdivide called", f": {amount}")
        return self

    def decimate(self, amount: "float"):
        print("decimate called", f": {amount}")
        return self

    def create_from_vertices(
        self,
        points: "list[str|list[str]|list[float]|list[Dimension]|Point|VertexInterface]",
        options: "SketchOptions| None" = None,
    ) -> Self:
        print("create_from_vertices called", f": {points}, {options}")
        return self

    def create_point(
        self,
        point: "str|list[str]|list[float]|list[Dimension]|Point",
        options: "SketchOptions| None" = None,
    ) -> Self:
        print("create_point called", f": {point}, {options}")
        return self

    def create_line(
        self,
        length: "str|float|Dimension",
        angle: "str|float|Angle",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        options: "SketchOptions| None" = None,
    ) -> Self:
        print("create_line called", f": {length}, {angle}, {start_at}, {options}")
        return self

    def create_line_to(
        self,
        to: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        options: "SketchOptions| None" = None,
    ) -> Self:
        print("create_line_to called", f": {to}, {start_at}, {options}")
        return self

    def create_arc(
        self,
        end_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface",
        radius: "str|float|Dimension",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        flip: "bool| None" = False,
        options: "SketchOptions| None" = None,
    ) -> Self:
        print(
            "create_arc called", f": {end_at}, {radius}, {start_at}, {flip}, {options}"
        )
        return self
