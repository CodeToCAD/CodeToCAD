# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *

from typing import Self


from codetocad.providers import get_provider

from codetocad.interfaces.part_interface import PartInterface


from codetocad.interfaces.material_interface import MaterialInterface

from codetocad.interfaces.landmark_interface import LandmarkInterface


from codetocad.interfaces.booleanable_interface import BooleanableInterface


from codetocad.interfaces.entity_interface import EntityInterface


from codetocad.proxy.entity import Entity


class Part(PartInterface, Entity):
    """
    Capabilities related to creating and manipulating 3D shapes.

    NOTE: This is a proxy - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """

    # References OBJECT PROXYING (PYTHON RECIPE) https://code.activestate.com/recipes/496741-object-proxying/

    def __getattribute__(self, name):
        return getattr(object.__getattribute__(self, "__proxied"), name)

    def __delattr__(self, name):
        delattr(object.__getattribute__(self, "__proxied"), name)

    def __setattr__(self, name, value):
        setattr(object.__getattribute__(self, "__proxied"), name, value)

    def __nonzero__(self):
        return bool(object.__getattribute__(self, "__proxied"))

    def __str__(self):
        return str(object.__getattribute__(self, "__proxied"))

    def __repr__(self):
        return repr(object.__getattribute__(self, "__proxied"))

    __slots__ = [
        "__proxied",
    ]

    def __init__(
        self, name: "str", description: "str| None" = None, native_instance=None
    ):
        object.__setattr__(
            self,
            "__proxied",
            get_provider(PartInterface)(
                name, description, native_instance
            ),  # type: ignore
        )

    def create_cube(
        self,
        width: "str|float|Dimension",
        length: "str|float|Dimension",
        height: "str|float|Dimension",
        options: "PartOptions| None" = None,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").create_cube(
            width, length, height, options
        )

    def create_cone(
        self,
        radius: "str|float|Dimension",
        height: "str|float|Dimension",
        draft_radius: "str|float|Dimension" = 0,
        options: "PartOptions| None" = None,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").create_cone(
            radius, height, draft_radius, options
        )

    def create_cylinder(
        self,
        radius: "str|float|Dimension",
        height: "str|float|Dimension",
        options: "PartOptions| None" = None,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").create_cylinder(
            radius, height, options
        )

    def create_torus(
        self,
        inner_radius: "str|float|Dimension",
        outer_radius: "str|float|Dimension",
        options: "PartOptions| None" = None,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").create_torus(
            inner_radius, outer_radius, options
        )

    def create_sphere(
        self, radius: "str|float|Dimension", options: "PartOptions| None" = None
    ) -> Self:
        return object.__getattribute__(self, "__proxied").create_sphere(radius, options)

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
        options: "PartOptions| None" = None,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").create_gear(
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
            options,
        )

    def clone(self, new_name: "str", copy_landmarks: "bool" = True) -> "PartInterface":
        return object.__getattribute__(self, "__proxied").clone(
            new_name, copy_landmarks
        )

    def hollow(
        self,
        thickness_x: "str|float|Dimension",
        thickness_y: "str|float|Dimension",
        thickness_z: "str|float|Dimension",
        start_axis: "str|int|Axis" = "z",
        flip_axis: "bool" = False,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").hollow(
            thickness_x, thickness_y, thickness_z, start_axis, flip_axis
        )

    def thicken(self, radius: "str|float|Dimension") -> Self:
        return object.__getattribute__(self, "__proxied").thicken(radius)

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
    ) -> Self:
        return object.__getattribute__(self, "__proxied").hole(
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

    def twist(
        self,
        angle: "str|float|Angle",
        screw_pitch: "str|float|Dimension",
        iterations: "int" = 1,
        axis: "str|int|Axis" = "z",
    ) -> Self:
        return object.__getattribute__(self, "__proxied").twist(
            angle, screw_pitch, iterations, axis
        )

    def set_material(self, material_name: "str|MaterialInterface") -> Self:
        return object.__getattribute__(self, "__proxied").set_material(material_name)

    def is_colliding_with_part(self, other_part: "str|PartInterface") -> "bool":
        return object.__getattribute__(self, "__proxied").is_colliding_with_part(
            other_part
        )

    def fillet_all_edges(
        self, radius: "str|float|Dimension", use_width: "bool" = False
    ) -> Self:
        return object.__getattribute__(self, "__proxied").fillet_all_edges(
            radius, use_width
        )

    def fillet_edges(
        self,
        radius: "str|float|Dimension",
        landmarks_near_edges: "list[str|LandmarkInterface]",
        use_width: "bool" = False,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").fillet_edges(
            radius, landmarks_near_edges, use_width
        )

    def fillet_faces(
        self,
        radius: "str|float|Dimension",
        landmarks_near_faces: "list[str|LandmarkInterface]",
        use_width: "bool" = False,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").fillet_faces(
            radius, landmarks_near_faces, use_width
        )

    def chamfer_all_edges(self, radius: "str|float|Dimension") -> Self:
        return object.__getattribute__(self, "__proxied").chamfer_all_edges(radius)

    def chamfer_edges(
        self,
        radius: "str|float|Dimension",
        landmarks_near_edges: "list[str|LandmarkInterface]",
    ) -> Self:
        return object.__getattribute__(self, "__proxied").chamfer_edges(
            radius, landmarks_near_edges
        )

    def chamfer_faces(
        self,
        radius: "str|float|Dimension",
        landmarks_near_faces: "list[str|LandmarkInterface]",
    ) -> Self:
        return object.__getattribute__(self, "__proxied").chamfer_faces(
            radius, landmarks_near_faces
        )

    def select_vertex_near_landmark(
        self, landmark_name: "str|LandmarkInterface| None" = None
    ) -> Self:
        return object.__getattribute__(self, "__proxied").select_vertex_near_landmark(
            landmark_name
        )

    def select_edge_near_landmark(
        self, landmark_name: "str|LandmarkInterface| None" = None
    ) -> Self:
        return object.__getattribute__(self, "__proxied").select_edge_near_landmark(
            landmark_name
        )

    def select_face_near_landmark(
        self, landmark_name: "str|LandmarkInterface| None" = None
    ) -> Self:
        return object.__getattribute__(self, "__proxied").select_face_near_landmark(
            landmark_name
        )

    def mirror(
        self,
        mirror_across_entity: "str|EntityInterface",
        axis: "str|int|Axis",
        resulting_mirrored_entity_name: "str| None" = None,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").mirror(
            mirror_across_entity, axis, resulting_mirrored_entity_name
        )

    def linear_pattern(
        self,
        instance_count: "int",
        offset: "str|float|Dimension",
        direction_axis: "str|int|Axis" = "z",
    ) -> Self:
        return object.__getattribute__(self, "__proxied").linear_pattern(
            instance_count, offset, direction_axis
        )

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "str|float|Angle",
        center_entity_or_landmark: "str|EntityInterface",
        normal_direction_axis: "str|int|Axis" = "z",
    ) -> Self:
        return object.__getattribute__(self, "__proxied").circular_pattern(
            instance_count,
            separation_angle,
            center_entity_or_landmark,
            normal_direction_axis,
        )

    def remesh(self, strategy: "str", amount: "float") -> Self:
        return object.__getattribute__(self, "__proxied").remesh(strategy, amount)

    def subdivide(self, amount: "float") -> Self:
        return object.__getattribute__(self, "__proxied").subdivide(amount)

    def decimate(self, amount: "float") -> Self:
        return object.__getattribute__(self, "__proxied").decimate(amount)

    def create_from_file(self, file_path: "str", file_type: "str| None" = None) -> Self:
        return object.__getattribute__(self, "__proxied").create_from_file(
            file_path, file_type
        )

    def export(
        self, file_path: "str", overwrite: "bool" = True, scale: "float" = 1.0
    ) -> Self:
        return object.__getattribute__(self, "__proxied").export(
            file_path, overwrite, scale
        )

    def scale_xyz(
        self,
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ) -> Self:
        return object.__getattribute__(self, "__proxied").scale_xyz(x, y, z)

    def scale_x(self, scale: "str|float|Dimension") -> Self:
        return object.__getattribute__(self, "__proxied").scale_x(scale)

    def scale_y(self, scale: "str|float|Dimension") -> Self:
        return object.__getattribute__(self, "__proxied").scale_y(scale)

    def scale_z(self, scale: "str|float|Dimension") -> Self:
        return object.__getattribute__(self, "__proxied").scale_z(scale)

    def scale_x_by_factor(self, scale_factor: "float") -> Self:
        return object.__getattribute__(self, "__proxied").scale_x_by_factor(
            scale_factor
        )

    def scale_y_by_factor(self, scale_factor: "float") -> Self:
        return object.__getattribute__(self, "__proxied").scale_y_by_factor(
            scale_factor
        )

    def scale_z_by_factor(self, scale_factor: "float") -> Self:
        return object.__getattribute__(self, "__proxied").scale_z_by_factor(
            scale_factor
        )

    def scale_keep_aspect_ratio(
        self, scale: "str|float|Dimension", axis: "str|int|Axis"
    ) -> Self:
        return object.__getattribute__(self, "__proxied").scale_keep_aspect_ratio(
            scale, axis
        )

    def create_landmark(
        self,
        landmark_name: "str",
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ) -> "LandmarkInterface":
        return object.__getattribute__(self, "__proxied").create_landmark(
            landmark_name, x, y, z
        )

    def get_landmark(self, landmark_name: "str|PresetLandmark") -> "LandmarkInterface":
        return object.__getattribute__(self, "__proxied").get_landmark(landmark_name)

    def union(
        self,
        other: "str|BooleanableInterface",
        delete_after_union: "bool" = True,
        is_transfer_data: "bool" = False,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").union(
            other, delete_after_union, is_transfer_data
        )

    def subtract(
        self,
        other: "str|BooleanableInterface",
        delete_after_subtract: "bool" = True,
        is_transfer_data: "bool" = False,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").subtract(
            other, delete_after_subtract, is_transfer_data
        )

    def intersect(
        self,
        other: "str|BooleanableInterface",
        delete_after_intersect: "bool" = True,
        is_transfer_data: "bool" = False,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").intersect(
            other, delete_after_intersect, is_transfer_data
        )
