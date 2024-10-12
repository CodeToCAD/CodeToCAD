from codetocad.interfaces.part_interface import PartInterface
from codetocad.interfaces.sketch_interface import SketchInterface
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from typing import Self
from codetocad.interfaces.vertex_interface import VertexInterface
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.interfaces.edge_interface import EdgeInterface
from codetocad.interfaces.projectable_interface import ProjectableInterface
from codetocad.interfaces.booleanable_interface import BooleanableInterface
from codetocad.proxy.landmark import Landmark
from codetocad.proxy.part import Part
from providers.fusion360.fusion360_provider.fusion_actions.actions import sweep
from providers.fusion360.fusion360_provider.fusion_actions.base import (
    get_body,
    get_component,
)
from providers.fusion360.fusion360_provider.fusion_actions.fusion_body import FusionBody
from providers.fusion360.fusion360_provider.fusion_actions.fusion_sketch import (
    FusionSketch,
)
from codetocad.interfaces.wire_interface import WireInterface
from codetocad.interfaces.landmark_interface import LandmarkInterface
from providers.fusion360.fusion360_provider.entity import Entity
from codetocad.codetocad_types import *
from providers.fusion360.fusion360_provider.fusion_actions.modifiers import (
    make_loft,
    make_revolve,
)
from providers.fusion360.fusion360_provider.fusion_actions.normals import (
    calculate_normal,
)


class Wire(WireInterface, Entity):

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

    @supported(SupportLevel.SUPPORTED)
    def get_normal(self, flip: "bool| None" = False) -> "Point":
        vertices = self.get_vertices()
        num_vertices = len(vertices)
        normal = calculate_normal(
            vertices[0].location,
            vertices[int(num_vertices * 1 / 3)].location,
            vertices[int(num_vertices * 2 / 3)].location,
        )
        return normal

    @supported(SupportLevel.SUPPORTED)
    def get_vertices(self) -> "list[VertexInterface]":
        if len(self.edges) == 0:
            return []
        all_vertices = [self.edges[0].v1, self.edges[0].v2]
        for edge in self.edges:
            all_vertices.append(edge.v2)
        return all_vertices

    @supported(SupportLevel.PLANNED)
    def get_is_closed(self) -> bool:
        print("is_closed called:")
        return True

    @supported(SupportLevel.SUPPORTED)
    def loft(
        self, other: "WireInterface", new_part_name: "str| None" = None
    ) -> "PartInterface":
        new_name = new_part_name if new_part_name else self.parent_entity.name
        component = FusionSketch(self.parent_entity.name).component
        sketch = FusionSketch(self.parent_entity.name).instance
        other_sketch = FusionSketch(other.parent_entity.name).instance
        part = Part(new_name)
        part.fusion_body.instance = make_loft(component, sketch, other_sketch)
        return part

    @supported(SupportLevel.PLANNED)
    def create_landmark(
        self,
        landmark_name: "str",
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ) -> "LandmarkInterface":
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def get_landmark(self, landmark_name: "str|PresetLandmark") -> "LandmarkInterface":
        print("get_landmark called", f": {landmark_name}")
        return Landmark("name", "parent")

    @supported(SupportLevel.PLANNED)
    def union(
        self,
        other: "str|BooleanableInterface",
        delete_after_union: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def subtract(
        self,
        other: "str|BooleanableInterface",
        delete_after_subtract: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def intersect(
        self,
        other: "str|BooleanableInterface",
        delete_after_intersect: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED)
    def revolve(
        self,
        angle: "str|float|Angle",
        about_entity_or_landmark: "str|EntityInterface",
        axis: "str|int|Axis" = "z",
    ) -> "Part":
        if isinstance(about_entity_or_landmark, str):
            component = get_component(about_entity_or_landmark)
            if get_body(component, about_entity_or_landmark):
                fusionEntity = FusionBody(about_entity_or_landmark)
            else:
                fusionEntity = FusionSketch(about_entity_or_landmark)
        body = make_revolve(
            FusionSketch(self.name).component,
            FusionSketch(self.name).instance,
            angle,
            axis,
            fusionEntity.center,
        )
        part = Part(body.name)
        part.fusion_body.instance = body
        return part

    @supported(SupportLevel.PLANNED)
    def twist(
        self,
        angle: "str|float|Angle",
        screw_pitch: "str|float|Dimension",
        iterations: "int" = 1,
        axis: "str|int|Axis" = "z",
    ):
        print("twist called:", angle, screw_pitch, iterations, axis)
        return self

    @supported(SupportLevel.SUPPORTED)
    def extrude(self, length: "str|float|Dimension") -> "PartInterface":
        length = Dimension.from_dimension_or_its_float_or_string_value(length, None)
        body = FusionSketch(self.name).extrude(length.value)
        part = Part(body.name)
        return part

    @supported(SupportLevel.PARTIAL, "fill_caps is not supported")
    def sweep(
        self, profile_name_or_instance: "str|WireInterface", fill_cap: "bool" = True
    ) -> "Part":
        fusion_sketch = FusionSketch(profile_name_or_instance)
        name = sweep(
            FusionSketch(self.name).component,
            FusionSketch(self.name).instance,
            fusion_sketch.component,
            fusion_sketch.instance,
        )
        return Part(name)

    @supported(SupportLevel.PLANNED)
    def offset(self, radius: "str|float|Dimension"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def profile(self, profile_curve_name: "str|WireInterface|SketchInterface"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def get_edges(self) -> "list[EdgeInterface]":
        raise NotImplementedError()
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def remesh(self, strategy: "str", amount: "float"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def subdivide(self, amount: "float"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def decimate(self, amount: "float"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def create_from_vertices(
        self,
        points: "list[str|list[str]|list[float]|list[Dimension]|Point|VertexInterface]",
        options: "SketchOptions| None" = None,
    ) -> Self:
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def create_point(
        self,
        point: "str|list[str]|list[float]|list[Dimension]|Point",
        options: "SketchOptions| None" = None,
    ) -> Self:
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def create_line(
        self,
        length: "str|float|Dimension",
        angle: "str|float|Angle",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        options: "SketchOptions| None" = None,
    ) -> Self:
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def create_line_to(
        self,
        to: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        options: "SketchOptions| None" = None,
    ) -> Self:
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def create_arc(
        self,
        end_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface",
        radius: "str|float|Dimension",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        flip: "bool| None" = False,
        options: "SketchOptions| None" = None,
    ) -> Self:
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
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

    @supported(SupportLevel.PLANNED)
    def linear_pattern(
        self,
        instance_count: "int",
        offset: "str|float|Dimension",
        direction_axis: "str|int|Axis" = "z",
    ):
        print("linear_pattern called:", instance_count, offset, direction_axis)
        return self

    @supported(SupportLevel.PLANNED)
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

    @supported(SupportLevel.PLANNED)
    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":
        raise NotImplementedError()
        return self
