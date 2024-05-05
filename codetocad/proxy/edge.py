# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *


from codetocad.providers import get_provider

from codetocad.interfaces.edge_interface import EdgeInterface


from codetocad.interfaces.landmark_interface import LandmarkInterface

from codetocad.interfaces.vertex_interface import VertexInterface

from codetocad.interfaces.projectable_interface import ProjectableInterface

from codetocad.interfaces.subdividable_interface import SubdividableInterface

from codetocad.interfaces.patternable_interface import PatternableInterface

from codetocad.interfaces.mirrorable_interface import MirrorableInterface

from codetocad.interfaces.landmarkable_interface import LandmarkableInterface

from codetocad.interfaces.entity_interface import EntityInterface


from providers.sample.entity import Entity


class Edge(EdgeInterface, Entity):
    """
    A curve bounded by two Vertices.

    NOTE: This is a proxy - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """

    # References OBJECT PROXYING (PYTHON RECIPE) https://code.activestate.com/recipes/496741-object-proxying/

    __slots__ = [
        "__proxied",
    ]

    def __init__(
        self,
        name: "str",
        v1: "VertexInterface",
        v2: "VertexInterface",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "str|EntityInterface| None" = None,
    ):

        self.__proxied = get_provider(EdgeInterface)(
            name, v1, v2, description, native_instance, parent_entity
        )  # type: ignore

    def offset(self, distance: "str|float|Dimension") -> "EdgeInterface":
        return self.__proxied.offset(distance)

    def fillet(self, other_edge: "EdgeInterface", amount: "str|float|Angle"):
        return self.__proxied.fillet(other_edge, amount)

    def set_is_construction(self, is_construction: "bool"):
        return self.__proxied.set_is_construction(is_construction)

    def get_is_construction(
        self,
    ) -> "bool":
        return self.__proxied.get_is_construction()

    def mirror(
        self,
        mirror_across_entity: "str|EntityInterface",
        axis: "str|int|Axis",
        resulting_mirrored_entity_name: "str| None" = None,
    ):
        return self.__proxied.mirror(
            mirror_across_entity, axis, resulting_mirrored_entity_name
        )

    def linear_pattern(
        self,
        instance_count: "int",
        offset: "str|float|Dimension",
        direction_axis: "str|int|Axis" = "z",
    ):
        return self.__proxied.linear_pattern(instance_count, offset, direction_axis)

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "str|float|Angle",
        center_entity_or_landmark: "str|EntityInterface",
        normal_direction_axis: "str|int|Axis" = "z",
    ):
        return self.__proxied.circular_pattern(
            instance_count,
            separation_angle,
            center_entity_or_landmark,
            normal_direction_axis,
        )

    def remesh(self, strategy: "str", amount: "float"):
        return self.__proxied.remesh(strategy, amount)

    def subdivide(self, amount: "float"):
        return self.__proxied.subdivide(amount)

    def decimate(self, amount: "float"):
        return self.__proxied.decimate(amount)

    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":
        return self.__proxied.project(project_from)

    def create_landmark(
        self,
        landmark_name: "str",
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ) -> "LandmarkInterface":
        return self.__proxied.create_landmark(landmark_name, x, y, z)

    def get_landmark(self, landmark_name: "str|PresetLandmark") -> "LandmarkInterface":
        return self.__proxied.get_landmark(landmark_name)
