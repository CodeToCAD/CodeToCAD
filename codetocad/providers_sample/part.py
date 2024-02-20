# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from codetocad.interfaces import PartInterface


from codetocad.interfaces.material_interface import MaterialInterface

from codetocad.interfaces.entity_interface import EntityInterface

from codetocad.interfaces.landmark_interface import LandmarkInterface


from codetocad.providers_sample.material import Material

from codetocad.providers_sample.entity import Entity

from codetocad.providers_sample.landmark import Landmark


class Part(PartInterface, Entity):
    def create_cube(
        self,
        width: "DimensionOrItsFloatOrStringValue",
        length: "DimensionOrItsFloatOrStringValue",
        height: "DimensionOrItsFloatOrStringValue",
        keyword_arguments: "dict| None" = None,
    ):
        print(
            "create_cube called", f": {width}, {length}, {height}, {keyword_arguments}"
        )

        return self

    def create_cone(
        self,
        radius: "DimensionOrItsFloatOrStringValue",
        height: "DimensionOrItsFloatOrStringValue",
        draft_radius: "DimensionOrItsFloatOrStringValue" = 0,
        keyword_arguments: "dict| None" = None,
    ):
        print(
            "create_cone called",
            f": {radius}, {height}, {draft_radius}, {keyword_arguments}",
        )

        return self

    def create_cylinder(
        self,
        radius: "DimensionOrItsFloatOrStringValue",
        height: "DimensionOrItsFloatOrStringValue",
        keyword_arguments: "dict| None" = None,
    ):
        print("create_cylinder called", f": {radius}, {height}, {keyword_arguments}")

        return self

    def create_torus(
        self,
        inner_radius: "DimensionOrItsFloatOrStringValue",
        outer_radius: "DimensionOrItsFloatOrStringValue",
        keyword_arguments: "dict| None" = None,
    ):
        print(
            "create_torus called",
            f": {inner_radius}, {outer_radius}, {keyword_arguments}",
        )

        return self

    def create_sphere(
        self,
        radius: "DimensionOrItsFloatOrStringValue",
        keyword_arguments: "dict| None" = None,
    ):
        print("create_sphere called", f": {radius}, {keyword_arguments}")

        return self

    def create_gear(
        self,
        outer_radius: "DimensionOrItsFloatOrStringValue",
        addendum: "DimensionOrItsFloatOrStringValue",
        inner_radius: "DimensionOrItsFloatOrStringValue",
        dedendum: "DimensionOrItsFloatOrStringValue",
        height: "DimensionOrItsFloatOrStringValue",
        pressure_angle: "AngleOrItsFloatOrStringValue" = "20d",
        number_of_teeth: "int" = 12,
        skew_angle: "AngleOrItsFloatOrStringValue" = 0,
        conical_angle: "AngleOrItsFloatOrStringValue" = 0,
        crown_angle: "AngleOrItsFloatOrStringValue" = 0,
        keyword_arguments: "dict| None" = None,
    ):
        print(
            "create_gear called",
            f": {outer_radius}, {addendum}, {inner_radius}, {dedendum}, {height}, {pressure_angle}, {number_of_teeth}, {skew_angle}, {conical_angle}, {crown_angle}, {keyword_arguments}",
        )

        return self

    def clone(self, new_name: "str", copy_landmarks: "bool" = True) -> "PartInterface":
        print("clone called", f": {new_name}, {copy_landmarks}")

        return Part("a part")

    def hollow(
        self,
        thickness_x: "DimensionOrItsFloatOrStringValue",
        thickness_y: "DimensionOrItsFloatOrStringValue",
        thickness_z: "DimensionOrItsFloatOrStringValue",
        start_axis: "AxisOrItsIndexOrItsName" = "z",
        flip_axis: "bool" = False,
    ):
        print(
            "hollow called",
            f": {thickness_x}, {thickness_y}, {thickness_z}, {start_axis}, {flip_axis}",
        )

        return self

    def thicken(self, radius: "DimensionOrItsFloatOrStringValue"):
        print("thicken called", f": {radius}")

        return self

    def hole(
        self,
        hole_landmark: "LandmarkOrItsName",
        radius: "DimensionOrItsFloatOrStringValue",
        depth: "DimensionOrItsFloatOrStringValue",
        normal_axis: "AxisOrItsIndexOrItsName" = "z",
        flip_axis: "bool" = False,
        initial_rotation_x: "AngleOrItsFloatOrStringValue" = 0.0,
        initial_rotation_y: "AngleOrItsFloatOrStringValue" = 0.0,
        initial_rotation_z: "AngleOrItsFloatOrStringValue" = 0.0,
        mirror_about_entity_or_landmark: "EntityOrItsName| None" = None,
        mirror_axis: "AxisOrItsIndexOrItsName" = "x",
        mirror: "bool" = False,
        circular_pattern_instance_count: "int" = 1,
        circular_pattern_instance_separation: "AngleOrItsFloatOrStringValue" = 0.0,
        circular_pattern_instance_axis: "AxisOrItsIndexOrItsName" = "z",
        circular_pattern_about_entity_or_landmark: "EntityOrItsName| None" = None,
        linear_pattern_instance_count: "int" = 1,
        linear_pattern_instance_separation: "DimensionOrItsFloatOrStringValue" = 0.0,
        linear_pattern_instance_axis: "AxisOrItsIndexOrItsName" = "x",
        linear_pattern2nd_instance_count: "int" = 1,
        linear_pattern2nd_instance_separation: "DimensionOrItsFloatOrStringValue" = 0.0,
        linear_pattern2nd_instance_axis: "AxisOrItsIndexOrItsName" = "y",
    ):
        print(
            "hole called",
            f": {hole_landmark}, {radius}, {depth}, {normal_axis}, {flip_axis}, {initial_rotation_x}, {initial_rotation_y}, {initial_rotation_z}, {mirror_about_entity_or_landmark}, {mirror_axis}, {mirror}, {circular_pattern_instance_count}, {circular_pattern_instance_separation}, {circular_pattern_instance_axis}, {circular_pattern_about_entity_or_landmark}, {linear_pattern_instance_count}, {linear_pattern_instance_separation}, {linear_pattern_instance_axis}, {linear_pattern2nd_instance_count}, {linear_pattern2nd_instance_separation}, {linear_pattern2nd_instance_axis}",
        )

        return self

    def twist(
        self,
        angle: "AngleOrItsFloatOrStringValue",
        screw_pitch: "DimensionOrItsFloatOrStringValue",
        iterations: "int" = 1,
        axis: "AxisOrItsIndexOrItsName" = "z",
    ):
        print("twist called", f": {angle}, {screw_pitch}, {iterations}, {axis}")

        return self

    def set_material(self, material_name: "MaterialOrItsName"):
        print("set_material called", f": {material_name}")

        return self

    def is_colliding_with_part(self, other_part: "PartOrItsName") -> "bool":
        print("is_colliding_with_part called", f": {other_part}")

        return True

    def fillet_all_edges(
        self, radius: "DimensionOrItsFloatOrStringValue", use_width: "bool" = False
    ):
        print("fillet_all_edges called", f": {radius}, {use_width}")

        return self

    def fillet_edges(
        self,
        radius: "DimensionOrItsFloatOrStringValue",
        landmarks_near_edges: "list[LandmarkOrItsName]",
        use_width: "bool" = False,
    ):
        print("fillet_edges called", f": {radius}, {landmarks_near_edges}, {use_width}")

        return self

    def fillet_faces(
        self,
        radius: "DimensionOrItsFloatOrStringValue",
        landmarks_near_faces: "list[LandmarkOrItsName]",
        use_width: "bool" = False,
    ):
        print("fillet_faces called", f": {radius}, {landmarks_near_faces}, {use_width}")

        return self

    def chamfer_all_edges(self, radius: "DimensionOrItsFloatOrStringValue"):
        print("chamfer_all_edges called", f": {radius}")

        return self

    def chamfer_edges(
        self,
        radius: "DimensionOrItsFloatOrStringValue",
        landmarks_near_edges: "list[LandmarkOrItsName]",
    ):
        print("chamfer_edges called", f": {radius}, {landmarks_near_edges}")

        return self

    def chamfer_faces(
        self,
        radius: "DimensionOrItsFloatOrStringValue",
        landmarks_near_faces: "list[LandmarkOrItsName]",
    ):
        print("chamfer_faces called", f": {radius}, {landmarks_near_faces}")

        return self

    def select_vertex_near_landmark(
        self, landmark_name: "LandmarkOrItsName| None" = None
    ):
        print("select_vertex_near_landmark called", f": {landmark_name}")

        return self

    def select_edge_near_landmark(
        self, landmark_name: "LandmarkOrItsName| None" = None
    ):
        print("select_edge_near_landmark called", f": {landmark_name}")

        return self

    def select_face_near_landmark(
        self, landmark_name: "LandmarkOrItsName| None" = None
    ):
        print("select_face_near_landmark called", f": {landmark_name}")

        return self

    def mirror(
        self,
        mirror_across_entity: "EntityOrItsName",
        axis: "AxisOrItsIndexOrItsName",
        resulting_mirrored_entity_name: "str| None" = None,
    ):
        print(
            "mirror called",
            f": {mirror_across_entity}, {axis}, {resulting_mirrored_entity_name}",
        )

        return self

    def linear_pattern(
        self,
        instance_count: "int",
        offset: "DimensionOrItsFloatOrStringValue",
        direction_axis: "AxisOrItsIndexOrItsName" = "z",
    ):
        print(
            "linear_pattern called", f": {instance_count}, {offset}, {direction_axis}"
        )

        return self

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "AngleOrItsFloatOrStringValue",
        center_entity_or_landmark: "EntityOrItsName",
        normal_direction_axis: "AxisOrItsIndexOrItsName" = "z",
    ):
        print(
            "circular_pattern called",
            f": {instance_count}, {separation_angle}, {center_entity_or_landmark}, {normal_direction_axis}",
        )

        return self

    def remesh(self, strategy: "str", amount: "float"):
        print("remesh called", f": {strategy}, {amount}")

        return self

    def subdivide(self, amount: "float"):
        print("subdivide called", f": {amount}")

        return self

    def decimate(self, amount: "float"):
        print("decimate called", f": {amount}")

        return self

    def create_from_file(self, file_path: "str", file_type: "str| None" = None):
        print("create_from_file called", f": {file_path}, {file_type}")

        return self

    def export(self, file_path: "str", overwrite: "bool" = True, scale: "float" = 1.0):
        print("export called", f": {file_path}, {overwrite}, {scale}")

        return self

    def scale_xyz(
        self,
        x: "DimensionOrItsFloatOrStringValue",
        y: "DimensionOrItsFloatOrStringValue",
        z: "DimensionOrItsFloatOrStringValue",
    ):
        print("scale_xyz called", f": {x}, {y}, {z}")

        return self

    def scale_x(self, scale: "DimensionOrItsFloatOrStringValue"):
        print("scale_x called", f": {scale}")

        return self

    def scale_y(self, scale: "DimensionOrItsFloatOrStringValue"):
        print("scale_y called", f": {scale}")

        return self

    def scale_z(self, scale: "DimensionOrItsFloatOrStringValue"):
        print("scale_z called", f": {scale}")

        return self

    def scale_x_by_factor(self, scale_factor: "float"):
        print("scale_x_by_factor called", f": {scale_factor}")

        return self

    def scale_y_by_factor(self, scale_factor: "float"):
        print("scale_y_by_factor called", f": {scale_factor}")

        return self

    def scale_z_by_factor(self, scale_factor: "float"):
        print("scale_z_by_factor called", f": {scale_factor}")

        return self

    def scale_keep_aspect_ratio(
        self, scale: "DimensionOrItsFloatOrStringValue", axis: "AxisOrItsIndexOrItsName"
    ):
        print("scale_keep_aspect_ratio called", f": {scale}, {axis}")

        return self

    def create_landmark(
        self,
        landmark_name: "str",
        x: "DimensionOrItsFloatOrStringValue",
        y: "DimensionOrItsFloatOrStringValue",
        z: "DimensionOrItsFloatOrStringValue",
    ) -> "LandmarkInterface":
        print("create_landmark called", f": {landmark_name}, {x}, {y}, {z}")

        return Landmark("name", "parent")

    def get_landmark(
        self, landmark_name: "PresetLandmarkOrItsName"
    ) -> "LandmarkInterface":
        print("get_landmark called", f": {landmark_name}")

        return Landmark("name", "parent")

    def union(
        self,
        other: "BooleanableOrItsName",
        delete_after_union: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        print("union called", f": {other}, {delete_after_union}, {is_transfer_data}")

        return self

    def subtract(
        self,
        other: "BooleanableOrItsName",
        delete_after_subtract: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        print(
            "subtract called", f": {other}, {delete_after_subtract}, {is_transfer_data}"
        )

        return self

    def intersect(
        self,
        other: "BooleanableOrItsName",
        delete_after_intersect: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        print(
            "intersect called",
            f": {other}, {delete_after_intersect}, {is_transfer_data}",
        )

        return self
