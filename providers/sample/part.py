# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *


from codetocad.interfaces.part_interface import PartInterface


from codetocad.interfaces.landmark_interface import LandmarkInterface

from codetocad.interfaces.material_interface import MaterialInterface

from codetocad.interfaces.importable_interface import ImportableInterface

from codetocad.interfaces.booleanable_interface import BooleanableInterface

from codetocad.interfaces.mirrorable_interface import MirrorableInterface

from codetocad.interfaces.scalable_interface import ScalableInterface

from codetocad.interfaces.exportable_interface import ExportableInterface

from codetocad.interfaces.subdividable_interface import SubdividableInterface

from codetocad.interfaces.patternable_interface import PatternableInterface

from codetocad.interfaces.landmarkable_interface import LandmarkableInterface

from codetocad.interfaces.entity_interface import EntityInterface


from codetocad.proxy.landmark import Landmark

from codetocad.proxy.material import Material


from providers.sample.entity import Entity


class Part(PartInterface, Entity):

    def __init__(
        self, name: "str", description: "str| None" = None, native_instance=None
    ):

        self.name = name
        self.description = description
        self.native_instance = native_instance

    def create_cube(
        self,
        width: "str|float|Dimension",
        length: "str|float|Dimension",
        height: "str|float|Dimension",
        keyword_arguments: "dict| None" = None,
    ):

        print(
            "create_cube called", f": {width}, {length}, {height}, {keyword_arguments}"
        )

        return self

    def create_cone(
        self,
        radius: "str|float|Dimension",
        height: "str|float|Dimension",
        draft_radius: "str|float|Dimension" = 0,
        keyword_arguments: "dict| None" = None,
    ):

        print(
            "create_cone called",
            f": {radius}, {height}, {draft_radius}, {keyword_arguments}",
        )

        return self

    def create_cylinder(
        self,
        radius: "str|float|Dimension",
        height: "str|float|Dimension",
        keyword_arguments: "dict| None" = None,
    ):

        print("create_cylinder called", f": {radius}, {height}, {keyword_arguments}")

        return self

    def create_torus(
        self,
        inner_radius: "str|float|Dimension",
        outer_radius: "str|float|Dimension",
        keyword_arguments: "dict| None" = None,
    ):

        print(
            "create_torus called",
            f": {inner_radius}, {outer_radius}, {keyword_arguments}",
        )

        return self

    def create_sphere(
        self, radius: "str|float|Dimension", keyword_arguments: "dict| None" = None
    ):

        print("create_sphere called", f": {radius}, {keyword_arguments}")

        return self

    def create_gear(
        self,
        outer_radius: "str|float|Dimension",
        addendum: "str|float|Dimension",
        inner_radius: "str|float|Dimension",
        dedendum: "str|float|Dimension",
        height: "str|float|Dimension",
        pressure_angle: "str|float|Angle" = "20d",
        number_of_teeth: "int" = 12,
        skew_angle: "str|float|Angle" = 0,
        conical_angle: "str|float|Angle" = 0,
        crown_angle: "str|float|Angle" = 0,
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
        thickness_x: "str|float|Dimension",
        thickness_y: "str|float|Dimension",
        thickness_z: "str|float|Dimension",
        start_axis: "str|int|Axis" = "z",
        flip_axis: "bool" = False,
    ):

        print(
            "hollow called",
            f": {thickness_x}, {thickness_y}, {thickness_z}, {start_axis}, {flip_axis}",
        )

        return self

    def thicken(self, radius: "str|float|Dimension"):

        print("thicken called", f": {radius}")

        return self

    def hole(
        self,
        hole_landmark: "str|LandmarkInterface",
        radius: "str|float|Dimension",
        depth: "str|float|Dimension",
        normal_axis: "str|int|Axis" = "z",
        flip_axis: "bool" = False,
        initial_rotation_x: "str|float|Angle" = 0.0,
        initial_rotation_y: "str|float|Angle" = 0.0,
        initial_rotation_z: "str|float|Angle" = 0.0,
        mirror_about_entity_or_landmark: "str|EntityInterface| None" = None,
        mirror_axis: "str|int|Axis" = "x",
        mirror: "bool" = False,
        circular_pattern_instance_count: "int" = 1,
        circular_pattern_instance_separation: "str|float|Angle" = 0.0,
        circular_pattern_instance_axis: "str|int|Axis" = "z",
        circular_pattern_about_entity_or_landmark: "str|EntityInterface| None" = None,
        linear_pattern_instance_count: "int" = 1,
        linear_pattern_instance_separation: "str|float|Dimension" = 0.0,
        linear_pattern_instance_axis: "str|int|Axis" = "x",
        linear_pattern2nd_instance_count: "int" = 1,
        linear_pattern2nd_instance_separation: "str|float|Dimension" = 0.0,
        linear_pattern2nd_instance_axis: "str|int|Axis" = "y",
    ):

        print(
            "hole called",
            f": {hole_landmark}, {radius}, {depth}, {normal_axis}, {flip_axis}, {initial_rotation_x}, {initial_rotation_y}, {initial_rotation_z}, {mirror_about_entity_or_landmark}, {mirror_axis}, {mirror}, {circular_pattern_instance_count}, {circular_pattern_instance_separation}, {circular_pattern_instance_axis}, {circular_pattern_about_entity_or_landmark}, {linear_pattern_instance_count}, {linear_pattern_instance_separation}, {linear_pattern_instance_axis}, {linear_pattern2nd_instance_count}, {linear_pattern2nd_instance_separation}, {linear_pattern2nd_instance_axis}",
        )

        return self

    def twist(
        self,
        angle: "str|float|Angle",
        screw_pitch: "str|float|Dimension",
        iterations: "int" = 1,
        axis: "str|int|Axis" = "z",
    ):

        print("twist called", f": {angle}, {screw_pitch}, {iterations}, {axis}")

        return self

    def set_material(self, material_name: "str|MaterialInterface"):

        print("set_material called", f": {material_name}")

        return self

    def is_colliding_with_part(self, other_part: "str|PartInterface") -> "bool":

        print("is_colliding_with_part called", f": {other_part}")

        return True

    def fillet_all_edges(
        self, radius: "str|float|Dimension", use_width: "bool" = False
    ):

        print("fillet_all_edges called", f": {radius}, {use_width}")

        return self

    def fillet_edges(
        self,
        radius: "str|float|Dimension",
        landmarks_near_edges: "list[str|LandmarkInterface]",
        use_width: "bool" = False,
    ):

        print("fillet_edges called", f": {radius}, {landmarks_near_edges}, {use_width}")

        return self

    def fillet_faces(
        self,
        radius: "str|float|Dimension",
        landmarks_near_faces: "list[str|LandmarkInterface]",
        use_width: "bool" = False,
    ):

        print("fillet_faces called", f": {radius}, {landmarks_near_faces}, {use_width}")

        return self

    def chamfer_all_edges(self, radius: "str|float|Dimension"):

        print("chamfer_all_edges called", f": {radius}")

        return self

    def chamfer_edges(
        self,
        radius: "str|float|Dimension",
        landmarks_near_edges: "list[str|LandmarkInterface]",
    ):

        print("chamfer_edges called", f": {radius}, {landmarks_near_edges}")

        return self

    def chamfer_faces(
        self,
        radius: "str|float|Dimension",
        landmarks_near_faces: "list[str|LandmarkInterface]",
    ):

        print("chamfer_faces called", f": {radius}, {landmarks_near_faces}")

        return self

    def select_vertex_near_landmark(
        self, landmark_name: "str|LandmarkInterface| None" = None
    ):

        print("select_vertex_near_landmark called", f": {landmark_name}")

        return self

    def select_edge_near_landmark(
        self, landmark_name: "str|LandmarkInterface| None" = None
    ):

        print("select_edge_near_landmark called", f": {landmark_name}")

        return self

    def select_face_near_landmark(
        self, landmark_name: "str|LandmarkInterface| None" = None
    ):

        print("select_face_near_landmark called", f": {landmark_name}")

        return self

    def mirror(
        self,
        mirror_across_entity: "str|EntityInterface",
        axis: "str|int|Axis",
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
        offset: "str|float|Dimension",
        direction_axis: "str|int|Axis" = "z",
    ):

        print(
            "linear_pattern called", f": {instance_count}, {offset}, {direction_axis}"
        )

        return self

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "str|float|Angle",
        center_entity_or_landmark: "str|EntityInterface",
        normal_direction_axis: "str|int|Axis" = "z",
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
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ):

        print("scale_xyz called", f": {x}, {y}, {z}")

        return self

    def scale_x(self, scale: "str|float|Dimension"):

        print("scale_x called", f": {scale}")

        return self

    def scale_y(self, scale: "str|float|Dimension"):

        print("scale_y called", f": {scale}")

        return self

    def scale_z(self, scale: "str|float|Dimension"):

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
        self, scale: "str|float|Dimension", axis: "str|int|Axis"
    ):

        print("scale_keep_aspect_ratio called", f": {scale}, {axis}")

        return self

    def create_landmark(
        self,
        landmark_name: "str",
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ) -> "LandmarkInterface":

        print("create_landmark called", f": {landmark_name}, {x}, {y}, {z}")

        return Landmark("name", "parent")

    def get_landmark(self, landmark_name: "str|PresetLandmark") -> "LandmarkInterface":

        print("get_landmark called", f": {landmark_name}")

        return Landmark("name", "parent")

    def union(
        self,
        other: "str|BooleanableInterface",
        delete_after_union: "bool" = True,
        is_transfer_data: "bool" = False,
    ):

        print("union called", f": {other}, {delete_after_union}, {is_transfer_data}")

        return self

    def subtract(
        self,
        other: "str|BooleanableInterface",
        delete_after_subtract: "bool" = True,
        is_transfer_data: "bool" = False,
    ):

        print(
            "subtract called", f": {other}, {delete_after_subtract}, {is_transfer_data}"
        )

        return self

    def intersect(
        self,
        other: "str|BooleanableInterface",
        delete_after_intersect: "bool" = True,
        is_transfer_data: "bool" = False,
    ):

        print(
            "intersect called",
            f": {other}, {delete_after_intersect}, {is_transfer_data}",
        )

        return self
