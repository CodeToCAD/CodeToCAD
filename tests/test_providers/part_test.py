# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from unittest import skip

from .test_helper import *
from codetocad.tests_interfaces import PartTestInterface
import math


class PartTest(TestProviderCase, PartTestInterface):
    def test_mirror(self):
        instance = Part("myPart")

        instance.create_cylinder(
            radius=5,
            height=20,
        )

        value = instance.mirror(mirror_across_entity="myPart", axis="z")

        assert value.is_exists(), "Create method failed."

    def test_linear_pattern(self):
        instance = Part("myPart")

        instance.create_cylinder(
            radius=5,
            height=20,
        )

        value = instance.linear_pattern(
            instance_count=2,
            offset=2,
        )

        assert value, "Modify method failed."

    def test_circular_pattern(self):
        instance = Part("myPart")

        value = instance.create_cube(1, 1, 1)

        value = instance.circular_pattern(
            instance_count=2,
            separation_angle=math.pi,
            center_entity_or_landmark="myPart",
            # "normal_direction_axis",
        )

        assert value, "Modify method failed."

    @skip("TODO")
    def test_remesh(self):
        instance = Part()

        value = instance.remesh("strategy", "amount")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_subdivide(self):  # NotImplemented
        instance = Part("myCube")

        instance.create_cube(1, 1, 1)

        value = instance.subdivide(amount=10)

        assert value, "Modify method failed."

    @skip("TODO")
    def test_decimate(self):
        instance = Part()

        value = instance.decimate("amount")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_create_from_file(self):
        instance = Part()

        value = instance.create_from_file("file_path", "file_type")

        assert value.is_exists(), "Create method failed."

    def test_export(self):
        instance = Part("myPart")

        instance.create_cylinder(
            radius=5,
            height=20,
        )

        value = instance.export(
            file_path="part-export-test.stl",
        )

    def test_scale_xyz(self):
        instance = Part("myCube")

        instance.create_cube(1, 1, 1)

        value = instance.scale_xyz(x=1, y=0.5, z=2)

        assert value, "Modify method failed."

    def test_scale_x(self):
        instance = Part("myCube")

        instance.create_cube(1, 1, 1)

        value = instance.scale_x(scale=2)

        assert value, "Modify method failed."

    def test_scale_y(self):
        instance = Part("myCube")

        instance.create_cube(1, 1, 1)

        value = instance.scale_y(scale=0.5)

        assert value, "Modify method failed."

    def test_scale_z(self):
        instance = Part("myCube")

        instance.create_cube(1, 1, 1)

        value = instance.scale_z(scale=3)

        assert value, "Modify method failed."

    def test_scale_x_by_factor(self):
        instance = Part("myCube")

        instance.create_cube(1, 1, 1)

        value = instance.scale_x_by_factor(scale_factor=0.5)

        assert value, "Modify method failed."

    def test_scale_y_by_factor(self):
        instance = Part("myCube")

        instance.create_cube(1, 1, 1)

        value = instance.scale_y_by_factor(scale_factor=2.5)

        assert value, "Modify method failed."

    def test_scale_z_by_factor(self):
        instance = Part("myCube")

        instance.create_cube(1, 1, 1)

        value = instance.scale_z_by_factor(scale_factor=1.5)

        assert value, "Modify method failed."

    def test_scale_keep_aspect_ratio(self):
        instance = Part("myCube")

        instance.create_cube(1, 1, 1)

        value = instance.scale_keep_aspect_ratio(scale=2, axis="z")

        assert value, "Modify method failed."

    def test_create_cube(self):
        instance = Part("myCube")

        value = instance.create_cube(1, 1, 1)

        assert value.is_exists(), "Create method failed."

    def test_create_cone(self):
        instance = Part("myPart")

        value = instance.create_cone(
            radius=10,
            height=5,
            draft_radius=5,  # "keyword_arguments"
        )

        assert value.is_exists(), "Create method failed."

    def test_create_cylinder(self):
        instance = Part("myPart")

        value = instance.create_cylinder(
            radius=5,
            height=20,
        )

        assert value.is_exists(), "Create method failed."

    def test_create_torus(self):
        instance = Part("myPart")

        value = instance.create_torus(
            inner_radius=3,
            outer_radius=7,  # "keyword_arguments"
        )

        assert value.is_exists(), "Create method failed."

    def test_create_sphere(self):
        instance = Part("myPart")

        value = instance.create_sphere(
            radius=5,
        )  # "keyword_arguments")

        assert value.is_exists(), "Create method failed."

    def test_create_gear(self):
        instance = Part("myPart")

        value = instance.create_gear(
            outer_radius=50,
            addendum=5,
            inner_radius=35,
            dedendum=12,
            height=5,
            # "pressure_angle",
            # "number_of_teeth",
            # "skew_angle",
            # "conical_angle",
            # "crown_angle",
            # "keyword_arguments",
        )

        assert value.is_exists(), "Create method failed."

    def test_clone(self):
        instance = Part("myCube")

        instance.create_cube(1, 1, 1)

        value = instance.clone(
            "myCubeClone",
        )

        assert value, "Get method failed."

    def test_union(self):
        instance = Part("myCube")

        instance.create_cube(1, 1, 1)

        instance2 = Part("myCylinder")

        instance2.create_cylinder(radius=5, height=10)

        value = instance.union(
            with_part="myCylinder",  # "delete_after_union", "is_transfer_landmarks"
        )

        assert value, "Modify method failed."

    def test_subtract(self):
        instance = Part("myCube")

        instance.create_cube(1, 1, 1)

        instance2 = Part("myCylinder")

        instance2.create_cylinder(radius=5, height=10)

        value = instance.subtract(
            with_part="myCylinder",  # "delete_after_subtract", "is_transfer_landmarks"
        )

        assert value, "Modify method failed."

    def test_intersect(self):
        instance = Part("myCube")

        instance.create_cube(1, 1, 1)

        instance2 = Part("myCylinder")

        instance2.create_cylinder(radius=5, height=10)

        value = instance.intersect(
            with_part="myCylinder",  # "delete_after_intersect", "is_transfer_landmarks"
        )

        assert value, "Modify method failed."

    @skip("TODO")
    def test_hollow(self):  # Object myCube_f7272a513a does not exists
        instance = Part("myCube")

        instance.create_cube(1, 1, 1)

        value = instance.hollow(
            thickness_x=0.5,
            thickness_y=0.5,
            thickness_z=0.5,  # "start_axis", "flip_axis"
        )

        assert value, "Modify method failed."

    def test_thicken(self):
        instance = Part("myCylinder")

        instance.create_cylinder(radius=5, height=10)

        value = instance.thicken(radius=1)

        assert value, "Modify method failed."

    @skip("TODO")
    def test_hole(
        self,
    ):  # zero-size array to reduction operation minimum which has no identity
        instance = Part("myCylinder")

        instance.create_cylinder(radius=5, height=10)

        value = instance.hole(
            hole_landmark="myCube",
            radius=2,
            depth=3,
            # "normal_axis",
            # "flip_axis",
            # "initial_rotation_x",
            # "initial_rotation_y",
            # "initial_rotation_z",
            # "mirror_about_entity_or_landmark",
            # "mirror_axis",
            # "mirror",
            # "circular_pattern_instance_count",
            # "circular_pattern_instance_separation",
            # "circular_pattern_instance_axis",
            # "circular_pattern_about_entity_or_landmark",
            # "linear_pattern_instance_count",
            # "linear_pattern_instance_separation",
            # "linear_pattern_instance_axis",
            # "linear_pattern2nd_instance_count",
            # "linear_pattern2nd_instance_separation",
            # "linear_pattern2nd_instance_axis",
        )

        assert value, "Modify method failed."

    @skip("TODO")
    def test_twist(self):
        instance = Part("myScrew")

        value = instance.twist(
            angle=30,
            screw_pitch=5,
            iterations=10,
        )

        assert value, "Modify method failed."

    def test_set_material(self):
        instance = Part("myCylinder")

        instance.create_cylinder(radius=5, height=10)

        value = instance.set_material(material_name="test-material")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_is_colliding_with_part(self):
        instance = Part("myCube")

        instance.create_cube(1, 1, 1)

        instance2 = Part("myCylinder")

        instance2.create_cylinder(radius=5, height=10)

        value = instance.is_colliding_with_part(other_part="myCylinder")

        assert value, "Get method failed."

    def test_fillet_all_edges(self):
        instance = Part("myCube")

        instance.create_cube(5, 5, 5)

        value = instance.fillet_all_edges(
            radius=0.2,
        )  # "use_width")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_fillet_edges(self):
        instance = Part("myCube")

        instance.create_cube(1, 1, 1)

        instance.create_landmark(x=0.5, y=0.5, z=0.5, landmark_name="fillet-ref-lm")

        value = instance.fillet_edges(
            radius=0.1,
            landmarks_near_edges=["fillet-ref-lm"],
        )  # "use_width")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_fillet_faces(self):
        instance = Part()

        value = instance.fillet_faces("radius", "landmarks_near_faces", "use_width")

        assert value, "Modify method failed."

    def test_chamfer_all_edges(self):
        instance = Part("myCube")

        instance.create_cube(5, 5, 5)

        value = instance.chamfer_all_edges(radius=2)

        assert value, "Modify method failed."

    @skip("TODO")
    def test_chamfer_edges(self):
        instance = Part()

        value = instance.chamfer_edges("radius", "landmarks_near_edges")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_chamfer_faces(self):
        instance = Part()

        value = instance.chamfer_faces("radius", "landmarks_near_faces")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_select_vertex_near_landmark(self):
        instance = Part("myCube")

        instance.create_cube(5, 5, 5)

        value = instance.select_vertex_near_landmark("landmark_name")

    @skip("TODO")
    def test_select_edge_near_landmark(self):
        instance = Part()

        value = instance.select_edge_near_landmark("landmark_name")

    @skip("TODO")
    def test_select_face_near_landmark(self):
        instance = Part()

        value = instance.select_face_near_landmark("landmark_name")
