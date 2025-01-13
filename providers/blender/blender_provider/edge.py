from typing import Self
from codetocad.proxy.vertex import Vertex
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.utilities.override import override
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.proxy.landmark import Landmark
from codetocad.interfaces.edge_interface import EdgeInterface
from codetocad.interfaces.vertex_interface import VertexInterface
from codetocad.interfaces.landmark_interface import LandmarkInterface
from providers.blender.blender_provider.entity import Entity
from codetocad.codetocad_types import *
from codetocad.interfaces.projectable_interface import ProjectableInterface


class Edge(EdgeInterface, Entity):

    def __init__(self, native_instance: "Any"):
        self.native_instance = native_instance

    @supported(SupportLevel.SUPPORTED, notes="")
    def offset(self, distance: "str|float|Dimension") -> "Edge":
        raise NotImplementedError()

    @supported(SupportLevel.SUPPORTED, notes="")
    def fillet(self, other_edge: "EdgeInterface", amount: "str|float|Angle"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_is_construction(self, is_construction: "bool"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_is_construction(self) -> bool:
        raise NotImplementedError()

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
    def mirror(
        self,
        mirror_across_entity: "EntityInterface",
        axis: "str|int|Axis",
        separate_resulting_entity: "bool| None" = False,
    ):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def linear_pattern(
        self,
        instance_count: "int",
        offset: "str|float|Dimension",
        direction_axis: "str|int|Axis" = "z",
    ):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "str|float|Angle",
        center_entity_or_landmark: "EntityInterface",
        normal_direction_axis: "str|int|Axis" = "z",
    ):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_landmark(
        self,
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
        landmark_name: "str| None" = None,
    ) -> "LandmarkInterface":
        raise NotImplementedError()
        print("create_landmark called", f": {landmark_name}, {x}, {y}, {z}")
        return Landmark("name", "parent")

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_landmark(self, landmark_name: "str|PresetLandmark") -> "LandmarkInterface":
        raise NotImplementedError()
        print("get_landmark called", f": {landmark_name}")
        return Landmark("name", "parent")

    @override
    @supported(SupportLevel.SUPPORTED, notes="")
    def translate_xyz(
        self,
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ) -> Self:
        self.v1.translate_xyz(x, y, z)
        self.v2.translate_xyz(x, y, z)
        return self

    @override
    @supported(SupportLevel.SUPPORTED, notes="")
    def translate_x(self, amount: "str|float|Dimension") -> Self:
        return self.translate_xyz(amount, 0, 0)

    @override
    @supported(SupportLevel.SUPPORTED, notes="")
    def translate_y(self, amount: "str|float|Dimension") -> Self:
        return self.translate_xyz(0, amount, 0)

    @override
    @supported(SupportLevel.SUPPORTED, notes="")
    def translate_z(self, amount: "str|float|Dimension") -> Self:
        return self.translate_xyz(0, 0, amount)

    @override
    @supported(SupportLevel.UNSUPPORTED, notes="")
    def set_visible(self, is_visible: "bool") -> Self:
        raise NotImplementedError()

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_vertices(self) -> "list[VertexInterface]":
        print("get_vertices called")
        return [Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0]))]
