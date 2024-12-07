from typing import Self
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

    def __init__(
        self,
        v1: "VertexInterface",
        v2: "VertexInterface",
        name: "str| None" = None,
        description: "str| None" = None,
        native_instance=None,
        parent: "EntityInterface| None" = None,
    ):
        """
        NOTE: Blender Provider's Edge requires a parent and a native_instance
        """
        assert (
            parent is not None and native_instance is not None
        ), "Blender Provider's Edge requires a parent and a native_instance"
        self.v1 = v1
        self.v2 = v2
        self.parent = parent
        self.name = name
        self.description = description
        self.native_instance = native_instance

    @supported(SupportLevel.PLANNED)
    def offset(self, distance: "str|float|Dimension") -> "Edge":
        raise NotImplementedError()

    @supported(SupportLevel.PLANNED)
    def fillet(self, other_edge: "EdgeInterface", amount: "str|float|Angle"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def set_is_construction(self, is_construction: "bool"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def get_is_construction(self) -> bool:
        raise NotImplementedError()

    @supported(SupportLevel.PLANNED)
    def remesh(self, strategy: "str", amount: "float"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def subdivide(self, amount: "float"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def decimate(self, amount: "float"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def mirror(
        self,
        mirror_across_entity: "EntityInterface",
        axis: "str|int|Axis",
        separate_resulting_entity: "bool| None" = False,
    ):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def linear_pattern(
        self,
        instance_count: "int",
        offset: "str|float|Dimension",
        direction_axis: "str|int|Axis" = "z",
    ):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "str|float|Angle",
        center_entity_or_landmark: "EntityInterface",
        normal_direction_axis: "str|int|Axis" = "z",
    ):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def create_landmark(
        self,
        landmark_name: "str",
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ) -> "LandmarkInterface":
        raise NotImplementedError()
        print("create_landmark called", f": {landmark_name}, {x}, {y}, {z}")
        return Landmark("name", "parent")

    @supported(SupportLevel.PLANNED)
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
