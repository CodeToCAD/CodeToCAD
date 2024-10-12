# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from tests.test_providers import *

from codetocad.tests_interfaces.part_test_interface import PartTestInterface


class PartTest(TestProviderCase, PartTestInterface):

    def test_create_cube(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.create_cube(
            width=Dimension(0, "mm"),
            length=Dimension(0, "mm"),
            height=Dimension(0, "mm"),
            options=PartOptions(),
        )

        assert value.is_exists(), "Create method failed."

    def test_create_cone(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.create_cone(
            radius=Dimension(0, "mm"),
            height=Dimension(0, "mm"),
            draft_radius=0,
            options=PartOptions(),
        )

        assert value.is_exists(), "Create method failed."

    def test_create_cylinder(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.create_cylinder(
            radius=Dimension(0, "mm"), height=Dimension(0, "mm"), options=PartOptions()
        )

        assert value.is_exists(), "Create method failed."

    def test_create_torus(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.create_torus(
            inner_radius=Dimension(0, "mm"),
            outer_radius=Dimension(0, "mm"),
            options=PartOptions(),
        )

        assert value.is_exists(), "Create method failed."

    def test_create_sphere(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.create_sphere(radius=Dimension(0, "mm"), options=PartOptions())

        assert value.is_exists(), "Create method failed."

    def test_create_gear(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.create_gear(
            outer_radius=Dimension(0, "mm"),
            addendum=Dimension(0, "mm"),
            inner_radius=Dimension(0, "mm"),
            dedendum=Dimension(0, "mm"),
            height=Dimension(0, "mm"),
            pressure_angle="20d",
            number_of_teeth=12,
            skew_angle=0,
            conical_angle=0,
            crown_angle=0,
            options=PartOptions(),
        )

        assert value.is_exists(), "Create method failed."

    def test_create_text(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.create_text(
            text="String",
            extrude_amount=Dimension(0, "mm"),
            font_size=1.0,
            bold=False,
            italic=False,
            underlined=False,
            character_spacing=1,
            word_spacing=1,
            line_spacing=1,
            font_file_path="String",
            profile_curve_name=Wire(
                "a wire",
                [
                    Edge(
                        v1=Vertex(
                            "a vertex", Point.from_list_of_float_or_string([0, 0, 0])
                        ),
                        v2=Vertex(
                            "a vertex", Point.from_list_of_float_or_string([0, 0, 0])
                        ),
                        name="an edge",
                    )
                ],
            ),
            options=PartOptions(),
        )

        assert value.is_exists(), "Create method failed."

    def test_clone(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.clone(new_name="String", copy_landmarks=True)

        assert value, "Get method failed."

    def test_hollow(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.hollow(
            thickness_x=Dimension(0, "mm"),
            thickness_y=Dimension(0, "mm"),
            thickness_z=Dimension(0, "mm"),
            start_axis="z",
            flip_axis=False,
        )

        assert value, "Modify method failed."

    def test_thicken(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.thicken(radius=Dimension(0, "mm"))

        assert value, "Modify method failed."

    def test_hole(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.hole(
            hole_landmark=Landmark("name", "parent"),
            radius=Dimension(0, "mm"),
            depth=Dimension(0, "mm"),
            normal_axis="z",
            flip_axis=False,
            initial_rotation_x=0.0,
            initial_rotation_y=0.0,
            initial_rotation_z=0.0,
            mirror_about_entity_or_landmark=__import__("codetocad").Part("an entity"),
            mirror_axis="x",
            mirror=False,
            circular_pattern_instance_count=1,
            circular_pattern_instance_separation=0.0,
            circular_pattern_instance_axis="z",
            circular_pattern_about_entity_or_landmark=__import__("codetocad").Part(
                "an entity"
            ),
            linear_pattern_instance_count=1,
            linear_pattern_instance_separation=0.0,
            linear_pattern_instance_axis="x",
            linear_pattern2nd_instance_count=1,
            linear_pattern2nd_instance_separation=0.0,
            linear_pattern2nd_instance_axis="y",
        )

        assert value, "Modify method failed."

    def test_twist(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.twist(
            angle=Angle(90), screw_pitch=Dimension(0, "mm"), iterations=1, axis="z"
        )

        assert value, "Modify method failed."

    def test_set_material(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.set_material(material_name=Material("mat"))

        assert value, "Modify method failed."

    def test_is_colliding_with_part(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.is_colliding_with_part(other_part=Part("a part"))

        assert value, "Get method failed."

    def test_fillet_all_edges(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.fillet_all_edges(radius=Dimension(0, "mm"), use_width=False)

        assert value, "Modify method failed."

    def test_fillet_edges(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.fillet_edges(
            radius=Dimension(0, "mm"),
            landmarks_near_edges=["Landmark('name', 'parent')"],
            use_width=False,
        )

        assert value, "Modify method failed."

    def test_fillet_faces(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.fillet_faces(
            radius=Dimension(0, "mm"),
            landmarks_near_faces=["Landmark('name', 'parent')"],
            use_width=False,
        )

        assert value, "Modify method failed."

    def test_chamfer_all_edges(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.chamfer_all_edges(radius=Dimension(0, "mm"))

        assert value, "Modify method failed."

    def test_chamfer_edges(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.chamfer_edges(
            radius=Dimension(0, "mm"),
            landmarks_near_edges=["Landmark('name', 'parent')"],
        )

        assert value, "Modify method failed."

    def test_chamfer_faces(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.chamfer_faces(
            radius=Dimension(0, "mm"),
            landmarks_near_faces=["Landmark('name', 'parent')"],
        )

        assert value, "Modify method failed."

    def test_select_vertex_near_landmark(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.select_vertex_near_landmark(
            landmark_name=Landmark("name", "parent")
        )

    def test_select_edge_near_landmark(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.select_edge_near_landmark(
            landmark_name=Landmark("name", "parent")
        )

    def test_select_face_near_landmark(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.select_face_near_landmark(
            landmark_name=Landmark("name", "parent")
        )

    def test_mirror(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.mirror(
            mirror_across_entity=__import__("codetocad").Part("an entity"),
            axis="x",
            resulting_mirrored_entity_name="String",
        )

        assert value.is_exists(), "Create method failed."

    def test_linear_pattern(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.linear_pattern(
            instance_count=0, offset=Dimension(0, "mm"), direction_axis="z"
        )

        assert value, "Modify method failed."

    def test_circular_pattern(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.circular_pattern(
            instance_count=0,
            separation_angle=Angle(90),
            center_entity_or_landmark=__import__("codetocad").Part("an entity"),
            normal_direction_axis="z",
        )

        assert value, "Modify method failed."

    def test_remesh(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.remesh(strategy="String", amount=0.0)

        assert value, "Modify method failed."

    def test_subdivide(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.subdivide(amount=0.0)

        assert value, "Modify method failed."

    def test_decimate(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.decimate(amount=0.0)

        assert value, "Modify method failed."

    def test_create_from_file(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.create_from_file(file_path="String", file_type="String")

        assert value.is_exists(), "Create method failed."

    def test_export(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.export(file_path="String", overwrite=True, scale=1.0)

    def test_scale_xyz(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.scale_xyz(
            x=Dimension(0, "mm"), y=Dimension(0, "mm"), z=Dimension(0, "mm")
        )

        assert value, "Modify method failed."

    def test_scale_x(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.scale_x(scale=Dimension(0, "mm"))

        assert value, "Modify method failed."

    def test_scale_y(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.scale_y(scale=Dimension(0, "mm"))

        assert value, "Modify method failed."

    def test_scale_z(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.scale_z(scale=Dimension(0, "mm"))

        assert value, "Modify method failed."

    def test_scale_x_by_factor(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.scale_x_by_factor(scale_factor=0.0)

        assert value, "Modify method failed."

    def test_scale_y_by_factor(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.scale_y_by_factor(scale_factor=0.0)

        assert value, "Modify method failed."

    def test_scale_z_by_factor(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.scale_z_by_factor(scale_factor=0.0)

        assert value, "Modify method failed."

    def test_scale_keep_aspect_ratio(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.scale_keep_aspect_ratio(scale=Dimension(0, "mm"), axis="x")

        assert value, "Modify method failed."

    def test_create_landmark(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.create_landmark(
            landmark_name="String",
            x=Dimension(0, "mm"),
            y=Dimension(0, "mm"),
            z=Dimension(0, "mm"),
        )

        assert value, "Get method failed."

    def test_get_landmark(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.get_landmark(landmark_name=PresetLandmark.leftTop)

        assert value, "Get method failed."

    def test_union(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.union(
            other=__import__("codetocad").Part("a booleanable part"),
            delete_after_union=True,
            is_transfer_data=False,
        )

        assert value, "Modify method failed."

    def test_subtract(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.subtract(
            other=__import__("codetocad").Part("a booleanable part"),
            delete_after_subtract=True,
            is_transfer_data=False,
        )

        assert value, "Modify method failed."

    def test_intersect(self):

        instance = Part(name="String", description="String", native_instance="value")

        value = instance.intersect(
            other=__import__("codetocad").Part("a booleanable part"),
            delete_after_intersect=True,
            is_transfer_data=False,
        )

        assert value, "Modify method failed."
