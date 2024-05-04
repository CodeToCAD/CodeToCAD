from codetocad.interfaces.part_interface import PartInterface
from codetocad.interfaces.landmark_interface import LandmarkInterface
from providers.onshape.onshape_provider.material import Material
from providers.onshape.onshape_provider.entity import Entity
from providers.onshape.onshape_provider.landmark import Landmark
from codetocad.codetocad_types import *
from . import Entity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Landmark
    from . import Entity
    from . import Material


class Part(PartInterface, Entity):
    def __init__(
        self, name: "str", description: "str| None" = None, native_instance=None
    ):
        self.name = name
        self.description = description
        self.native_instance = native_instance

    def mirror(
        self,
        mirror_across_entity: "str|Entity",
        axis: "str|int|Axis",
        resulting_mirrored_entity_name: "str| None" = None,
    ):
        return self

    def linear_pattern(
        self,
        instance_count: "int",
        offset: "str|float|Dimension",
        direction_axis: "str|int|Axis" = "z",
    ):
        return self

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "str|float|Angle",
        center_entity_or_landmark: "str|Entity",
        normal_direction_axis: "str|int|Axis" = "z",
    ):
        return self

    def remesh(self, strategy: "str", amount: "float"):
        return self

    def subdivide(self, amount: "float"):
        return self

    def decimate(self, amount: "float"):
        return self

    def create_from_file(self, file_path: "str", file_type: "str| None" = None):
        return self

    def export(self, file_path: "str", overwrite: "bool" = True, scale: "float" = 1.0):
        return self

    def scale_xyz(
        self,
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ):
        return self

    def scale_x(self, scale: "str|float|Dimension"):
        return self

    def scale_y(self, scale: "str|float|Dimension"):
        return self

    def scale_z(self, scale: "str|float|Dimension"):
        return self

    def scale_x_by_factor(self, scale_factor: "float"):
        return self

    def scale_y_by_factor(self, scale_factor: "float"):
        return self

    def scale_z_by_factor(self, scale_factor: "float"):
        return self

    def scale_keep_aspect_ratio(
        self, scale: "str|float|Dimension", axis: "str|int|Axis"
    ):
        return self

    def create_cube(
        self,
        width: "str|float|Dimension",
        length: "str|float|Dimension",
        height: "str|float|Dimension",
        keyword_arguments: "dict| None" = None,
    ):
        return self

    def create_cone(
        self,
        radius: "str|float|Dimension",
        height: "str|float|Dimension",
        draft_radius: "str|float|Dimension" = 0,
        keyword_arguments: "dict| None" = None,
    ):
        return self

    def create_cylinder(
        self,
        radius: "str|float|Dimension",
        height: "str|float|Dimension",
        keyword_arguments: "dict| None" = None,
    ):
        return self

    def create_torus(
        self,
        inner_radius: "str|float|Dimension",
        outer_radius: "str|float|Dimension",
        keyword_arguments: "dict| None" = None,
    ):
        return self

    def create_sphere(
        self, radius: "str|float|Dimension", keyword_arguments: "dict| None" = None
    ):
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
        return self

    def clone(self, new_name: "str", copy_landmarks: "bool" = True) -> "Part":
        raise NotImplementedError()

    def union(
        self,
        other: "str|Booleanable",
        delete_after_union: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        return self

    def subtract(
        self,
        other: "str|Booleanable",
        delete_after_subtract: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        return self

    def intersect(
        self,
        other: "str|Booleanable",
        delete_after_intersect: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        return self

    def hollow(
        self,
        thickness_x: "str|float|Dimension",
        thickness_y: "str|float|Dimension",
        thickness_z: "str|float|Dimension",
        start_axis: "str|int|Axis" = "z",
        flip_axis: "bool" = False,
    ):
        return self

    def thicken(self, radius: "str|float|Dimension"):
        return self

    def hole(
        self,
        hole_landmark: "str|Landmark",
        radius: "str|float|Dimension",
        depth: "str|float|Dimension",
        normal_axis: "str|int|Axis" = "z",
        flip_axis: "bool" = False,
        initial_rotation_x: "str|float|Angle" = 0.0,
        initial_rotation_y: "str|float|Angle" = 0.0,
        initial_rotation_z: "str|float|Angle" = 0.0,
        mirror_about_entity_or_landmark: "str|Entity| None" = None,
        mirror_axis: "str|int|Axis" = "x",
        mirror: "bool" = False,
        circular_pattern_instance_count: "int" = 1,
        circular_pattern_instance_separation: "str|float|Angle" = 0.0,
        circular_pattern_instance_axis: "str|int|Axis" = "z",
        circular_pattern_about_entity_or_landmark: "str|Entity| None" = None,
        linear_pattern_instance_count: "int" = 1,
        linear_pattern_instance_separation: "str|float|Dimension" = 0.0,
        linear_pattern_instance_axis: "str|int|Axis" = "x",
        linear_pattern2nd_instance_count: "int" = 1,
        linear_pattern2nd_instance_separation: "str|float|Dimension" = 0.0,
        linear_pattern2nd_instance_axis: "str|int|Axis" = "y",
    ):
        return self

    def twist(
        self,
        angle: "str|float|Angle",
        screw_pitch: "str|float|Dimension",
        iterations: "int" = 1,
        axis: "str|int|Axis" = "z",
    ):
        return self

    def set_material(self, material_name: "str|Material"):
        return self

    def is_colliding_with_part(self, other_part: "str|Part") -> bool:
        raise NotImplementedError()

    def fillet_all_edges(
        self, radius: "str|float|Dimension", use_width: "bool" = False
    ):
        return self

    def fillet_edges(
        self,
        radius: "str|float|Dimension",
        landmarks_near_edges: "list[str|Landmark]",
        use_width: "bool" = False,
    ):
        return self

    def fillet_faces(
        self,
        radius: "str|float|Dimension",
        landmarks_near_faces: "list[str|Landmark]",
        use_width: "bool" = False,
    ):
        return self

    def chamfer_all_edges(self, radius: "str|float|Dimension"):
        return self

    def chamfer_edges(
        self, radius: "str|float|Dimension", landmarks_near_edges: "list[str|Landmark]"
    ):
        return self

    def chamfer_faces(
        self, radius: "str|float|Dimension", landmarks_near_faces: "list[str|Landmark]"
    ):
        return self

    def select_vertex_near_landmark(self, landmark_name: "str|Landmark| None" = None):
        return self

    def select_edge_near_landmark(self, landmark_name: "str|Landmark| None" = None):
        return self

    def select_face_near_landmark(self, landmark_name: "str|Landmark| None" = None):
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
