from functools import wraps
from typing import Optional

from codetocad.codetocad_types import *
from codetocad.interfaces import SketchInterface
from codetocad.utilities import *

from . import blender_actions, blender_definitions
from .entity import Entity
from .part import Part


class Sketch(Entity, SketchInterface):

    name: str
    curve_type: Optional['CurveTypes'] = None
    description: Optional[str] = None

    def __init__(self, name: str, curve_type: Optional['CurveTypes'] = None, description: Optional[str] = None):
        self.name = name
        self.curve_type = curve_type
        self.description = description

    def clone(self, new_name: str, copy_landmarks: bool = True
              ) -> 'Sketch':

        assert Entity(
            new_name).is_exists() == False, f"{new_name} already exists."

        blender_actions.duplicate_object(self.name, new_name, copy_landmarks)

        return Sketch(new_name, self.curve_type, self.description)

    def revolve(self, angle: AngleOrItsFloatOrStringValue, about_entity_or_landmark: EntityOrItsNameOrLandmark, axis: AxisOrItsIndexOrItsName = "z") -> 'PartInterface':

        if isinstance(about_entity_or_landmark, Entity):
            about_entity_or_landmark = about_entity_or_landmark.name

        axis = Axis.from_string(axis)

        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

        blender_actions.apply_screw_modifier(self.name, Angle.from_string(
            angle).to_radians(), axis, entityNameToDetermineAxis=about_entity_or_landmark)

        blender_actions.create_mesh_from_curve(
            self.name)

        return Part(self.name, self.description).apply()

    def offset(self, radius: DimensionOrItsFloatOrStringValue):

        radius = Dimension.from_string(radius)

        blender_actions.offset_curve_geometry(
            self.name, radius)

        return self

    def extrude(self, length: DimensionOrItsFloatOrStringValue) -> 'PartInterface':

        blender_actions.extrude_curve(
            self.name, Dimension.from_string(length))

        blender_actions.create_mesh_from_curve(
            self.name)

        return Part(self.name, self.description).apply()

    def sweep(self, profile_name_or_instance: SketchOrItsName, fill_cap: bool = True) -> 'PartInterface':
        profile_curve_name = profile_name_or_instance
        if isinstance(profile_curve_name, SketchInterface):
            profile_curve_name = profile_curve_name.name

        blender_actions.add_bevel_object_to_curve(
            self.name, profile_curve_name, fill_cap)

        blender_actions.create_mesh_from_curve(
            self.name)

        # Recalculate normals because they're usually wrong after sweeping.
        blender_actions.recalculate_normals(self.name)

        return Part(self.name, self.description).apply()

    def profile(self,
                profile_curve_name
                ):

        if isinstance(profile_curve_name, Entity):
            profile_curve_name = profile_curve_name.name

        blender_actions.apply_curve_modifier(self.name, profile_curve_name)

        return self

    def create_text(self, text: str, font_size: DimensionOrItsFloatOrStringValue = 1.0, bold: bool = False, italic: bool = False, underlined: bool = False, character_spacing: 'int' = 1, word_spacing: 'int' = 1, line_spacing: 'int' = 1, font_file_path: Optional[str] = None
                    ):
        size = Dimension.from_string(font_size)

        blender_actions.create_text(self.name, text, size, bold, italic, underlined,
                                    character_spacing, word_spacing, line_spacing, font_file_path)
        return self

    def create_from_vertices(self, coordinates: list[PointOrListOfFloatOrItsStringValue], interpolation: 'int' = 64
                             ):
        blender_actions.create_3d_curve(self.name, blender_definitions.BlenderCurveTypes.from_curve_types(
            self.curve_type) if self.curve_type is not None else blender_definitions.BlenderCurveTypes.BEZIER, coordinates, interpolation)

        return self

    @staticmethod
    def _create_primitive_decorator(curve_primitive_type: CurvePrimitiveTypes):
        def decorator(primitiveFunction):

            @wraps(primitiveFunction)
            def wrapper(*args, **kwargs):

                self = args[0]

                blenderCurvePrimitiveType = blender_definitions.BlenderCurvePrimitiveTypes.from_curve_primitive_types(
                    curve_primitive_type)

                blenderPrimitiveFunction = blender_actions.get_blender_curve_primitive_function(
                    blenderCurvePrimitiveType)

                keywordArgs = dict(
                    {
                        "curve_type": blender_definitions.BlenderCurveTypes.from_curve_types(self.curve_type) if self.curve_type is not None else None},
                    **kwargs
                )

                blenderPrimitiveFunction(
                    *args[1:],
                    **keywordArgs
                )

                # Since we're using Blender's bpy.ops API, we cannot provide a name for the newly created object,
                # therefore, we'll use the object's "expected" name and rename it to what it should be
                # note: this will fail if the "expected" name is incorrect
                curve = Sketch(
                    blenderCurvePrimitiveType.name).rename(self.name)

                blender_actions.set_curve_use_path(self.name, False)

                return primitiveFunction(*args, **kwargs)
            return wrapper
        return decorator

    @_create_primitive_decorator(CurvePrimitiveTypes.Point)
    def create_point(self, coordinate: PointOrListOfFloatOrItsStringValue
                     ):
        return self

    @_create_primitive_decorator(CurvePrimitiveTypes.Line)
    def create_line(self, length: DimensionOrItsFloatOrStringValue, angle_x: AngleOrItsFloatOrStringValue = 0.0, angle_y: AngleOrItsFloatOrStringValue = 0.0, symmetric: bool = False
                    ):
        return self

    @_create_primitive_decorator(CurvePrimitiveTypes.LineTo)
    def create_line_between_points(self, end_at: PointOrListOfFloatOrItsStringValue, start_at: Optional[PointOrListOfFloatOrItsStringValue] = None
                                   ):
        return self

    @_create_primitive_decorator(CurvePrimitiveTypes.Circle)
    def create_circle(self, radius: DimensionOrItsFloatOrStringValue
                      ):
        return self

    @_create_primitive_decorator(CurvePrimitiveTypes.Ellipse)
    def create_ellipse(self, radius_a: DimensionOrItsFloatOrStringValue, radius_b: DimensionOrItsFloatOrStringValue
                       ):
        return self

    @_create_primitive_decorator(CurvePrimitiveTypes.Arc)
    def create_arc(self, radius: DimensionOrItsFloatOrStringValue, angle: AngleOrItsFloatOrStringValue = "180d"
                   ):
        return self

    def create_arc_between_three_points(self, point_a: 'Point', point_b: 'Point', center_point: 'Point'
                                        ):
        raise NotImplementedError()
        return self

    @_create_primitive_decorator(CurvePrimitiveTypes.Segment)
    def create_segment(self, inner_radius: DimensionOrItsFloatOrStringValue, outer_radius: DimensionOrItsFloatOrStringValue, angle: AngleOrItsFloatOrStringValue = "180d"
                       ):
        return self

    @_create_primitive_decorator(CurvePrimitiveTypes.Rectangle)
    def create_rectangle(self, length: DimensionOrItsFloatOrStringValue, width: DimensionOrItsFloatOrStringValue
                         ):
        return self

    @_create_primitive_decorator(CurvePrimitiveTypes.Polygon_ab)
    def create_polygon(self, number_of_sides: 'int', length: DimensionOrItsFloatOrStringValue, width: DimensionOrItsFloatOrStringValue
                       ):
        return self

    @_create_primitive_decorator(CurvePrimitiveTypes.Trapezoid)
    def create_trapezoid(self, length_upper: DimensionOrItsFloatOrStringValue, length_lower: DimensionOrItsFloatOrStringValue, height: DimensionOrItsFloatOrStringValue
                         ):
        return self

    @_create_primitive_decorator(CurvePrimitiveTypes.Spiral)
    def create_spiral(self, number_of_turns: 'int', height: DimensionOrItsFloatOrStringValue, radius: DimensionOrItsFloatOrStringValue, is_clockwise: bool = True, radius_end: Optional[DimensionOrItsFloatOrStringValue] = None):

        return self
