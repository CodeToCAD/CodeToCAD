from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.interfaces.projectable_interface import ProjectableInterface
from codetocad.proxy.landmark import Landmark
from codetocad.interfaces.edge_interface import EdgeInterface
from codetocad.interfaces.vertex_interface import VertexInterface
from codetocad.interfaces.landmark_interface import LandmarkInterface
from providers.fusion360.fusion360_provider.entity import Entity
from providers.fusion360.fusion360_provider.landmark import Landmark
from codetocad.codetocad_types import *


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
        self.v1 = v1
        self.v2 = v2
        self.parent_entity = parent_entity
        self.name = name
        self.description = description
        self.native_instance = native_instance

    @supported(SupportLevel.PLANNED)
    def offset(self, distance: "str|float|Dimension") -> "Edge":
        raise NotImplementedError()
        return Edge.get_dummy_edge()

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
        return True

    @supported(SupportLevel.PLANNED)
    def create_landmark(
        self,
        landmark_name: "str",
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ) -> "LandmarkInterface":
        raise NotImplementedError()
        return Landmark("name", "parent")

    @supported(SupportLevel.PLANNED)
    def get_landmark(self, landmark_name: "str|PresetLandmark") -> "LandmarkInterface":
        raise NotImplementedError()
        return Landmark("name", "parent")

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
    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":
        raise NotImplementedError()
        return Sketch("a projected sketch")
