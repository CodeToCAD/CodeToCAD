# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from codetocad.interfaces import PartInterface

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from . import Entity

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Landmark
    from . import Entity
    from . import Material


class Part(Entity, PartInterface):
    def mirror(
        self,
        mirror_across_entity: EntityOrItsName,
        axis: AxisOrItsIndexOrItsName,
        resulting_mirrored_entity_name: Optional[str] = None,
    ):
        print(
            "mirror called:", mirror_across_entity, axis, resulting_mirrored_entity_name
        )
        return self

    def linear_pattern(
        self,
        instance_count: "int",
        offset: DimensionOrItsFloatOrStringValue,
        direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        print("linear_pattern called:", instance_count, offset, direction_axis)
        return self

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: AngleOrItsFloatOrStringValue,
        center_entity_or_landmark: EntityOrItsName,
        normal_direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        print(
            "circular_pattern called:",
            instance_count,
            separation_angle,
            center_entity_or_landmark,
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
        print("scale_xyz called:", x, y, z)
        return self

    def scale_x(self, scale: DimensionOrItsFloatOrStringValue):
        print("scale_x called:", scale)
        return self

    def scale_y(self, scale: DimensionOrItsFloatOrStringValue):
        print("scale_y called:", scale)
        return self

    def scale_z(self, scale: DimensionOrItsFloatOrStringValue):
        print("scale_z called:", scale)
        return self

    def scale_x_by_factor(self, scale_factor: float):
        print("scale_x_by_factor called:", scale_factor)
        return self

    def scale_y_by_factor(self, scale_factor: float):
        print("scale_y_by_factor called:", scale_factor)
        return self

    def scale_z_by_factor(self, scale_factor: float):
        print("scale_z_by_factor called:", scale_factor)
        return self

    def scale_keep_aspect_ratio(
        self, scale: DimensionOrItsFloatOrStringValue, axis: AxisOrItsIndexOrItsName
    ):
        print("scale_keep_aspect_ratio called:", scale, axis)
        return self

    def create_cube(
        self,
        width: DimensionOrItsFloatOrStringValue,
        length: DimensionOrItsFloatOrStringValue,
        height: DimensionOrItsFloatOrStringValue,
        keyword_arguments: Optional[dict] = None,
    ):
        print("create_cube called:", width, length, height, keyword_arguments)
        return self

    def create_cone(
        self,
        radius: DimensionOrItsFloatOrStringValue,
        height: DimensionOrItsFloatOrStringValue,
        draft_radius: DimensionOrItsFloatOrStringValue = 0,
        keyword_arguments: Optional[dict] = None,
    ):
        print("create_cone called:", radius, height, draft_radius, keyword_arguments)
        return self

    def create_cylinder(
        self,
        radius: DimensionOrItsFloatOrStringValue,
        height: DimensionOrItsFloatOrStringValue,
        keyword_arguments: Optional[dict] = None,
    ):
        print("create_cylinder called:", radius, height, keyword_arguments)
        return self

    def create_torus(
        self,
        inner_radius: DimensionOrItsFloatOrStringValue,
        outer_radius: DimensionOrItsFloatOrStringValue,
        keyword_arguments: Optional[dict] = None,
    ):
        print("create_torus called:", inner_radius, outer_radius, keyword_arguments)
        return self

    def create_sphere(
        self,
        radius: DimensionOrItsFloatOrStringValue,
        keyword_arguments: Optional[dict] = None,
    ):
        print("create_sphere called:", radius, keyword_arguments)
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
        print("clone called:", new_name, copy_landmarks)
        from . import Part

        return Part("a part")

    def union(
        self,
        with_part: PartOrItsName,
        delete_after_union: bool = True,
        is_transfer_landmarks: bool = False,
    ):
        print("union called:", with_part, delete_after_union, is_transfer_landmarks)
        return self

    def subtract(
        self,
        with_part: PartOrItsName,
        delete_after_subtract: bool = True,
        is_transfer_landmarks: bool = False,
    ):
        print(
            "subtract called:", with_part, delete_after_subtract, is_transfer_landmarks
        )
        return self

    def intersect(
        self,
        with_part: PartOrItsName,
        delete_after_intersect: bool = True,
        is_transfer_landmarks: bool = False,
    ):
        print(
            "intersect called:",
            with_part,
            delete_after_intersect,
            is_transfer_landmarks,
        )
        return self

    def hollow(
        self,
        thickness_x: DimensionOrItsFloatOrStringValue,
        thickness_y: DimensionOrItsFloatOrStringValue,
        thickness_z: DimensionOrItsFloatOrStringValue,
        start_axis: AxisOrItsIndexOrItsName = "z",
        flip_axis: bool = False,
    ):
        print(
            "hollow called:",
            thickness_x,
            thickness_y,
            thickness_z,
            start_axis,
            flip_axis,
        )
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
        print(
            "hole called:",
            hole_landmark,
            radius,
            depth,
            normal_axis,
            flip_axis,
            initial_rotation_x,
            initial_rotation_y,
            initial_rotation_z,
            mirror_about_entity_or_landmark,
            mirror_axis,
            mirror,
            circular_pattern_instance_count,
            circular_pattern_instance_separation,
            circular_pattern_instance_axis,
            circular_pattern_about_entity_or_landmark,
            linear_pattern_instance_count,
            linear_pattern_instance_separation,
            linear_pattern_instance_axis,
            linear_pattern2nd_instance_count,
            linear_pattern2nd_instance_separation,
            linear_pattern2nd_instance_axis,
        )
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
        print("set_material called:", material_name)
        return self

    def is_colliding_with_part(self, other_part: PartOrItsName) -> bool:
        print("is_colliding_with_part called:", other_part)
        return True

    def fillet_all_edges(
        self, radius: DimensionOrItsFloatOrStringValue, use_width: bool = False
    ):
        print("fillet_all_edges called:", radius, use_width)
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
        print("chamfer_all_edges called:", radius)
        return self

    def chamfer_edges(
        self,
        radius: DimensionOrItsFloatOrStringValue,
        landmarks_near_edges: list[LandmarkOrItsName],
    ):
        print("chamfer_edges called:", radius, landmarks_near_edges)
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
