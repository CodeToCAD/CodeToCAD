# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *

from typing import Self


from codetocad.providers import get_provider

from codetocad.interfaces.sketch_interface import SketchInterface


from codetocad.interfaces.vertex_interface import VertexInterface

from codetocad.interfaces.wire_interface import WireInterface

from codetocad.interfaces.landmark_interface import LandmarkInterface


from codetocad.interfaces.projectable_interface import ProjectableInterface


from codetocad.interfaces.entity_interface import EntityInterface


from codetocad.proxy.entity import Entity


class Sketch(SketchInterface, Entity):
    """
    Capabilities related to creating and manipulating 2D sketches, composed of vertices, edges and wires.

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
        description: "str| None" = None,
        native_instance=None,
        curve_type: "CurveTypes| None" = None,
    ):
        object.__setattr__(
            self,
            "__proxied",
            get_provider(SketchInterface)(
                name, description, native_instance, curve_type
            ),  # type: ignore
        )

    def get_wires(
        self,
    ) -> "list[WireInterface]":
        return object.__getattribute__(self, "__proxied").get_wires()

    def clone(
        self, new_name: "str", copy_landmarks: "bool" = True
    ) -> "SketchInterface":
        return object.__getattribute__(self, "__proxied").clone(
            new_name, copy_landmarks
        )

    def create_text(
        self,
        text: "str",
        font_size: "str|float|Dimension" = 1.0,
        bold: "bool" = False,
        italic: "bool" = False,
        underlined: "bool" = False,
        character_spacing: "int" = 1,
        word_spacing: "int" = 1,
        line_spacing: "int" = 1,
        font_file_path: "str| None" = None,
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":
        return object.__getattribute__(self, "__proxied").create_text(
            text,
            font_size,
            bold,
            italic,
            underlined,
            character_spacing,
            word_spacing,
            line_spacing,
            font_file_path,
            center_at,
            options,
        )

    def create_from_vertices(
        self,
        points: "list[str|list[str]|list[float]|list[Dimension]|Point|VertexInterface]",
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":
        return object.__getattribute__(self, "__proxied").create_from_vertices(
            points, options
        )

    def create_point(
        self,
        point: "str|list[str]|list[float]|list[Dimension]|Point",
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":
        return object.__getattribute__(self, "__proxied").create_point(point, options)

    def create_line(
        self,
        length: "str|float|Dimension",
        angle: "str|float|Angle",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":
        return object.__getattribute__(self, "__proxied").create_line(
            length, angle, start_at, options
        )

    def create_line_to(
        self,
        to: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":
        return object.__getattribute__(self, "__proxied").create_line_to(
            to, start_at, options
        )

    def create_circle(
        self,
        radius: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":
        return object.__getattribute__(self, "__proxied").create_circle(
            radius, center_at, options
        )

    def create_ellipse(
        self,
        radius_minor: "str|float|Dimension",
        radius_major: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":
        return object.__getattribute__(self, "__proxied").create_ellipse(
            radius_minor, radius_major, center_at, options
        )

    def create_arc(
        self,
        end_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface",
        radius: "str|float|Dimension",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        flip: "bool| None" = False,
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":
        return object.__getattribute__(self, "__proxied").create_arc(
            end_at, radius, start_at, flip, options
        )

    def create_rectangle(
        self,
        length: "str|float|Dimension",
        width: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":
        return object.__getattribute__(self, "__proxied").create_rectangle(
            length, width, center_at, options
        )

    def create_polygon(
        self,
        number_of_sides: "int",
        length: "str|float|Dimension",
        width: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":
        return object.__getattribute__(self, "__proxied").create_polygon(
            number_of_sides, length, width, center_at, options
        )

    def create_trapezoid(
        self,
        length_upper: "str|float|Dimension",
        length_lower: "str|float|Dimension",
        height: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":
        return object.__getattribute__(self, "__proxied").create_trapezoid(
            length_upper, length_lower, height, center_at, options
        )

    def create_spiral(
        self,
        number_of_turns: "int",
        height: "str|float|Dimension",
        radius: "str|float|Dimension",
        is_clockwise: "bool" = True,
        radius_end: "str|float|Dimension| None" = None,
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":
        return object.__getattribute__(self, "__proxied").create_spiral(
            number_of_turns,
            height,
            radius,
            is_clockwise,
            radius_end,
            center_at,
            options,
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

    def create_from_file(self, file_path: "str", file_type: "str| None" = None) -> Self:
        return object.__getattribute__(self, "__proxied").create_from_file(
            file_path, file_type
        )

    def export(
        self, file_path: "str", overwrite: "bool" = True, scale: "float" = 1.0
    ) -> Self:
        return object.__getattribute__(self, "__proxied").export(
            file_path, overwrite, scale
        )

    def scale_xyz(
        self,
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ) -> Self:
        return object.__getattribute__(self, "__proxied").scale_xyz(x, y, z)

    def scale_x(self, scale: "str|float|Dimension") -> Self:
        return object.__getattribute__(self, "__proxied").scale_x(scale)

    def scale_y(self, scale: "str|float|Dimension") -> Self:
        return object.__getattribute__(self, "__proxied").scale_y(scale)

    def scale_z(self, scale: "str|float|Dimension") -> Self:
        return object.__getattribute__(self, "__proxied").scale_z(scale)

    def scale_x_by_factor(self, scale_factor: "float") -> Self:
        return object.__getattribute__(self, "__proxied").scale_x_by_factor(
            scale_factor
        )

    def scale_y_by_factor(self, scale_factor: "float") -> Self:
        return object.__getattribute__(self, "__proxied").scale_y_by_factor(
            scale_factor
        )

    def scale_z_by_factor(self, scale_factor: "float") -> Self:
        return object.__getattribute__(self, "__proxied").scale_z_by_factor(
            scale_factor
        )

    def scale_keep_aspect_ratio(
        self, scale: "str|float|Dimension", axis: "str|int|Axis"
    ) -> Self:
        return object.__getattribute__(self, "__proxied").scale_keep_aspect_ratio(
            scale, axis
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
