# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *


from codetocad.providers import get_provider

from codetocad.interfaces.wire_interface import WireInterface


from codetocad.interfaces.part_interface import PartInterface

from codetocad.interfaces.vertex_interface import VertexInterface

from codetocad.interfaces.landmark_interface import LandmarkInterface

from codetocad.interfaces.edge_interface import EdgeInterface

from codetocad.interfaces.projectable_interface import ProjectableInterface

from codetocad.interfaces.subdividable_interface import SubdividableInterface

from codetocad.interfaces.patternable_interface import PatternableInterface

from codetocad.interfaces.booleanable_interface import BooleanableInterface

from codetocad.interfaces.mirrorable_interface import MirrorableInterface

from codetocad.interfaces.landmarkable_interface import LandmarkableInterface

from codetocad.interfaces.entity_interface import EntityInterface


from providers.sample.entity import Entity


class Wire(WireInterface, Entity):
    """
    A collection of connected edges.

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
        edges: "list[EdgeInterface]",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "str|EntityInterface| None" = None,
    ):

        self.__proxied = get_provider(WireInterface)(
            name, edges, description, native_instance, parent_entity
        )  # type: ignore

    def get_normal(self, flip: "bool| None" = False) -> "Point":
        return self.__proxied.get_normal(flip)

    def get_edges(
        self,
    ) -> "list[EdgeInterface]":
        return self.__proxied.get_edges()

    def get_vertices(
        self,
    ) -> "list[VertexInterface]":
        return self.__proxied.get_vertices()

    def get_is_closed(
        self,
    ) -> "bool":
        return self.__proxied.get_is_closed()

    def loft(
        self, other: "WireInterface", new_part_name: "str| None" = None
    ) -> "PartInterface":
        return self.__proxied.loft(other, new_part_name)

    def revolve(
        self,
        angle: "str|float|Angle",
        about_entity_or_landmark: "str|EntityInterface",
        axis: "str|int|Axis" = "z",
    ) -> "PartInterface":
        return self.__proxied.revolve(angle, about_entity_or_landmark, axis)

    def twist(
        self,
        angle: "str|float|Angle",
        screw_pitch: "str|float|Dimension",
        iterations: "int" = 1,
        axis: "str|int|Axis" = "z",
    ):
        return self.__proxied.twist(angle, screw_pitch, iterations, axis)

    def extrude(self, length: "str|float|Dimension") -> "PartInterface":
        return self.__proxied.extrude(length)

    def sweep(
        self, profile_name_or_instance: "str|WireInterface", fill_cap: "bool" = True
    ) -> "PartInterface":
        return self.__proxied.sweep(profile_name_or_instance, fill_cap)

    def offset(self, radius: "str|float|Dimension"):
        return self.__proxied.offset(radius)

    def profile(self, profile_curve_name: "str"):
        return self.__proxied.profile(profile_curve_name)

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

    def union(
        self,
        other: "str|BooleanableInterface",
        delete_after_union: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        return self.__proxied.union(other, delete_after_union, is_transfer_data)

    def subtract(
        self,
        other: "str|BooleanableInterface",
        delete_after_subtract: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        return self.__proxied.subtract(other, delete_after_subtract, is_transfer_data)

    def intersect(
        self,
        other: "str|BooleanableInterface",
        delete_after_intersect: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        return self.__proxied.intersect(other, delete_after_intersect, is_transfer_data)

    def remesh(self, strategy: "str", amount: "float"):
        return self.__proxied.remesh(strategy, amount)

    def subdivide(self, amount: "float"):
        return self.__proxied.subdivide(amount)

    def decimate(self, amount: "float"):
        return self.__proxied.decimate(amount)
