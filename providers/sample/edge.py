# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *

from typing import Self

from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel


from codetocad.interfaces.edge_interface import EdgeInterface


from codetocad.interfaces.vertex_interface import VertexInterface

from codetocad.interfaces.landmark_interface import LandmarkInterface


from codetocad.interfaces.projectable_interface import ProjectableInterface


from codetocad.interfaces.entity_interface import EntityInterface


from codetocad.proxy.vertex import Vertex

from codetocad.proxy.landmark import Landmark


from providers.sample.entity import Entity


class Edge(EdgeInterface, Entity):

    def __init__(
        self,
        name: "str",
        v1: "VertexInterface",
        v2: "VertexInterface",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "str|EntityInterface| None" = None,
    ):

        self.name = name
        self.v1 = v1
        self.v2 = v2
        self.description = description
        self.native_instance = native_instance
        self.parent_entity = parent_entity

    @supported(SupportLevel.SUPPORTED, notes="")
    def offset(self, distance: "str|float|Dimension") -> "EdgeInterface":

        print("offset called", f": {distance}")

        return Edge(
            v1=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            v2=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            name="an edge",
        )

    @supported(SupportLevel.SUPPORTED, notes="")
    def fillet(self, other_edge: "EdgeInterface", amount: "str|float|Angle") -> Self:

        print("fillet called", f": {other_edge}, {amount}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_is_construction(self, is_construction: "bool") -> Self:

        print("set_is_construction called", f": {is_construction}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_is_construction(
        self,
    ) -> "bool":

        print(
            "get_is_construction called",
        )

        return True

    @supported(SupportLevel.SUPPORTED, notes="")
    def mirror(
        self,
        mirror_across_entity: "str|EntityInterface",
        axis: "str|int|Axis",
        resulting_mirrored_entity_name: "str| None" = None,
    ) -> Self:

        print(
            "mirror called",
            f": {mirror_across_entity}, {axis}, {resulting_mirrored_entity_name}",
        )

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def linear_pattern(
        self,
        instance_count: "int",
        offset: "str|float|Dimension",
        direction_axis: "str|int|Axis" = "z",
    ) -> Self:

        print(
            "linear_pattern called", f": {instance_count}, {offset}, {direction_axis}"
        )

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "str|float|Angle",
        center_entity_or_landmark: "str|EntityInterface",
        normal_direction_axis: "str|int|Axis" = "z",
    ) -> Self:

        print(
            "circular_pattern called",
            f": {instance_count}, {separation_angle}, {center_entity_or_landmark}, {normal_direction_axis}",
        )

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def remesh(self, strategy: "str", amount: "float") -> Self:

        print("remesh called", f": {strategy}, {amount}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def subdivide(self, amount: "float") -> Self:

        print("subdivide called", f": {amount}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def decimate(self, amount: "float") -> Self:

        print("decimate called", f": {amount}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":

        print("project called", f": {project_from}")

        return __import__("codetocad").Sketch("a projected sketch")

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_landmark(
        self,
        landmark_name: "str",
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ) -> "LandmarkInterface":

        print("create_landmark called", f": {landmark_name}, {x}, {y}, {z}")

        return Landmark("name", "parent")

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_landmark(self, landmark_name: "str|PresetLandmark") -> "LandmarkInterface":

        print("get_landmark called", f": {landmark_name}")

        return Landmark("name", "parent")
