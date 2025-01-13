from typing import Optional
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.interfaces.projectable_interface import ProjectableInterface
from codetocad.proxy.vertex import Vertex
from codetocad.proxy.landmark import Landmark
from codetocad.interfaces.edge_interface import EdgeInterface
from codetocad.interfaces.vertex_interface import VertexInterface
from codetocad.interfaces.landmark_interface import LandmarkInterface
from providers.onshape.onshape_provider.entity import Entity
from providers.onshape.onshape_provider.vertex import Vertex
from providers.onshape.onshape_provider.landmark import Landmark
from codetocad.codetocad_types import *
from . import Entity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Vertex


class Edge(EdgeInterface, Entity):

    @supported(SupportLevel.SUPPORTED, notes="")
    def mirror(
        self,
        mirror_across_entity: "EntityInterface",
        axis: "str|int|Axis",
        separate_resulting_entity: "bool| None" = False,
    ):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def linear_pattern(
        self,
        instance_count: "int",
        offset: "str|float|Dimension",
        direction_axis: "str|int|Axis" = "z",
    ):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "str|float|Angle",
        center_entity_or_landmark: "EntityInterface",
        normal_direction_axis: "str|int|Axis" = "z",
    ):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def remesh(self, strategy: "str", amount: "float"):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def subdivide(self, amount: "float"):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def decimate(self, amount: "float"):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def project(self, project_from: "ProjectableInterface") -> "Projectable":
        raise NotImplementedError()

    v1: "Vertex"
    v2: "Vertex"
    parent: Optional[str | Entity] = None
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(self, native_instance: "Any"):
        self.v1 = v1
        self.v2 = v2
        self.parent = parent
        self.name = name
        self.description = description
        self.native_instance = native_instance

    @supported(SupportLevel.SUPPORTED, notes="")
    def offset(self, distance: "str|float|Dimension") -> "Edge":
        raise NotImplementedError()

    @supported(SupportLevel.SUPPORTED, notes="")
    def fillet(self, other_edge: "EdgeInterface", amount: "str|float|Angle"):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_is_construction(self, is_construction: "bool"):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_is_construction(self) -> bool:
        raise NotImplementedError()

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_landmark(
        self,
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
        landmark_name: "str| None" = None,
    ) -> "LandmarkInterface":
        print("create_landmark called", f": {landmark_name}, {x}, {y}, {z}")
        return Landmark("name", "parent")

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_landmark(self, landmark_name: "str|PresetLandmark") -> "LandmarkInterface":
        print("get_landmark called", f": {landmark_name}")
        return Landmark("name", "parent")

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_vertices(self) -> "list[VertexInterface]":
        print("get_vertices called")
        return [Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0]))]
