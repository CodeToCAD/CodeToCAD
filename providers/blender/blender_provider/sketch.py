import math
from typing import Optional, Sequence

from codetocad.core.shapes.circle import get_circle_points


from . import blender_actions, blender_definitions, implementables

from codetocad.interfaces import SketchInterface, PartInterface, VertexInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *

from codetocad.core.shapes.ellipse import get_ellipse_points


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

        self.resolution = 4 if curve_type == CurveTypes.BEZIER else 64

    def clone(self, new_name: str, copy_landmarks: bool = True) -> "Sketch":
        assert Entity(new_name).is_exists() is False, f"{new_name} already exists."

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
        self, profile_name_or_instance: EntityOrItsName, fill_cap: bool = True
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
        points: Sequence[PointOrListOfFloatOrItsStringValue],
        interpolation: "int" = 64,
        order_u: int = 2,
    ) -> "Wire":
        parsed_points = [Point.from_list_of_float_or_string(point) for point in points]

        is_closed = False
        if len(parsed_points) > 1 and parsed_points[0] == parsed_points[-1]:
            is_closed = True
            parsed_points = parsed_points[:-1]

        blender_spline, added_points = blender_actions.create_curve(
            self.name,
            blender_definitions.BlenderCurveTypes.from_curve_types(self.curve_type)
            if self.curve_type is not None
            else blender_definitions.BlenderCurveTypes.BEZIER,
            parsed_points,
            interpolation,
            is_3d=False,
            order_u=order_u,
        )

        if is_closed:
            blender_spline.use_cyclic_u = True

        return blender_actions.get_wire_from_blender_wire(
            entity=self.get_native_instance().data, wire=blender_spline
        )

    def create_point(self, point: PointOrListOfFloatOrItsStringValue) -> "Vertex":
        blender_spline, added_points = blender_actions.create_curve(
            curve_name=self.name,
            curve_type=blender_definitions.BlenderCurveTypes.from_curve_types(
                self.curve_type
            )
            if self.curve_type is not None
            else blender_definitions.BlenderCurveTypes.BEZIER,
            points=[point],
            is_3d=False,
        )
        return Vertex(
            location=point,
            name=create_uuid_like_id(),
            parent_entity=self,
            native_instance=blender_spline,
        )

    def create_line(
        self,
        start_at: PointOrListOfFloatOrItsStringValueOrVertex,
        end_at: PointOrListOfFloatOrItsStringValueOrVertex,
    ) -> "Edge":
        start_point: Point
        end_point: Point
        if isinstance(start_at, VertexInterface):
            start_point = Point.from_list_of_float_or_string(start_at.location)
        else:
            start_point = Point.from_list_of_float_or_string(start_at)

        if isinstance(end_at, VertexInterface):
            end_point = Point.from_list_of_float_or_string(end_at.location)
        else:
            end_point = Point.from_list_of_float_or_string(end_at)

        blender_spline, added_points = blender_actions.create_curve(
            curve_name=self.name,
            curve_type=blender_definitions.BlenderCurveTypes.from_curve_types(
                self.curve_type
            )
            if self.curve_type is not None
            else blender_definitions.BlenderCurveTypes.BEZIER,
            points=[start_point, end_point],
            is_3d=False,
        )

        edge = blender_actions.get_edge_from_blender_edge(
            entity=blender_actions.get_curve(self.name),
            edge=(added_points[0], added_points[1]),
        )

        return edge

    @staticmethod
    def _set_bezier_circular_handlers(wire: Wire, radius: Dimension):
        all_vertices = wire.get_vertices()
        num_verts = len(all_vertices)

        index = 1
        import mathutils

        for p1 in all_vertices:
            # References Blender Addon: add_curve_extra_objects/add_curve_simple.py
            p1x: float = p1.location.x.value
            p1y: float = p1.location.y.value
            if index >= num_verts:
                index = 0
            p2 = all_vertices[index]
            p2x: float = p2.location.x.value
            p2y: float = p2.location.y.value
            u1 = math.asin(p1y / radius.value)
            u2 = math.asin(p2y / radius.value)
            if (p1x > 0 and p2x < 0) or (p1x < 0 and p2x > 0):
                u1 = math.acos(p1x / radius.value)
                u2 = math.acos(p2x / radius.value)
            u = u2 - u1
            if u < 0:
                u = -u

            v1 = mathutils.Vector((p1y * -1, p1x, 0))
            v2 = mathutils.Vector((p2y * -1, p2x, 0))
            v1.normalize()
            v2.normalize()
            length = (4 / 3 * math.tan(1 / 4 * u)) * radius.value
            p1.get_native_instance().handle_right = (
                mathutils.Vector((p1x, p1y, 0)) + v1 * length
            )
            p2.get_native_instance().handle_left = (
                mathutils.Vector((p2x, p2y, 0)) - v2 * length
            )

            index += 1

    @staticmethod
    def _set_bezier_ellipse_handlers(
        wire: Wire, radius_x: Dimension, radius_y: Optional[Dimension] = None
    ):
        if not radius_y:
            radius_y = radius_x

        all_vertices = wire.get_vertices()
        num_verts = len(all_vertices)

        index = 1
        import mathutils
        from builtins import min as math_min

        for p1 in all_vertices:
            # References Blender Addon: add_curve_extra_objects/add_curve_simple.py
            p1x: float = p1.location.x.value
            p1y: float = p1.location.y.value
            if index >= num_verts:
                index = 0
            p2 = all_vertices[index]
            p2x: float = p2.location.x.value
            p2y: float = p2.location.y.value
            u1 = math.asin(p1y / radius_y.value)
            u2 = math.asin(p2y / radius_y.value)
            if (p1x > 0 and p2x < 0) or (p1x < 0 and p2x > 0):
                u1 = math.acos(p1x / radius_x.value)
                u2 = math.acos(p2x / radius_x.value)
            u = abs(u2 - u1)

            v1 = mathutils.Vector((p1y * -1, p1x, 0))
            v2 = mathutils.Vector((p2y * -1, p2x, 0))
            v1.normalize()
            v2.normalize()
            length = (4 / 3 * math.tan(1 / 4 * u)) * math_min(
                radius_x.value, radius_y.value
            )
            length = 2 * 0.27606262
            print("yo2")
            p1.get_native_instance().handle_right = (
                mathutils.Vector((p1x, p1y, 0)) + v1 * length
            )
            p2.get_native_instance().handle_left = (
                mathutils.Vector((p2x, p2y, 0)) - v2 * length
            )

            index += 1

    def create_circle(self, radius: DimensionOrItsFloatOrStringValue) -> "Wire":
        radius = Dimension.from_dimension_or_its_float_or_string_value(radius)

        points = get_circle_points(radius, self.resolution)

        wire = self.create_from_vertices(
            [Point.from_list_of_float_or_string(point) for point in points], order_u=4
        )

        if self.curve_type == CurveTypes.BEZIER:
            Sketch._set_bezier_circular_handlers(wire, radius)

        return wire

    def create_ellipse(
        self,
        radius_minor: DimensionOrItsFloatOrStringValue,
        radius_major: DimensionOrItsFloatOrStringValue,
    ) -> "Wire":
        radius_minor = Dimension.from_dimension_or_its_float_or_string_value(
            radius_minor
        )
        radius_major = Dimension.from_dimension_or_its_float_or_string_value(
            radius_major
        )

        points = get_ellipse_points(radius_minor, radius_major, self.resolution)[::-1]

        points.append(points[0])

        wire = self.create_from_vertices(points, order_u=4)

        if self.curve_type == CurveTypes.BEZIER:
            Sketch._set_bezier_ellipse_handlers(wire, radius_minor, radius_major)

        return wire

    def create_arc(
        self,
        start_at: PointOrListOfFloatOrItsStringValueOrVertex,
        center_at: PointOrListOfFloatOrItsStringValueOrVertex,
        end_at: PointOrListOfFloatOrItsStringValueOrVertex,
    ) -> "Wire":
        start_point: Point
        center_point: Point
        if isinstance(start_at, VertexInterface):
            start_point = Point.from_list_of_float_or_string(start_at.location)
        else:
            start_point = Point.from_list_of_float_or_string(start_at)
        if isinstance(center_at, VertexInterface):
            center_point = Point.from_list_of_float_or_string(center_at.location)
        else:
            center_point = Point.from_list_of_float_or_string(center_at)

        radius = (center_point - start_point).magnitude()

        points = [start_point, center_point, end_at]

        wire = self.create_from_vertices(
            [Point.from_list_of_float_or_string(point) for point in points], order_u=4
        )

        if self.curve_type == CurveTypes.BEZIER:
            Sketch._set_bezier_circular_handlers(wire, radius)

        return wire

    def create_rectangle(
        self,
        length: DimensionOrItsFloatOrStringValue,
        width: DimensionOrItsFloatOrStringValue,
    ) -> "Wire":
        half_length = (
            Dimension.from_dimension_or_its_float_or_string_value(length, None) / 2
        )
        half_width = (
            Dimension.from_dimension_or_its_float_or_string_value(width, None) / 2
        )

        left_top = Point(half_length * -1, half_width, Dimension(0))
        left_bottom = Point(half_length * -1, half_width * -1, Dimension(0))
        right_bottom = Point(half_length, half_width * -1, Dimension(0))
        right_top = Point(half_length, half_width, Dimension(0))

        return self.create_from_vertices(
            [left_top, left_bottom, right_bottom, right_top, left_top]
        )

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
        implementables.linear_pattern(self, instance_count, offset, direction_axis)
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
