from typing import Optional


from . import blender_actions, blender_definitions, implementables


from codetocad.interfaces import SketchInterface, PartInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from . import Entity, Part, Vertex, Wire, Edge


class Sketch(Entity, SketchInterface):
    name: str
    curve_type: Optional[CurveTypes] = None
    description: Optional[str] = None

    def __init__(
        self,
        name: str,
        curve_type: Optional[CurveTypes] = None,
        description: Optional[str] = None,
    ):
        self.name = name
        self.curve_type = curve_type
        self.description = description

    def clone(self, new_name: str, copy_landmarks: bool = True) -> "Sketch":
        assert Entity(new_name).is_exists(
        ) is False, f"{new_name} already exists."

        blender_actions.duplicate_object(self.name, new_name, copy_landmarks)

        return Sketch(new_name, self.curve_type, self.description)

    def create_from_file(self, file_path: str, file_type: Optional[str] = None):
        raise NotImplementedError()
        return self

    def revolve(
        self,
        angle: AngleOrItsFloatOrStringValue,
        about_entity_or_landmark: EntityOrItsName,
        axis: AxisOrItsIndexOrItsName = "z",
    ) -> "PartInterface":
        if isinstance(about_entity_or_landmark, Entity):
            about_entity_or_landmark = about_entity_or_landmark.name

        axis = Axis.from_string(axis)

        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

        blender_actions.apply_screw_modifier(
            self.name,
            Angle.from_string(angle).to_radians(),
            axis,
            entity_nameToDetermineAxis=about_entity_or_landmark,
        )

        blender_actions.create_mesh_from_curve(self.name)

        return Part(self.name, self.description).apply()

    def offset(self, radius: DimensionOrItsFloatOrStringValue):
        radius = Dimension.from_string(radius)

        blender_actions.set_curve_offset_geometry(self.name, radius)

        return self

    def extrude(self, length: DimensionOrItsFloatOrStringValue) -> "PartInterface":
        blender_actions.set_curve_extrude_property(
            self.name, Dimension.from_string(length)
        )

        blender_actions.create_mesh_from_curve(self.name)

        return Part(self.name, self.description).apply()

    def sweep(
        self, profile_name_or_instance: SketchOrItsName, fill_cap: bool = True
    ) -> "PartInterface":
        profile_curve_name = profile_name_or_instance
        if isinstance(profile_curve_name, SketchInterface):
            profile_curve_name = profile_curve_name.name

        blender_actions.add_bevel_object_to_curve(
            self.name, profile_curve_name, fill_cap
        )

        blender_actions.create_mesh_from_curve(self.name)

        # Recalculate normals because they're usually wrong after sweeping.
        blender_actions.recalculate_normals(self.name)

        return Part(self.name, self.description).apply()

    def profile(self, profile_curve_name):
        if isinstance(profile_curve_name, Entity):
            profile_curve_name = profile_curve_name.name

        blender_actions.apply_curve_modifier(self.name, profile_curve_name)

        return self

    def create_text(
        self,
        text: str,
        font_size: DimensionOrItsFloatOrStringValue = 1.0,
        bold: bool = False,
        italic: bool = False,
        underlined: bool = False,
        character_spacing: "int" = 1,
        word_spacing: "int" = 1,
        line_spacing: "int" = 1,
        font_file_path: Optional[str] = None,
    ):
        size = Dimension.from_string(font_size)

        blender_actions.create_text(
            self.name,
            text,
            size,
            bold,
            italic,
            underlined,
            character_spacing,
            word_spacing,
            line_spacing,
            font_file_path,
        )
        return self

    def create_from_vertices(
        self,
        points: list[PointOrListOfFloatOrItsStringValue],
        interpolation: "int" = 64,
    ):
        blender_actions.create_curve(
            self.name,
            blender_definitions.BlenderCurveTypes.from_curve_types(
                self.curve_type)
            if self.curve_type is not None
            else blender_definitions.BlenderCurveTypes.BEZIER,
            points,
            interpolation,
            is_3d=True,
        )

        return self

    def create_point(self, point: PointOrListOfFloatOrItsStringValue) -> "Vertex":
        return Vertex(
            location=point,
            name=create_uuid_like_id(),
            parent_sketch=self,
            native_instance=blender_actions.create_curve(
                curve_name=self.name,
                curve_type=blender_definitions.BlenderCurveTypes.from_curve_types(
                    self.curve_type
                )
                if self.curve_type is not None
                else blender_definitions.BlenderCurveTypes.BEZIER,
                points=[point],
                is_3d=False,
            ),
        )

    def create_line(
        self,
        start_at: PointOrListOfFloatOrItsStringValueOrVertex,
        end_at: PointOrListOfFloatOrItsStringValueOrVertex,
    ) -> "Edge":
        return self

    def create_circle(self, radius: DimensionOrItsFloatOrStringValue) -> "Wire":
        raise NotImplementedError()

    def create_ellipse(
        self,
        radius_minor: DimensionOrItsFloatOrStringValue,
        radius_major: DimensionOrItsFloatOrStringValue,
    ) -> "Wire":
        raise NotImplementedError()

    def create_arc(
        self,
        start_at: PointOrListOfFloatOrItsStringValueOrVertex,
        center_at: PointOrListOfFloatOrItsStringValueOrVertex,
        end_at: PointOrListOfFloatOrItsStringValueOrVertex,
    ) -> "Wire":
        raise NotImplementedError()

    def create_rectangle(
        self,
        length: DimensionOrItsFloatOrStringValue,
        width: DimensionOrItsFloatOrStringValue,
    ) -> "Wire":
        raise NotImplementedError()

    def create_polygon(
        self,
        number_of_sides: "int",
        length: DimensionOrItsFloatOrStringValue,
        width: DimensionOrItsFloatOrStringValue,
    ) -> "Wire":
        raise NotImplementedError()

    def create_trapezoid(
        self,
        length_upper: DimensionOrItsFloatOrStringValue,
        length_lower: DimensionOrItsFloatOrStringValue,
        height: DimensionOrItsFloatOrStringValue,
    ) -> "Wire":
        raise NotImplementedError()

    def create_spiral(
        self,
        number_of_turns: "int",
        height: DimensionOrItsFloatOrStringValue,
        radius: DimensionOrItsFloatOrStringValue,
        is_clockwise: bool = True,
        radius_end: Optional[DimensionOrItsFloatOrStringValue] = None,
    ) -> "Wire":
        raise NotImplementedError()

    def twist(
        self,
        angle: AngleOrItsFloatOrStringValue,
        screw_pitch: DimensionOrItsFloatOrStringValue,
        iterations: "int" = 1,
        axis: AxisOrItsIndexOrItsName = "z",
    ):
        implementables.twist(self, angle, screw_pitch, iterations, axis)
        return self

    def mirror(
        self,
        mirror_across_entity: EntityOrItsName,
        axis: AxisOrItsIndexOrItsName,
        resulting_mirrored_entity_name: Optional[str] = None,
    ):
        implementables.mirror(
            self, mirror_across_entity, axis, resulting_mirrored_entity_name
        )
        return self

    def linear_pattern(
        self,
        instance_count: "int",
        offset: DimensionOrItsFloatOrStringValue,
        direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        implementables.linear_pattern(
            self, instance_count, offset, direction_axis)
        return self

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: AngleOrItsFloatOrStringValue,
        center_entity_or_landmark: EntityOrItsName,
        normal_direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        implementables.circular_pattern(
            self,
            instance_count,
            separation_angle,
            center_entity_or_landmark,
            normal_direction_axis,
        )
        return self

    def export(self, file_path: str, overwrite: bool = True, scale: float = 1.0):
        implementables.export(self, file_path, overwrite, scale)
        return self

    def scale_xyz(
        self,
        x: DimensionOrItsFloatOrStringValue,
        y: DimensionOrItsFloatOrStringValue,
        z: DimensionOrItsFloatOrStringValue,
    ):
        implementables.scale_xyz(self, x, y, z)
        return self

    def scale_x(self, scale: DimensionOrItsFloatOrStringValue):
        implementables.scale_x(self, scale)
        return self

    def scale_y(self, scale: DimensionOrItsFloatOrStringValue):
        implementables.scale_y(self, scale)
        return self

    def scale_z(self, scale: DimensionOrItsFloatOrStringValue):
        implementables.scale_z(self, scale)
        return self

    def scale_x_by_factor(self, scale_factor: float):
        implementables.scale_x_by_factor(self, scale_factor)
        return self

    def scale_y_by_factor(self, scale_factor: float):
        implementables.scale_y_by_factor(self, scale_factor)
        return self

    def scale_z_by_factor(self, scale_factor: float):
        implementables.scale_z_by_factor(self, scale_factor)
        return self

    def scale_keep_aspect_ratio(
        self, scale: DimensionOrItsFloatOrStringValue, axis: AxisOrItsIndexOrItsName
    ):
        implementables.scale_keep_aspect_ratio(self, scale, axis)
        return self
