from tests.test_providers import *
from codetocad.tests_interfaces.part_test_interface import PartTestInterface
import math


class PartTest(TestProviderCase, PartTestInterface):
    def test_get_by_name(self):

        Part.create_cylinder(5, 1, name="testPart")

        value = Part.get_by_name(name="testPart")

        assert value, "Get method failed."

    def test_mirror(self):
        instance = Part("myPart")

        instance.create_cylinder(
            radius=5,
            height=20,
        )

        instance.translate_x(-1)

        mirror_entity = Sketch.create_point([0, 0, 0])

        value = instance.mirror(mirror_across_entity=mirror_entity, axis="z")

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

        mirror_entity = Sketch.create_point([0, 0, 0])

        value = instance.circular_pattern(
            instance_count=2,
            separation_angle=math.pi,
            center_entity_or_landmark=mirror_entity,
            # "normal_direction_axis",
        )

        assert value, "Modify method failed."

    def test_remesh(self):
        instance = Part("myPart")

        instance.create_cube(1, 1, 1)

        value = instance.remesh(strategy="smooth", amount=100)

        assert value, "Modify method failed."

    def test_subdivide(self):  # NotImplemented
        instance = Part.create_cube(1, 1, 1)

        value = instance.subdivide(amount=10)

        assert value, "Modify method failed."

    def test_decimate(self):
        instance = Part.create_cube(1, 1, 1)

        value = instance.decimate(amount=10)

        assert value, "Modify method failed."

    def test_create_from_file(self):
        instance = Part("myCube")

        value = instance.create_from_file(file_path="cube.png", file_type="png")

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
        instance = Part.create_cube(1, 1, 1)

        value = instance.scale_xyz(x=1, y=0.5, z=2)

        assert value, "Modify method failed."

    def test_scale_x(self):
        instance = Part.create_cube(1, 1, 1)

        value = instance.scale_x(scale=2)

        assert value, "Modify method failed."

    def test_scale_y(self):
        instance = Part.create_cube(1, 1, 1)

        value = instance.scale_y(scale=0.5)

        assert value, "Modify method failed."

    def test_scale_z(self):
        instance = Part.create_cube(1, 1, 1)

        value = instance.scale_z(scale=3)

        assert value, "Modify method failed."

    def test_scale_x_by_factor(self):
        instance = Part.create_cube(1, 1, 1)

        value = instance.scale_x_by_factor(scale_factor=0.5)

        assert value, "Modify method failed."

    def test_scale_y_by_factor(self):
        instance = Part.create_cube(1, 1, 1)

        value = instance.scale_y_by_factor(scale_factor=2.5)

        assert value, "Modify method failed."

    def test_scale_z_by_factor(self):
        instance = Part.create_cube(1, 1, 1)

        value = instance.scale_z_by_factor(scale_factor=1.5)

        assert value, "Modify method failed."

    def test_scale_keep_aspect_ratio(self):
        instance = Part.create_cube(1, 1, 1)

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

    def test_create_text(self):

        value = Part.create_text(text="My string", extrude_amount="10mm")

        assert value.is_exists(), "Create method failed."

    def test_clone(self):
        instance = Part.create_cube(1, 1, 1)

        value = instance.clone(
            "myCubeClone",
        )

        assert value, "Get method failed."

    def test_union(self):
        instance = Part.create_cube(1, 1, 1)

        instance2 = Part("myCylinder")

        instance2.create_cylinder(radius=5, height=10)

        value = instance.union(
            other=instance2,
        )

        assert value, "Modify method failed."

    def test_subtract(self):
        instance = Part.create_cube(1, 1, 1)

        instance2 = Part("myCylinder")

        instance2.create_cylinder(radius=5, height=10)

        value = instance.subtract(other=instance2)

        assert value, "Modify method failed."

    def test_intersect(self):
        instance = Part.create_cube(1, 1, 1)

        instance2 = Part("myCylinder")

        instance2.create_cylinder(radius=5, height=10)

        value = instance.intersect(other=instance2)

        assert value, "Modify method failed."

    def test_hollow(self):
        instance = Part.create_cube(1, 1, 1)

        value = instance.hollow(
            thickness_x=0.5,
            thickness_y=0.5,
            thickness_z=0.5,
        )

        assert value, "Modify method failed."

    def test_thicken(self):
        instance = Part("myCylinder")

        instance.create_cylinder(radius=5, height=10)

        value = instance.thicken(radius=1)

        assert value, "Modify method failed."

    def test_hole(self):
        instance = Part("holeTest")

        instance.create_cube(1, 1, 1)

        value = instance.hole(
            hole_landmark=instance.get_landmark("center"),
            radius=2,
            depth=3,
        )

        assert value, "Modify method failed."

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

        value = instance.set_material(PresetMaterial.blue.material)

        assert value, "Modify method failed."

    def test_is_colliding_with_part(self):
        instance = Part.create_cube(1, 1, 1)

        instance2 = Part("myCylinder")

        instance2.create_cylinder(radius=5, height=10)

        value = instance.is_colliding_with_part(other_part=instance2)

        assert value, "Get method failed."

    def test_fillet_all_edges(self):
        instance = Part.create_cube(5, 5, 5)

        value = instance.fillet_all_edges(
            radius=0.2,
        )  # "use_width")

        assert value, "Modify method failed."

    def test_fillet_edges(self):
        instance = Part.create_cube(1, 1, 1)

        instance.create_landmark(x=0.5, y=0.5, z=0.5, landmark_name="fillet-ref-lm")

        value = instance.fillet_edges(
            radius=0.1,
            landmarks_near_edges=["fillet-ref-lm"],
        )  # "use_width")

        assert value, "Modify method failed."

    def test_fillet_faces(self):
        instance = Part.create_cube(5, 5, 5)

        instance.create_landmark(x=2.5, y=2.5, z=2.5, landmark_name="fillet-ref-lm")

        value = instance.fillet_faces(
            radius=1,
            landmarks_near_faces=["fillet-ref-lm"],
        )

        assert value, "Modify method failed."

    def test_chamfer_all_edges(self):
        instance = Part.create_cube(5, 5, 5)

        value = instance.chamfer_all_edges(radius=2)

        assert value, "Modify method failed."

    def test_chamfer_edges(self):
        instance = Part.create_cube(5, 5, 5)

        instance.create_landmark(x=2.5, y=2.5, z=2.5, landmark_name="ref-lm")

        value = instance.chamfer_edges(radius=2, landmarks_near_edges=["ref-lm"])

        assert value, "Modify method failed."

    def test_chamfer_faces(self):
        instance = Part.create_cube(5, 5, 5)

        instance.create_landmark(x=2.5, y=2.5, z=2.5, landmark_name="ref-lm")

        value = instance.chamfer_faces(radius=2, landmarks_near_faces=["ref-lm"])

        assert value, "Modify method failed."

    def test_select_vertex_near_landmark(self):
        instance = Part.create_cube(5, 5, 5)

        landmark = instance.create_landmark(x=2.5, y=2.5, z=2.5, landmark_name="ref-lm")

        value = instance.select_vertex_near_landmark(landmark=landmark)

        assert value, "Modify method failed."

    def test_select_edge_near_landmark(self):
        instance = Part.create_cube(5, 5, 5)

        landmark = instance.create_landmark(x=2.5, y=2.5, z=2.5, landmark_name="ref-lm")

        value = instance.select_edge_near_landmark(landmark=landmark)

        assert value, "Modify method failed."

    def test_select_face_near_landmark(self):
        instance = Part.create_cube(5, 5, 5)

        landmark = instance.create_landmark(x=2.5, y=2.5, z=2.5, landmark_name="ref-lm")

        value = instance.select_face_near_landmark(landmark=landmark)

        assert value, "Modify method failed."
