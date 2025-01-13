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
from codetocad.utilities.normals import calculate_normal


class Wire(WireInterface, Entity):

    def __init__(self, native_instance: "Any"):
        self.name = name
        self.description = description
        self.native_instance = native_instance

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_normal(self, flip: "bool| None" = False) -> "Point":
        vertices = self.get_vertices()
        num_vertices = len(vertices)
        normal = calculate_normal(
            vertices[0].location,
            vertices[int(num_vertices * 1 / 3)].location,
            vertices[int(num_vertices * 2 / 3)].location,
        )
        return normal

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_vertices(self) -> "list[VertexInterface]":
        edges = self.get_edges()
        if len(edges) == 0:
            return []
        all_vertices = [edges[0].v1, edges[0].v2]
        for edge in edges:
            all_vertices.append(edge.v2)
        return all_vertices

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_is_closed(self) -> bool:
        print("is_closed called:")
        return True

    @supported(SupportLevel.SUPPORTED, notes="")
    def loft(
        self,
        other: "WireInterface",
        union_connecting_parts: "bool| None" = True,
        new_name: "str| None" = None,
    ) -> "PartInterface":
        new_name = new_name if new_name else self.parent.name
        component = FusionSketch(self.parent.name).component
        sketch = FusionSketch(self.parent.name).instance
        other_sketch = FusionSketch(other.parent.name).instance
        part = Part(new_name)
        part.fusion_body.instance = make_loft(component, sketch, other_sketch)
        return part

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_landmark(
        self,
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
        landmark_name: "str| None" = None,
    ) -> "LandmarkInterface":
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_landmark(self, landmark_name: "str|PresetLandmark") -> "LandmarkInterface":
        print("get_landmark called", f": {landmark_name}")
        return Landmark("name", "parent")

    @supported(SupportLevel.SUPPORTED, notes="")
    def union(
        self,
        other: "BooleanableInterface",
        delete_after_union: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def subtract(
        self,
        other: "BooleanableInterface",
        delete_after_subtract: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def intersect(
        self,
        other: "BooleanableInterface",
        delete_after_intersect: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def revolve(
        self,
        angle: "str|float|Angle",
        about_entity_or_landmark: "EntityInterface",
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

    @supported(SupportLevel.SUPPORTED, notes="")
    def twist(
        self,
        angle: "str|float|Angle",
        screw_pitch: "str|float|Dimension",
        iterations: "int" = 1,
        axis: "str|int|Axis" = "z",
    ):
        print("twist called:", angle, screw_pitch, iterations, axis)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def extrude(self, length: "str|float|Dimension") -> "PartInterface":
        length = Dimension.from_dimension_or_its_float_or_string_value(length, None)
        body = FusionSketch(self.name).extrude(length.value)
        part = Part(body.name)
        return part

    @supported(SupportLevel.SUPPORTED, notes="")
    def sweep(self, profile: "WireInterface", fill_cap: "bool" = True) -> "Part":
        fusion_sketch = FusionSketch(profile)
        name = sweep(
            FusionSketch(self.name).component,
            FusionSketch(self.name).instance,
            fusion_sketch.component,
            fusion_sketch.instance,
        )
        return Part(name)

    @supported(SupportLevel.SUPPORTED, notes="")
    def offset(self, radius: "str|float|Dimension"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def profile(self, profile_curve: "WireInterface|SketchInterface"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_edges(self) -> "list[EdgeInterface]":
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def remesh(self, strategy: "str", amount: "float"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def subdivide(self, amount: "float"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def decimate(self, amount: "float"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_from_vertices(
        self,
        points: "list[str|list[str]|list[float]|list[Dimension]|Point|VertexInterface]",
    ) -> Self:
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_point(
        self, point: "str|list[str]|list[float]|list[Dimension]|Point"
    ) -> Self:
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_line(
        self,
        length: "str|float|Dimension",
        angle: "str|float|Angle",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
    ) -> Self:
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_line_to(
        self,
        to: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
    ) -> Self:
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_arc(
        self,
        end_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface",
        radius: "str|float|Dimension",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        flip: "bool| None" = False,
    ) -> Self:
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def mirror(
        self,
        mirror_across_entity: "EntityInterface",
        axis: "str|int|Axis",
        separate_resulting_entity: "bool| None" = False,
    ):
        print("mirror called:", mirror_across_entity, axis, separate_resulting_entity)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def linear_pattern(
        self,
        instance_count: "int",
        offset: "str|float|Dimension",
        direction_axis: "str|int|Axis" = "z",
    ):
        print("linear_pattern called:", instance_count, offset, direction_axis)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "str|float|Angle",
        center_entity_or_landmark: "EntityInterface",
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

    @supported(SupportLevel.SUPPORTED, notes="")
    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_parent(self) -> "EntityInterface":
        print("get_parent called")
        return __import__("codetocad").Part("an entity")
