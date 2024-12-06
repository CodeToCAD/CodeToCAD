import cmath
from functools import wraps
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.edge_interface import EdgeInterface
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.proxy.vertex import Vertex
from codetocad.core.angle import Angle
from codetocad.core.dimension import Dimension
from codetocad.core.point import Point
from codetocad.interfaces.sketch_interface import SketchInterface
from codetocad.interfaces.wire_interface import WireInterface
from codetocad.interfaces.vertex_interface import VertexInterface
from codetocad.interfaces.landmark_interface import LandmarkInterface
from codetocad.interfaces.projectable_interface import ProjectableInterface
from codetocad.utilities import create_uuid_like_id
from codetocad.utilities.override import override
from providers.blender.blender_provider.blender_actions.collections import (
    assign_object_to_collection,
)
from providers.blender.blender_provider.blender_actions.modifiers import (
    apply_curve_modifier,
)
from providers.blender.blender_provider.blender_actions.objects import (
    create_object,
    get_object_or_none,
    get_object_visibility,
    remove_object,
)
from providers.blender.blender_provider.blender_definitions import (
    BlenderCurveTypes,
    BlenderLength,
    BlenderTypes,
)
from providers.blender.blender_provider.entity import Entity
from codetocad.core.shapes.circle import get_center_of_circle, get_circle_points
from codetocad.core.shapes.clipping import clip_spline_points
from providers.blender.blender_provider.blender_actions.context import update_view_layer
from providers.blender.blender_provider.blender_actions.curve import (
    create_curve,
    create_text,
    get_curve,
    merge_touching_splines,
    set_curve_resolution_u,
)
from providers.blender.blender_provider.blender_actions.objects_transmute import (
    duplicate_object,
)
from providers.blender.blender_provider.blender_actions.vertex_edge_wire import (
    get_edge_from_blender_edge,
    get_wire_from_blender_wire,
    get_wires_from_blender_entity,
)
from codetocad.codetocad_types import *
import providers.blender.blender_provider.implementables as implementables


class Sketch(SketchInterface, Entity):

    def __init__(
        self,
        name: "str| None" = None,
        description: "str| None" = None,
        native_instance=None,
        curve_type: "CurveTypes| None" = None,
    ):
        curve_type = curve_type or CurveTypes.BEZIER
        self.name = name
        self.curve_type = curve_type
        self.description = description
        self.resolution = 4 if curve_type == CurveTypes.BEZIER else 64

    @override
    @supported(SupportLevel.SUPPORTED)
    def set_visible(self, is_visible: "bool"):
        """
        BlenderProvider sketch.set_visible surfaces the Curve object when necessary, otherwise keeps it hidden.
        Note: is_visible is reliant on this implementation
        """
        if is_visible:
            if get_object_or_none(self.name, BlenderTypes.CURVE.value) is not None:
                return self
            create_object(self.name, get_curve(self.name))
            assign_object_to_collection(self.name)
        else:
            remove_object(self.name, is_remove_data=False)
        update_view_layer()
        return self

    @override
    @supported(
        SupportLevel.SUPPORTED,
        notes="Checks if the object is visible in the 3D viewport, taking into account all visibility settings",
    )
    def is_visible(self) -> bool:
        """
        BlenderProvider sketch.set_visible surfaces the Curve object when necessary, otherwise keeps it hidden. This is_visible hooks into this logic.
        """
        sketch_object = get_object_or_none(self.name, BlenderTypes.CURVE.value)
        if self.is_exists() and sketch_object is None:
            return False
        return get_object_visibility(self.name)

    @supported(
        SupportLevel.PARTIAL,
        notes="Tries to copy a curve's shape onto another projectable.",
    )
    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":
        if isinstance(project_from, WireInterface):
            points = project_from.get_vertices()
            points.append(points[0])
            wire = self.create_from_vertices(points)
            wire.name = project_from.name
            return wire
        raise NotImplementedError(f"Type {type(project_from)} is not supported.")

    @supported(SupportLevel.SUPPORTED)
    def clone(
        self, new_name: "str| None" = None, copy_landmarks: "bool| None" = True
    ) -> "Sketch":
        assert Entity(new_name).is_exists() is False, f"{new_name} already exists."
        duplicate_object(self.name, new_name, copy_landmarks)
        return Sketch(
            new_name, curve_type=self.curve_type, description=self.description
        )

    @supported(SupportLevel.PLANNED)
    def create_from_file(self, file_path: "str", file_type: "str| None" = None):
        raise NotImplementedError()
        return self

    @supported(
        SupportLevel.PARTIAL, notes="Options, center_at parameters are not supported."
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
        profile_curve: "WireInterface|SketchInterface| None" = None,
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
        if profile_curve_name:
            if isinstance(profile_curve_name, EntityInterface):
                profile_curve_name = profile_curve_name.name
            apply_curve_modifier(self.name, profile_curve_name)
        update_view_layer()
        return self

    @supported(SupportLevel.PARTIAL, notes="The options parameter is not supported.")
    def create_from_vertices(
        self,
        points: "list[str|list[str]|list[float]|list[Dimension]|Point|VertexInterface]",
    ) -> "WireInterface":
        parsed_points = [
            Point.from_list_of_float_or_string_or_Vertex(point) for point in points
        ]
        is_closed = False
        if len(parsed_points) > 1 and parsed_points[0] == parsed_points[-1]:
            is_closed = True
            parsed_points = parsed_points[:-1]
        blender_spline, curve_data, added_points = create_curve(
            self.name,
            (
                BlenderCurveTypes.from_curve_types(self.curve_type)
                if self.curve_type is not None
                else BlenderCurveTypes.BEZIER
            ),
            parsed_points,
            self.resolution,
            is_3d=False,
            order_u=4,
        )
        wire = get_wire_from_blender_wire(self.get_native_instance(), blender_spline)
        for index, vertex in enumerate(wire.get_vertices()):
            point = points[index]
            if isinstance(point, VertexInterface):
                control_points = point.get_control_points()
                if len(control_points) < 2:
                    # TODO: add a warning message to a logger
                    continue
                vertex.set_control_points(control_points)
        merge_touching_splines(curve=curve_data, reference_spline_index=0)
        if is_closed:
            blender_spline.use_cyclic_u = True
        wire = get_wire_from_blender_wire(
            entity=get_curve(self.name), wire=blender_spline
        )
        update_view_layer()
        return wire

    @supported(SupportLevel.PARTIAL, notes="The Options parameters is not supported.")
    def create_point(
        self, point: "str|list[str]|list[float]|list[Dimension]|Point"
    ) -> "Vertex":
        blender_spline, curve_data, added_points = create_curve(
            curve_name=self.name,
            curve_type=(
                BlenderCurveTypes.from_curve_types(self.curve_type)
                if self.curve_type is not None
                else BlenderCurveTypes.BEZIER
            ),
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

    @supported(
        SupportLevel.PARTIAL,
        notes="The Options parameters is not supported. Returns an Edge entity instead of a Wire.",
    )
    def create_line_to(
        self,
        to: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
    ) -> "WireInterface":
        start_point: Point
        end_point: Point
        if isinstance(start_at, VertexInterface):
            start_point = Point.from_list_of_float_or_string(start_at.location)
        else:
            start_point = Point.from_list_of_float_or_string(start_at)
        if isinstance(to, VertexInterface):
            end_point = Point.from_list_of_float_or_string(to.location)
        else:
            end_point = Point.from_list_of_float_or_string(to)
        blender_spline, curve_data, added_points = create_curve(
            curve_name=self.name,
            curve_type=(
                BlenderCurveTypes.from_curve_types(self.curve_type)
                if self.curve_type is not None
                else BlenderCurveTypes.BEZIER
            ),
            points=[start_point, end_point],
            is_3d=False,
        )
        merge_touching_splines(curve=curve_data, reference_spline_index=0)
        edge = get_edge_from_blender_edge(
            entity=get_curve(self.name), edge=(added_points[0], added_points[1])
        )
        update_view_layer()
        return edge

    @supported(SupportLevel.PLANNED)
    def create_line(
        self,
        length: "str|float|Dimension",
        angle: "str|float|Angle",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
    ) -> "EdgeInterface":
        raise NotImplementedError()

    @staticmethod
    def _set_bezier_circular_handlers(wire: WireInterface, radius: Dimension):
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
            u1 = cmath.asin(p1y / radius.value).real
            u2 = cmath.asin(p2y / radius.value).real
            if p1x > 0 and p2x < 0 or (p1x < 0 and p2x > 0):
                u1 = cmath.acos(p1x / radius.value).real
                u2 = cmath.acos(p2x / radius.value).real
            u = u2 - u1
            if u < 0:
                u = -u
            v1 = mathutils.Vector((p1y * -1, p1x, 0))
            v2 = mathutils.Vector((p2y * -1, p2x, 0))
            v1.normalize()
            v2.normalize()
            length = 4 / 3 * cmath.tan(1 / 4 * u).real * radius.value
            p1.get_native_instance().handle_right = (
                mathutils.Vector((p1x, p1y, 0)) + v1 * length
            )
            p2.get_native_instance().handle_left = (
                mathutils.Vector((p2x, p2y, 0)) - v2 * length
            )
            index += 1

    @supported(
        SupportLevel.PARTIAL,
        notes="center_at and Options are not implemented. This method uses a custom implementation, i.e. not Blender's implementation of creating this shape.",
    )
    def create_circle(
        self,
        radius: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
    ) -> "WireInterface":
        radius = Dimension.from_dimension_or_its_float_or_string_value(radius)
        radius = BlenderLength.convert_dimension_to_blender_unit(radius)
        points = get_circle_points(radius, self.resolution)
        wire: WireInterface = self.create_from_vertices(
            [Point.from_list_of_float_or_string(point) for point in points]
        )
        if self.curve_type == CurveTypes.BEZIER:
            Sketch._set_bezier_circular_handlers(wire, radius)
            set_curve_resolution_u(self.name, 12)
        update_view_layer()
        return wire

    @supported(
        SupportLevel.PARTIAL,
        notes="center_at and Options are not implemented. This method uses a custom implementation, i.e. not Blender's implementation of creating this shape.",
    )
    def create_ellipse(
        self,
        radius_minor: "str|float|Dimension",
        radius_major: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
    ) -> "WireInterface":
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

    @supported(SupportLevel.PARTIAL, notes="The options parameter is not implemented.")
    def create_arc(
        self,
        end_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface",
        radius: "str|float|Dimension",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        flip: "bool| None" = False,
    ) -> "WireInterface":
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
            (
                BlenderCurveTypes.from_curve_types(self.curve_type)
                if self.curve_type is not None
                else BlenderCurveTypes.BEZIER
            ),
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

    @supported(SupportLevel.SUPPORTED)
    def create_rectangle(
        self,
        length: "str|float|Dimension",
        width: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
    ) -> "WireInterface":
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

    @supported(SupportLevel.PLANNED)
    def create_polygon(
        self,
        number_of_sides: "int",
        length: "str|float|Dimension",
        width: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
    ) -> "WireInterface":
        raise NotImplementedError()

    @supported(SupportLevel.PLANNED)
    def create_trapezoid(
        self,
        length_upper: "str|float|Dimension",
        length_lower: "str|float|Dimension",
        height: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
    ) -> "WireInterface":
        raise NotImplementedError()

    @supported(SupportLevel.PLANNED)
    def create_spiral(
        self,
        number_of_turns: "int",
        height: "str|float|Dimension",
        radius: "str|float|Dimension",
        is_clockwise: "bool" = True,
        radius_end: "str|float|Dimension| None" = None,
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
    ) -> "WireInterface":
        raise NotImplementedError()

    @supported(SupportLevel.SUPPORTED)
    def mirror(
        self,
        mirror_across_entity: "EntityInterface",
        axis: "str|int|Axis",
        separate_resulting_entity: "bool| None" = False,
    ):
        implementables.mirror(
            self, mirror_across_entity, axis, resulting_mirrored_entity_name
        )
        return self

    @supported(SupportLevel.SUPPORTED)
    def linear_pattern(
        self,
        instance_count: "int",
        offset: "str|float|Dimension",
        direction_axis: "str|int|Axis" = "z",
    ):
        implementables.linear_pattern(self, instance_count, offset, direction_axis)
        return self

    @supported(SupportLevel.SUPPORTED)
    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "str|float|Angle",
        center_entity_or_landmark: "EntityInterface",
        normal_direction_axis: "str|int|Axis" = "z",
    ):
        implementables.circular_pattern(
            self,
            instance_count,
            separation_angle,
            center_entity_or_landmark,
            normal_direction_axis,
        )
        return self

    @supported(SupportLevel.PLANNED)
    def export(self, file_path: "str", overwrite: "bool" = True, scale: "float" = 1.0):
        implementables.export(self, file_path, overwrite, scale)
        return self

    @supported(SupportLevel.SUPPORTED)
    def scale_xyz(
        self,
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ):
        implementables.scale_xyz(self, x, y, z)
        return self

    @supported(SupportLevel.SUPPORTED)
    def scale_x(self, scale: "str|float|Dimension"):
        implementables.scale_x(self, scale)
        return self

    @supported(SupportLevel.SUPPORTED)
    def scale_y(self, scale: "str|float|Dimension"):
        implementables.scale_y(self, scale)
        return self

    @supported(SupportLevel.SUPPORTED)
    def scale_z(self, scale: "str|float|Dimension"):
        implementables.scale_z(self, scale)
        return self

    @supported(SupportLevel.SUPPORTED)
    def scale_x_by_factor(self, scale_factor: "float"):
        implementables.scale_x_by_factor(self, scale_factor)
        return self

    @supported(SupportLevel.SUPPORTED)
    def scale_y_by_factor(self, scale_factor: "float"):
        implementables.scale_y_by_factor(self, scale_factor)
        return self

    @supported(SupportLevel.SUPPORTED)
    def scale_z_by_factor(self, scale_factor: "float"):
        implementables.scale_z_by_factor(self, scale_factor)
        return self

    @supported(SupportLevel.SUPPORTED)
    def scale_keep_aspect_ratio(
        self, scale: "str|float|Dimension", axis: "str|int|Axis"
    ):
        implementables.scale_keep_aspect_ratio(self, scale, axis)
        return self

    @supported(SupportLevel.SUPPORTED)
    def create_landmark(
        self,
        landmark_name: "str",
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ) -> "LandmarkInterface":
        return implementables.create_landmark(self, landmark_name, x, y, z)

    @supported(SupportLevel.SUPPORTED)
    def get_wires(self) -> "list[WireInterface]":
        return get_wires_from_blender_entity(get_curve(self.name))

    def _translate_child_wires_xyz(
        self,
        x: "str|float|Dimension|None",
        y: "str|float|Dimension|None",
        z: "str|float|Dimension|None",
    ):
        x = Entity._parse_and_convert_dimension_to_blender_units(x) if x else 0
        y = Entity._parse_and_convert_dimension_to_blender_units(y) if y else 0
        z = Entity._parse_and_convert_dimension_to_blender_units(z) if z else 0
        for wire in self.get_wires():
            wire.translate_xyz(x, y, z)
        return self

    @override
    @supported(SupportLevel.SUPPORTED)
    def translate_xyz(
        self,
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ):
        self.set_visible(True)
        return super().translate_xyz(x, y, z)

    @override
    @supported(SupportLevel.SUPPORTED)
    def translate_x(self, amount: "str|float|Dimension"):
        self.set_visible(True)
        return super().translate_x(amount)

    @override
    @supported(SupportLevel.SUPPORTED)
    def translate_y(self, amount: "str|float|Dimension"):
        self.set_visible(True)
        return super().translate_y(amount)

    @override
    @supported(SupportLevel.SUPPORTED)
    def translate_z(self, amount: "str|float|Dimension"):
        self.set_visible(True)
        return super().translate_z(amount)

    @staticmethod
    def _create_blender_object_and_run(func):
        """
        Sketches are normally not added as Objects unless set_visibility(True) is called.
        However, some operations, like rotate, need the object.
        We'll toggle the object just to apply the rotation, then remove it.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            if self.is_visible():
                return func(*args, **kwargs)
            self.set_visible(True)
            value = func(*args, **kwargs)
            self.set_visible(False)
            return value

        return wrapper

    @override
    @_create_blender_object_and_run
    def rotate_xyz(
        self, x: "str|float|Angle", y: "str|float|Angle", z: "str|float|Angle"
    ):
        return super().rotate_xyz(x, y, z)

    @override
    @_create_blender_object_and_run
    @supported(SupportLevel.SUPPORTED)
    def rotate_x(self, rotation: "str|float|Angle"):
        return super().rotate_x(rotation)

    @override
    @_create_blender_object_and_run
    @supported(SupportLevel.SUPPORTED)
    def rotate_y(self, rotation: "str|float|Angle"):
        return super().rotate_y(rotation)

    @override
    @_create_blender_object_and_run
    @supported(SupportLevel.SUPPORTED)
    def rotate_z(self, rotation: "str|float|Angle"):
        return super().rotate_z(rotation)

    @override
    @_create_blender_object_and_run
    @supported(SupportLevel.SUPPORTED)
    def get_bounding_box(self) -> "BoundaryBox":
        return super().get_bounding_box()

    @override
    @_create_blender_object_and_run
    @supported(SupportLevel.SUPPORTED)
    def get_dimensions(self) -> "Dimensions":
        return super().get_dimensions()

    @override
    @_create_blender_object_and_run
    @supported(SupportLevel.SUPPORTED)
    def get_location_world(self) -> "Point":
        return super().get_location_world()

    @override
    @_create_blender_object_and_run
    @supported(SupportLevel.SUPPORTED)
    def get_location_local(self) -> "Point":
        return super().get_location_local()

    @override
    @supported(
        SupportLevel.SUPPORTED,
        notes="Selects the object in the viewport using the object's name",
    )
    def select(self):
        self.set_visible(True)
        return super().get_location_world()

    @override
    def get_landmark(self, landmark_name: "str|PresetLandmark") -> "LandmarkInterface":
        self.set_visible(True)
        return implementables.get_landmark(self, landmark_name)
