# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from codetocad.interfaces import EdgeInterface


from codetocad.interfaces.entity_interface import EntityInterface

from codetocad.interfaces.landmark_interface import LandmarkInterface

from codetocad.interfaces.vertex_interface import VertexInterface


from codetocad.providers_sample.entity import Entity

from codetocad.providers_sample.landmark import Landmark

from codetocad.providers_sample.vertex import Vertex


class Edge(EdgeInterface, Entity):
    def __init__(
        self,
        name: "str",
        v1: "VertexInterface",
        v2: "VertexInterface",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "EntityOrItsName| None" = None,
    ):
        self.name = name
        self.v1 = v1
        self.v2 = v2
        self.description = description
        self.native_instance = native_instance
        self.parent_entity = parent_entity

    def offset(self, distance: "DimensionOrItsFloatOrStringValue") -> "EdgeInterface":
        print("offset called", f": {distance}")

        return Edge(
            v1=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            v2=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            name="an edge",
        )

    def fillet(
        self, other_edge: "EdgeInterface", amount: "AngleOrItsFloatOrStringValue"
    ):
        print("fillet called", f": {other_edge}, {amount}")

        return self

    def set_is_construction(self, is_construction: "bool"):
        print("set_is_construction called", f": {is_construction}")

        return self

    def get_is_construction(
        self,
    ) -> "bool":
        print(
            "get_is_construction called",
        )

        return True

    def mirror(
        self,
        mirror_across_entity: "EntityOrItsName",
        axis: "AxisOrItsIndexOrItsName",
        resulting_mirrored_entity_name: "str| None" = None,
    ):
        print(
            "mirror called",
            f": {mirror_across_entity}, {axis}, {resulting_mirrored_entity_name}",
        )

        return self

    def linear_pattern(
        self,
        instance_count: "int",
        offset: "DimensionOrItsFloatOrStringValue",
        direction_axis: "AxisOrItsIndexOrItsName" = "z",
    ):
        print(
            "linear_pattern called", f": {instance_count}, {offset}, {direction_axis}"
        )

        return self

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "AngleOrItsFloatOrStringValue",
        center_entity_or_landmark: "EntityOrItsName",
        normal_direction_axis: "AxisOrItsIndexOrItsName" = "z",
    ):
        print(
            "circular_pattern called",
            f": {instance_count}, {separation_angle}, {center_entity_or_landmark}, {normal_direction_axis}",
        )

        return self

    def remesh(self, strategy: "str", amount: "float"):
        print("remesh called", f": {strategy}, {amount}")

        return self

    def subdivide(self, amount: "float"):
        print("subdivide called", f": {amount}")

        return self

    def decimate(self, amount: "float"):
        print("decimate called", f": {amount}")

        return self

    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":
        print("project called", f": {project_from}")

        return __import__("codetocad").Sketch("a projected sketch")

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
