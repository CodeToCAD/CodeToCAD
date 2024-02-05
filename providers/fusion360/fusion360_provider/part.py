from typing import Optional
from adsk.fusion import adsk

from codetocad.interfaces import PartInterface

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *
from .fusion_actions.actions import create_circular_pattern, create_rectangular_pattern, mirror
from .fusion_actions.fusion_sketch import FusionSketch

from .fusion_actions.base import delete_occurrence
from .fusion_actions.curve import make_arc, make_circle, make_lines, make_rectangle
from .fusion_actions.modifiers import make_loft, make_revolve

from .fusion_actions.fusion_body import FusionBody

from . import Entity

from .fusion_actions.common import (
    chamfer_all_edges,
    combine,
    fillet_all_edges,
    hole,
    hollow,
    intersect,
    make_point3d,
    set_material,
    subtract,
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Landmark
    from . import Entity
    from . import Material


class Part(Entity, PartInterface):
    def __init__(self, name: str):
        self.fusion_body = FusionBody(name)
        self.name = name


    def mirror(
        self,
        mirror_across_entity: EntityOrItsName,
        axis: AxisOrItsIndexOrItsName,
        resulting_mirrored_entity_name: Optional[str] = None,
    ):
        body, newPosition = mirror(self.fusion_body, mirror_across_entity.center, axis)
        part = self.__class__(body.name)
        part.fusion_body.instance = body
        part.translate_xyz(newPosition.x, newPosition.y, newPosition.z)
        return self

    def linear_pattern(
        self,
        instance_count: "int",
        offset: DimensionOrItsFloatOrStringValue,
        direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        create_rectangular_pattern(
            self.fusion_body.component,
            instance_count,
            offset,
            direction_axis
        )
        return self

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: AngleOrItsFloatOrStringValue,
        center_entity_or_landmark: EntityOrItsName,
        normal_direction_axis: AxisOrItsIndexOrItsName = "z",
    ):

        # sketch it's not moved
        center = center_entity_or_landmark.center
        create_circular_pattern(
            self.fusion_body.component,
            self.fusion_body.instance,
            center,
            instance_count,
            separation_angle,
            normal_direction_axis,
        )

        return self

    def remesh(self, strategy: str, amount: float):
        print("remesh called:", strategy, amount)
        return self

    def subdivide(self, amount: float):
        print("subdivide called:", amount)
        return self

    def decimate(self, amount: float):
        print("decimate called:", amount)
        return self

    def create_from_file(self, file_path: str, file_type: Optional[str] = None):
        print("create_from_file called:", file_path, file_type)
        return self

    def export(self, file_path: str, overwrite: bool = True, scale: float = 1.0):
        print("export called:", file_path, overwrite, scale)
        return self

    def scale_xyz(
        self,
        x: DimensionOrItsFloatOrStringValue,
        y: DimensionOrItsFloatOrStringValue,
        z: DimensionOrItsFloatOrStringValue,
    ):
        self.fusion_body.scale(x, y, z)
        return self

    def scale_x(self, scale: DimensionOrItsFloatOrStringValue):
        self.fusion_body.scale(scale, 0, 0)
        return self

    def scale_y(self, scale: DimensionOrItsFloatOrStringValue):
        self.fusion_body.scale(0, scale, 0)
        return self

    def scale_z(self, scale: DimensionOrItsFloatOrStringValue):
        self.fusion_body.scale(0, 0, scale)
        return self

    def scale_x_by_factor(self, scale_factor: float):
        self.fusion_body.scale_by_factor(scale_factor, 1, 1)
        return self

    def scale_y_by_factor(self, scale_factor: float):
        self.fusion_body.scale_by_factor(1, scale_factor, 1)
        return self

    def scale_z_by_factor(self, scale_factor: float):
        self.fusion_body.scale_by_factor(1, 1, scale_factor)
        return self

    def scale_keep_aspect_ratio(
        self, scale: DimensionOrItsFloatOrStringValue, axis: AxisOrItsIndexOrItsName
    ):
        self.fusion_body.scale_uniform(scale)
        return self

    def create_cube(
        self,
        width: DimensionOrItsFloatOrStringValue,
        length: DimensionOrItsFloatOrStringValue,
        height: DimensionOrItsFloatOrStringValue,
        keyword_arguments: Optional[dict] = None,
    ):
        sketch = FusionSketch(self.fusion_body.sketch.name)
        _ = make_rectangle(sketch.instance, width, length)
        self.fusion_body.instance = sketch.extrude(height)

        return self

    def create_cone(
        self,
        radius: DimensionOrItsFloatOrStringValue,
        height: DimensionOrItsFloatOrStringValue,
        draft_radius: DimensionOrItsFloatOrStringValue = 0,
        keyword_arguments: Optional[dict] = None,
    ):
        from . import Sketch

        if draft_radius == Dimension(0):
            import math

            points = [
                make_point3d(0, 0, 0),
                make_point3d(0, 0, height),
                make_point3d(radius, 0, 0),
                make_point3d(0, 0, 0),
            ]

            _ = make_lines(self.fusion_body.sketch, points)
            self.fusion_body.instance = make_revolve(
                self.fusion_body.component,
                self.fusion_body.sketch,
                math.pi * 2,
                "Entity",
                "z"
            )
        else:
            base = Sketch(self.fusion_body.sketch.name + "_temp_base")
            _ = base.create_circle(radius)

            top = Sketch(self.fusion_body.sketch.name + "_temp_top")
            _ = top.create_circle(draft_radius)
            top.translate_z(height)

            self.fusion_body.instance = make_loft(
                self.fusion_body.component,
                base.fusion_sketch.instance,
                top.fusion_sketch.instance
            )

            delete_occurrence(base.fusion_sketch.instance.name)
            delete_occurrence(top.fusion_sketch.instance.name)

        return self

    def create_cylinder(
        self,
        radius: DimensionOrItsFloatOrStringValue,
        height: DimensionOrItsFloatOrStringValue,
        keyword_arguments: Optional[dict] = None,
    ):
        from . import Sketch

        sketch = FusionSketch(self.fusion_body.sketch.name)
        _ = make_circle(sketch.instance, radius, 4)
        self.fusion_body.instance = sketch.extrude(height)

        return self

    def create_torus(
        self,
        inner_radius: DimensionOrItsFloatOrStringValue,
        outer_radius: DimensionOrItsFloatOrStringValue,
        keyword_arguments: Optional[dict] = None,
    ):
        from . import Sketch
        import math

        inner_radius = Dimension.from_dimension_or_its_float_or_string_value(
            inner_radius
        )
        outer_radius = Dimension.from_dimension_or_its_float_or_string_value(
            outer_radius
        )

        sketch = Sketch(self.fusion_body.sketch.name).fusion_sketch.instance

        circles = sketch.sketchCurves.sketchCircles
        _ = circles.addByCenterRadius(
            adsk.core.Point3D.create(0, 0, 0), inner_radius.value
        )

        # this should be a landmark
        # lines = sketch.sketchCurves.sketchLines
        # axisLine = lines.addByTwoPoints(
        #     adsk.core.Point3D.create(-inner_radius.value, -outer_radius.value, 0),
        #     adsk.core.Point3D.create(inner_radius.value, -outer_radius.value, 0),
        # )

        self.fusion_body.instance = make_revolve(
            self.fusion_body.component,
            sketch,
            math.pi * 2,
            "",
            "x",
        )

        return self

    def create_sphere(
        self,
        radius: DimensionOrItsFloatOrStringValue,
        keyword_arguments: Optional[dict] = None,
    ):
        from . import Sketch
        import math

        radius = Dimension.from_dimension_or_its_float_or_string_value(
            radius
        )

        start = make_point3d(radius.value, 0, 0)
        end = make_point3d(-radius.value, 0, 0)

        sketch = Sketch(self.fusion_body.sketch.name)

        make_arc(sketch.fusion_sketch.instance, start, end, radius.value, True)

        self.fusion_body.instance = make_revolve(
            self.fusion_body.component,
            sketch.fusion_sketch.instance,
            math.pi * 2,
            "",
            "x",
        )

        return self

    def create_gear(
        self,
        outer_radius: DimensionOrItsFloatOrStringValue,
        addendum: DimensionOrItsFloatOrStringValue,
        inner_radius: DimensionOrItsFloatOrStringValue,
        dedendum: DimensionOrItsFloatOrStringValue,
        height: DimensionOrItsFloatOrStringValue,
        pressure_angle: AngleOrItsFloatOrStringValue = "20d",
        number_of_teeth: "int" = 12,
        skew_angle: AngleOrItsFloatOrStringValue = 0,
        conical_angle: AngleOrItsFloatOrStringValue = 0,
        crown_angle: AngleOrItsFloatOrStringValue = 0,
        keyword_arguments: Optional[dict] = None,
    ):
        print(
            "create_gear called:",
            outer_radius,
            addendum,
            inner_radius,
            dedendum,
            height,
            pressure_angle,
            number_of_teeth,
            skew_angle,
            conical_angle,
            crown_angle,
            keyword_arguments,
        )
        return self

    def clone(self, new_name: str, copy_landmarks: bool = True) -> "Part":
        body = self.fusion_body.clone(new_name, copy_landmarks)
        return Part(body.name)


    def union(
        self,
        with_part: PartOrItsName,
        delete_after_union: bool = True,
        is_transfer_landmarks: bool = False,
    ):
        combine(self.name, with_part)
        return self

    def subtract(
        self,
        with_part: PartOrItsName,
        delete_after_subtract: bool = True,
        is_transfer_landmarks: bool = False,
    ):
        subtract(self.name, with_part)
        return self

    def intersect(
        self,
        with_part: PartOrItsName,
        delete_after_intersect: bool = True,
        is_transfer_landmarks: bool = False,
    ):
        intersect(self.name, with_part, delete_after_intersect)
        return self

    def hollow(
        self,
        thickness_x: DimensionOrItsFloatOrStringValue,
        thickness_y: DimensionOrItsFloatOrStringValue,
        thickness_z: DimensionOrItsFloatOrStringValue,
        start_axis: AxisOrItsIndexOrItsName = "z",
        flip_axis: bool = False,
    ):
        hollow(self.name, thickness_x)
        return self

    def thicken(self, radius: DimensionOrItsFloatOrStringValue):
        print("thicken called:", radius)
        return self

    def hole(
        self,
        hole_landmark: LandmarkOrItsName,
        radius: DimensionOrItsFloatOrStringValue,
        depth: DimensionOrItsFloatOrStringValue,
        normal_axis: AxisOrItsIndexOrItsName = "z",
        flip_axis: bool = False,
        initial_rotation_x: AngleOrItsFloatOrStringValue = 0.0,
        initial_rotation_y: AngleOrItsFloatOrStringValue = 0.0,
        initial_rotation_z: AngleOrItsFloatOrStringValue = 0.0,
        mirror_about_entity_or_landmark: Optional[EntityOrItsName] = None,
        mirror_axis: AxisOrItsIndexOrItsName = "x",
        mirror: bool = False,
        circular_pattern_instance_count: "int" = 1,
        circular_pattern_instance_separation: AngleOrItsFloatOrStringValue = 0.0,
        circular_pattern_instance_axis: AxisOrItsIndexOrItsName = "z",
        circular_pattern_about_entity_or_landmark: Optional[EntityOrItsName] = None,
        linear_pattern_instance_count: "int" = 1,
        linear_pattern_instance_separation: DimensionOrItsFloatOrStringValue = 0.0,
        linear_pattern_instance_axis: AxisOrItsIndexOrItsName = "x",
        linear_pattern2nd_instance_count: "int" = 1,
        linear_pattern2nd_instance_separation: DimensionOrItsFloatOrStringValue = 0.0,
        linear_pattern2nd_instance_axis: AxisOrItsIndexOrItsName = "y",
    ):
        # hardcoded because I need to figure out how to get that information
        # @check: implement Landmark.py
        hole(self.name, Point(0.5, 1, 6.0), radius, depth)
        return self

    def twist(
        self,
        angle: AngleOrItsFloatOrStringValue,
        screw_pitch: DimensionOrItsFloatOrStringValue,
        iterations: "int" = 1,
        axis: AxisOrItsIndexOrItsName = "z",
    ):
        print("twist called:", angle, screw_pitch, iterations, axis)
        return self

    def set_material(self, material_name: MaterialOrItsName):
        set_material(self.name, material_name)
        return self

    def is_colliding_with_part(self, other_part: PartOrItsName) -> bool:
        print("is_colliding_with_part called:", other_part)
        return True

    def fillet_all_edges(
        self, radius: DimensionOrItsFloatOrStringValue, use_width: bool = False
    ):
        fillet_all_edges(self.name, radius)
        return self

    def fillet_edges(
        self,
        radius: DimensionOrItsFloatOrStringValue,
        landmarks_near_edges: list[LandmarkOrItsName],
        use_width: bool = False,
    ):
        print("fillet_edges called:", radius, landmarks_near_edges, use_width)
        return self

    def fillet_faces(
        self,
        radius: DimensionOrItsFloatOrStringValue,
        landmarks_near_faces: list[LandmarkOrItsName],
        use_width: bool = False,
    ):
        print("fillet_faces called:", radius, landmarks_near_faces, use_width)
        return self

    def chamfer_all_edges(self, radius: DimensionOrItsFloatOrStringValue):
        chamfer_all_edges(self.name, radius)
        return self

    def chamfer_edges(
        self,
        radius: DimensionOrItsFloatOrStringValue,
        landmarks_near_edges: list[LandmarkOrItsName],
    ):
        return self

    def chamfer_faces(
        self,
        radius: DimensionOrItsFloatOrStringValue,
        landmarks_near_faces: list[LandmarkOrItsName],
    ):
        print("chamfer_faces called:", radius, landmarks_near_faces)
        return self

    def select_vertex_near_landmark(
        self, landmark_name: Optional[LandmarkOrItsName] = None
    ):
        print("select_vertex_near_landmark called:", landmark_name)
        return self

    def select_edge_near_landmark(
        self, landmark_name: Optional[LandmarkOrItsName] = None
    ):
        print("select_edge_near_landmark called:", landmark_name)
        return self

    def select_face_near_landmark(
        self, landmark_name: Optional[LandmarkOrItsName] = None
    ):
        print("select_face_near_landmark called:", landmark_name)
        return self
