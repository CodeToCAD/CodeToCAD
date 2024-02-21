import math
from typing import Optional, Sequence

from codetocad.core.shapes.circle import get_center_of_circle, get_circle_points
from codetocad.core.shapes.clipping import clip_spline_points
from providers.blender.blender_provider.blender_actions.context import update_view_layer
from providers.blender.blender_provider.blender_actions.curve import (
    add_bevel_object_to_curve,
    create_curve,
    create_text,
    get_curve,
    merge_touching_splines,
    set_curve_offset_geometry,
)
from providers.blender.blender_provider.blender_actions.mesh import recalculate_normals
from providers.blender.blender_provider.blender_actions.modifiers import (
    apply_curve_modifier,
    apply_screw_modifier,
)
from providers.blender.blender_provider.blender_actions.normals import (
    project_vector_along_normal,
)
from providers.blender.blender_provider.blender_actions.objects_transmute import (
    create_mesh_from_curve,
    duplicate_object,
)
from providers.blender.blender_provider.blender_actions.vertex_edge_wire import (
    get_edge_from_blender_edge,
    get_wire_from_blender_wire,
    get_wires_from_blender_entity,
)


from codetocad.interfaces import (
    SketchInterface,
    PartInterface,
    VertexInterface,
    EntityInterface,
    LandmarkInterface,
    ProjectableInterface,
)
from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *

from providers.blender.blender_provider import (
    blender_definitions,
    implementables,
    Entity,
    Part,
    Vertex,
    Wire,
    Edge,
)


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

    def project(self, project_onto: "Sketch") -> "ProjectableInterface":
        print("project called:", project_onto)

        return Sketch("a projected sketch")

    def clone(self, new_name: str, copy_landmarks: bool = True) -> "Sketch":
        assert Entity(new_name).is_exists() is False, f"{new_name} already exists."

        duplicate_object(self.name, new_name, copy_landmarks)

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
        if isinstance(about_entity_or_landmark, LandmarkInterface):
            about_entity_or_landmark = (
                about_entity_or_landmark.get_landmark_entity_name()
            )
        elif isinstance(about_entity_or_landmark, Entity):
            about_entity_or_landmark = about_entity_or_landmark.name

        axis = Axis.from_string(axis)

        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

        apply_screw_modifier(
            self.name,
            Angle.from_string(angle).to_radians(),
            axis,
            entity_nameToDetermineAxis=about_entity_or_landmark,
        )

        create_mesh_from_curve(self.name)

        return Part(self.name, self.description).apply()

    def offset(self, radius: DimensionOrItsFloatOrStringValue):
        radius = Dimension.from_string(radius)

        set_curve_offset_geometry(self.name, radius)

        return self

    def extrude(self, length: DimensionOrItsFloatOrStringValue) -> "PartInterface":
        # We will assume that extruding a sketch will extrude all the underlying Wires.
        # We also assume the normal is never perpendicular to the Z axis.
        parsed_length = (
            blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_dimension_or_its_float_or_string_value(length)
            ).value
        )

        wires = get_wires_from_blender_entity(self.get_native_instance().data)

        for wire in wires:
            normal = wire.get_normal()

            # TODO: add the translation component of the wire's initial rotation. For example, if a rectangle of length 1x1 is rotated 45 degrees, then there is a 0.355 translation in the z axis that needs to be accounted for.
            translate_vector = [0, 0, parsed_length]

            projected_normal = project_vector_along_normal(
                translate_vector, [p.value for p in normal.to_list()]
            )
            temp_sketch = Sketch(self.name + "_temp")
            temp_wire = wire.clone(wire.name + "_temp", temp_sketch)

            temp_sketch.translate_xyz(*projected_normal)

            wire.loft(temp_wire)

        return Part(self.name, self.description)

    def sweep(
        self, profile_name_or_instance: EntityOrItsName, fill_cap: bool = True
    ) -> "PartInterface":
        profile_curve_name = profile_name_or_instance
        if isinstance(profile_curve_name, EntityInterface):
            profile_curve_name = profile_curve_name.name

        add_bevel_object_to_curve(self.name, profile_curve_name, fill_cap)

        create_mesh_from_curve(self.name)

        # Recalculate normals because they're usually wrong after sweeping.
        recalculate_normals(self.name)

        return Part(self.name, self.description).apply()

    def profile(self, profile_curve_name):
        if isinstance(profile_curve_name, Entity):
            profile_curve_name = profile_curve_name.name

        apply_curve_modifier(self.name, profile_curve_name)

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

        create_text(
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

        update_view_layer()

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

        blender_spline, curve_data, added_points = create_curve(
            self.name,
            blender_definitions.BlenderCurveTypes.from_curve_types(self.curve_type)
            if self.curve_type is not None
            else blender_definitions.BlenderCurveTypes.BEZIER,
            parsed_points,
            interpolation,
            is_3d=False,
            order_u=order_u,
        )

        merge_touching_splines(curve=curve_data, reference_spline_index=0)

        if is_closed:
            blender_spline.use_cyclic_u = True

        wire = get_wire_from_blender_wire(
            entity=self.get_native_instance().data, wire=blender_spline
        )

        update_view_layer()

        return wire

    def create_point(self, point: PointOrListOfFloatOrItsStringValue) -> "Vertex":
        blender_spline, curve_data, added_points = create_curve(
            curve_name=self.name,
            curve_type=blender_definitions.BlenderCurveTypes.from_curve_types(
                self.curve_type
            )
            if self.curve_type is not None
            else blender_definitions.BlenderCurveTypes.BEZIER,
            points=[point],
            is_3d=False,
        )

        merge_touching_splines(curve=curve_data, reference_spline_index=0)

        update_view_layer()

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

        blender_spline, curve_data, added_points = create_curve(
            curve_name=self.name,
            curve_type=blender_definitions.BlenderCurveTypes.from_curve_types(
                self.curve_type
            )
            if self.curve_type is not None
            else blender_definitions.BlenderCurveTypes.BEZIER,
            points=[start_point, end_point],
            is_3d=False,
        )

        merge_touching_splines(curve=curve_data, reference_spline_index=0)

        edge = get_edge_from_blender_edge(
            entity=get_curve(self.name),
            edge=(added_points[0], added_points[1]),
        )

        update_view_layer()

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

    def create_circle(self, radius: DimensionOrItsFloatOrStringValue) -> "Wire":
        radius = Dimension.from_dimension_or_its_float_or_string_value(radius)

        points = get_circle_points(radius, self.resolution)

        wire = self.create_from_vertices(
            [Point.from_list_of_float_or_string(point) for point in points], order_u=4
        )

        if self.curve_type == CurveTypes.BEZIER:
            Sketch._set_bezier_circular_handlers(wire, radius)

        update_view_layer()

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

        is_minor_lesser = radius_minor < radius_major

        wire = self.create_circle(radius_minor if is_minor_lesser else radius_major)

        update_view_layer()

        if is_minor_lesser:
            self.scale_y(radius_major * 2)
        else:
            self.scale_x(radius_minor * 2)

        return wire

    def create_arc(
        self,
        start_at: PointOrListOfFloatOrItsStringValueOrVertex,
        end_at: PointOrListOfFloatOrItsStringValueOrVertex,
        radius: DimensionOrItsFloatOrStringValue,
        flip: Optional[bool] = False,
    ) -> "Wire":
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

        radius = Dimension.from_dimension_or_its_float_or_string_value(radius)

        cord_length = start_point.distance_to(end_point)

        circle_radius = (
            radius.raise_power(2) + (cord_length / 2).raise_power(2)
        ).raise_power(1 / 2)

        points = get_circle_points(circle_radius, 64)

        parsed_points = [Point.from_list_of_float_or_string(point) for point in points]

        center_of_circle = get_center_of_circle(start_point, end_point, circle_radius)

        start_point_normalized = start_point - center_of_circle
        end_point_normalized = end_point - center_of_circle

        clipped_points_normalized = clip_spline_points(
            parsed_points,
            start_point_normalized,
            end_point_normalized,
            is_flip=flip or False,
            is_include_points=True,
        )

        clipped_points = [
            point + center_of_circle for point in clipped_points_normalized
        ]

        # is_closed = False
        # if len(clipped_points) > 1 and clipped_points[0] == clipped_points[-1]:
        #     is_closed = True
        #     clipped_points: list[Point] = clipped_points[:-1]

        blender_spline, curve_data, added_points = create_curve(
            self.name,
            blender_definitions.BlenderCurveTypes.from_curve_types(self.curve_type)
            if self.curve_type is not None
            else blender_definitions.BlenderCurveTypes.BEZIER,
            clipped_points,
            interpolation=self.resolution,
            is_3d=False,
            order_u=4,
        )

        wire = get_wire_from_blender_wire(curve_data, blender_spline)

        if self.curve_type == CurveTypes.BEZIER:
            Sketch._set_bezier_circular_handlers(wire, circle_radius)

        merge_touching_splines(curve=curve_data, reference_spline_index=0)

        # if is_closed:
        #     blender_spline.use_cyclic_u = True

        update_view_layer()

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

        left_top = Point(half_width * -1, half_length, Dimension(0))
        left_bottom = Point(half_width * -1, half_length * -1, Dimension(0))
        right_bottom = Point(half_width, half_length * -1, Dimension(0))
        right_top = Point(half_width, half_length, Dimension(0))

        wire = self.create_from_vertices(
            [left_top, left_bottom, right_bottom, right_top, left_top]
        )

        update_view_layer()

        return wire

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
