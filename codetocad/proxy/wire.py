# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *

from typing import Self


from codetocad.providers import get_provider

from codetocad.interfaces.wire_interface import WireInterface


from codetocad.interfaces.vertex_interface import VertexInterface

from codetocad.interfaces.part_interface import PartInterface

from codetocad.interfaces.edge_interface import EdgeInterface

from codetocad.interfaces.landmark_interface import LandmarkInterface


from codetocad.interfaces.projectable_interface import ProjectableInterface


from codetocad.interfaces.booleanable_interface import BooleanableInterface


from codetocad.interfaces.entity_interface import EntityInterface


from codetocad.proxy.entity import Entity


class Wire(WireInterface, Entity):
    """
    A collection of connected edges.

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
        edges: "list[EdgeInterface]",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "str|EntityInterface| None" = None,
    ):
        object.__setattr__(
            self,
            "__proxied",
            get_provider(WireInterface)(
                name, edges, description, native_instance, parent_entity
            ),  # type: ignore
        )

    def get_normal(self, flip: "bool| None" = False) -> "Point":
        return object.__getattribute__(self, "__proxied").get_normal(flip)

    def get_edges(
        self,
    ) -> "list[EdgeInterface]":
        return object.__getattribute__(self, "__proxied").get_edges()

    def get_vertices(
        self,
    ) -> "list[VertexInterface]":
        return object.__getattribute__(self, "__proxied").get_vertices()

    def get_is_closed(
        self,
    ) -> "bool":
        return object.__getattribute__(self, "__proxied").get_is_closed()

    def loft(
        self, other: "WireInterface", new_part_name: "str| None" = None
    ) -> "PartInterface":
        return object.__getattribute__(self, "__proxied").loft(other, new_part_name)

    def revolve(
        self,
        angle: "str|float|Angle",
        about_entity_or_landmark: "str|EntityInterface",
        axis: "str|int|Axis" = "z",
    ) -> "PartInterface":
        return object.__getattribute__(self, "__proxied").revolve(
            angle, about_entity_or_landmark, axis
        )

    def twist(
        self,
        angle: "str|float|Angle",
        screw_pitch: "str|float|Dimension",
        iterations: "int" = 1,
        axis: "str|int|Axis" = "z",
    ) -> Self:
        return object.__getattribute__(self, "__proxied").twist(
            angle, screw_pitch, iterations, axis
        )

    def extrude(self, length: "str|float|Dimension") -> "PartInterface":
        return object.__getattribute__(self, "__proxied").extrude(length)

    def sweep(
        self, profile_name_or_instance: "str|WireInterface", fill_cap: "bool" = True
    ) -> "PartInterface":
        return object.__getattribute__(self, "__proxied").sweep(
            profile_name_or_instance, fill_cap
        )

    def offset(self, radius: "str|float|Dimension") -> "WireInterface":
        return object.__getattribute__(self, "__proxied").offset(radius)

    def profile(self, profile_curve_name: "str") -> Self:
        return object.__getattribute__(self, "__proxied").profile(profile_curve_name)

    def create_from_vertices(
        self,
        points: "list[str|list[str]|list[float]|list[Dimension]|Point|VertexInterface]",
        options: "SketchOptions| None" = None,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").create_from_vertices(
            points, options
        )

    def create_point(
        self,
        point: "str|list[str]|list[float]|list[Dimension]|Point",
        options: "SketchOptions| None" = None,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").create_point(point, options)

    def create_line(
        self,
        length: "str|float|Dimension",
        angle: "str|float|Angle",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        options: "SketchOptions| None" = None,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").create_line(
            length, angle, start_at, options
        )

    def create_line_to(
        self,
        to: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        options: "SketchOptions| None" = None,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").create_line_to(
            to, start_at, options
        )

    def create_arc(
        self,
        end_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface",
        radius: "str|float|Dimension",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        flip: "bool| None" = False,
        options: "SketchOptions| None" = None,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").create_arc(
            end_at, radius, start_at, flip, options
        )

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

    def union(
        self,
        other: "str|BooleanableInterface",
        delete_after_union: "bool" = True,
        is_transfer_data: "bool" = False,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").union(
            other, delete_after_union, is_transfer_data
        )

    def subtract(
        self,
        other: "str|BooleanableInterface",
        delete_after_subtract: "bool" = True,
        is_transfer_data: "bool" = False,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").subtract(
            other, delete_after_subtract, is_transfer_data
        )

    def intersect(
        self,
        other: "str|BooleanableInterface",
        delete_after_intersect: "bool" = True,
        is_transfer_data: "bool" = False,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").intersect(
            other, delete_after_intersect, is_transfer_data
        )

    def remesh(self, strategy: "str", amount: "float") -> Self:
        return object.__getattribute__(self, "__proxied").remesh(strategy, amount)

    def subdivide(self, amount: "float") -> Self:
        return object.__getattribute__(self, "__proxied").subdivide(amount)

    def decimate(self, amount: "float") -> Self:
        return object.__getattribute__(self, "__proxied").decimate(amount)
