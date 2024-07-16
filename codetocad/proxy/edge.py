# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *

from typing import Self


from codetocad.providers import get_provider

from codetocad.interfaces.edge_interface import EdgeInterface


from codetocad.interfaces.vertex_interface import VertexInterface

from codetocad.interfaces.landmark_interface import LandmarkInterface


from codetocad.interfaces.projectable_interface import ProjectableInterface


from codetocad.interfaces.entity_interface import EntityInterface


from codetocad.proxy.entity import Entity


class Edge(EdgeInterface, Entity):
    """
    A curve bounded by two Vertices.

    NOTE: This is a proxy - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """

    # References OBJECT PROXYING (PYTHON RECIPE) https://code.activestate.com/recipes/496741-object-proxying/

    def __getattribute__(self, name):
        return getattr(object.__getattribute__(self, "__proxied"), name)

    def __delattr__(self, name):
        delattr(object.__getattribute__(self, "__proxied"), name)

    def __setattr__(self, name, value):
        setattr(object.__getattribute__(self, "__proxied"), name, value)

    def __nonzero__(self):
        return bool(object.__getattribute__(self, "__proxied"))

    def __str__(self):
        return str(object.__getattribute__(self, "__proxied"))

    def __repr__(self):
        return repr(object.__getattribute__(self, "__proxied"))

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
        object.__setattr__(
            self,
            "__proxied",
            get_provider(EdgeInterface)(
                name, v1, v2, description, native_instance, parent_entity
            ),  # type: ignore
        )

    def offset(self, distance: "str|float|Dimension") -> "EdgeInterface":
        return object.__getattribute__(self, "__proxied").offset(distance)

    def fillet(self, other_edge: "EdgeInterface", amount: "str|float|Angle") -> Self:
        return object.__getattribute__(self, "__proxied").fillet(other_edge, amount)

    def set_is_construction(self, is_construction: "bool") -> Self:
        return object.__getattribute__(self, "__proxied").set_is_construction(
            is_construction
        )

    def get_is_construction(
        self,
    ) -> "bool":
        return object.__getattribute__(self, "__proxied").get_is_construction()

    def mirror(
        self,
        mirror_across_entity: "str|EntityInterface",
        axis: "str|int|Axis",
        resulting_mirrored_entity_name: "str| None" = None,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").mirror(
            mirror_across_entity, axis, resulting_mirrored_entity_name
        )

    def linear_pattern(
        self,
        instance_count: "int",
        offset: "str|float|Dimension",
        direction_axis: "str|int|Axis" = "z",
    ) -> Self:
        return object.__getattribute__(self, "__proxied").linear_pattern(
            instance_count, offset, direction_axis
        )

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "str|float|Angle",
        center_entity_or_landmark: "str|EntityInterface",
        normal_direction_axis: "str|int|Axis" = "z",
    ) -> Self:
        return object.__getattribute__(self, "__proxied").circular_pattern(
            instance_count,
            separation_angle,
            center_entity_or_landmark,
            normal_direction_axis,
        )

    def remesh(self, strategy: "str", amount: "float") -> Self:
        return object.__getattribute__(self, "__proxied").remesh(strategy, amount)

    def subdivide(self, amount: "float") -> Self:
        return object.__getattribute__(self, "__proxied").subdivide(amount)

    def decimate(self, amount: "float") -> Self:
        return object.__getattribute__(self, "__proxied").decimate(amount)

    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":
        return object.__getattribute__(self, "__proxied").project(project_from)

    def create_landmark(
        self,
        landmark_name: "str",
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ) -> "LandmarkInterface":
        return object.__getattribute__(self, "__proxied").create_landmark(
            landmark_name, x, y, z
        )

    def get_landmark(self, landmark_name: "str|PresetLandmark") -> "LandmarkInterface":
        return object.__getattribute__(self, "__proxied").get_landmark(landmark_name)
