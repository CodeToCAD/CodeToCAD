# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from tests.test_providers import *

from codetocad.tests_interfaces.sketch_test_interface import SketchTestInterface


class SketchTest(TestProviderCase, SketchTestInterface):

    def test_get_wires(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.get_wires()

        assert value, "Get method failed."

    def test_clone(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.clone(new_name="String", copy_landmarks=True)

        assert value, "Get method failed."

    def test_create_text(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.create_text(
            text="String",
            font_size=1.0,
            bold=False,
            italic=False,
            underlined=False,
            character_spacing=1,
            word_spacing=1,
            line_spacing=1,
            font_file_path="String",
            center_at=["Point.from_list_of_float_or_string([0,0,0])"],
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
            options=SketchOptions(),
        )

        assert value.is_exists(), "Create method failed."

    def test_create_from_vertices(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.create_from_vertices(
            points=["Point.from_list_of_float_or_string([0,0,0])"],
            options=SketchOptions(),
        )

        assert value, "Get method failed."

    def test_create_point(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.create_point(
            point=Point.from_list_of_float_or_string([0, 0, 0]), options=SketchOptions()
        )

        assert value, "Get method failed."

    def test_create_line(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.create_line(
            length=Dimension(0, "mm"),
            angle=Angle(90),
            start_at="PresetLandmark.end",
            options=SketchOptions(),
        )

        assert value, "Get method failed."

    def test_create_line_to(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.create_line_to(
            to=["Point.from_list_of_float_or_string([0,0,0])"],
            start_at="PresetLandmark.end",
            options=SketchOptions(),
        )

        assert value, "Get method failed."

    def test_create_circle(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.create_circle(
            radius=Dimension(0, "mm"),
            center_at=["Point.from_list_of_float_or_string([0,0,0])"],
            options=SketchOptions(),
        )

        assert value, "Get method failed."

    def test_create_ellipse(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.create_ellipse(
            radius_minor=Dimension(0, "mm"),
            radius_major=Dimension(0, "mm"),
            center_at=["Point.from_list_of_float_or_string([0,0,0])"],
            options=SketchOptions(),
        )

        assert value, "Get method failed."

    def test_create_arc(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.create_arc(
            end_at=Point.from_list_of_float_or_string([0, 0, 0]),
            radius=Dimension(0, "mm"),
            start_at="PresetLandmark.end",
            flip=False,
            options=SketchOptions(),
        )

        assert value, "Get method failed."

    def test_create_rectangle(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.create_rectangle(
            length=Dimension(0, "mm"),
            width=Dimension(0, "mm"),
            center_at=["Point.from_list_of_float_or_string([0,0,0])"],
            options=SketchOptions(),
        )

        assert value, "Get method failed."

    def test_create_polygon(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.create_polygon(
            number_of_sides=0,
            length=Dimension(0, "mm"),
            width=Dimension(0, "mm"),
            center_at=["Point.from_list_of_float_or_string([0,0,0])"],
            options=SketchOptions(),
        )

        assert value, "Get method failed."

    def test_create_trapezoid(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.create_trapezoid(
            length_upper=Dimension(0, "mm"),
            length_lower=Dimension(0, "mm"),
            height=Dimension(0, "mm"),
            center_at=["Point.from_list_of_float_or_string([0,0,0])"],
            options=SketchOptions(),
        )

        assert value, "Get method failed."

    def test_create_spiral(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.create_spiral(
            number_of_turns=0,
            height=Dimension(0, "mm"),
            radius=Dimension(0, "mm"),
            is_clockwise=True,
            radius_end=Dimension(0, "mm"),
            center_at=["Point.from_list_of_float_or_string([0,0,0])"],
            options=SketchOptions(),
        )

        assert value, "Get method failed."

    def test_mirror(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.mirror(
            mirror_across_entity=__import__("codetocad").Part("an entity"),
            axis="x",
            resulting_mirrored_entity_name="String",
        )

        assert value.is_exists(), "Create method failed."

    def test_linear_pattern(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.linear_pattern(
            instance_count=0, offset=Dimension(0, "mm"), direction_axis="z"
        )

        assert value, "Modify method failed."

    def test_circular_pattern(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.circular_pattern(
            instance_count=0,
            separation_angle=Angle(90),
            center_entity_or_landmark=__import__("codetocad").Part("an entity"),
            normal_direction_axis="z",
        )

        assert value, "Modify method failed."

    def test_create_from_file(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.create_from_file(file_path="String", file_type="String")

        assert value.is_exists(), "Create method failed."

    def test_export(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.export(file_path="String", overwrite=True, scale=1.0)

    def test_scale_xyz(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.scale_xyz(
            x=Dimension(0, "mm"), y=Dimension(0, "mm"), z=Dimension(0, "mm")
        )

        assert value, "Modify method failed."

    def test_scale_x(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.scale_x(scale=Dimension(0, "mm"))

        assert value, "Modify method failed."

    def test_scale_y(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.scale_y(scale=Dimension(0, "mm"))

        assert value, "Modify method failed."

    def test_scale_z(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.scale_z(scale=Dimension(0, "mm"))

        assert value, "Modify method failed."

    def test_scale_x_by_factor(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.scale_x_by_factor(scale_factor=0.0)

        assert value, "Modify method failed."

    def test_scale_y_by_factor(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.scale_y_by_factor(scale_factor=0.0)

        assert value, "Modify method failed."

    def test_scale_z_by_factor(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.scale_z_by_factor(scale_factor=0.0)

        assert value, "Modify method failed."

    def test_scale_keep_aspect_ratio(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.scale_keep_aspect_ratio(scale=Dimension(0, "mm"), axis="x")

        assert value, "Modify method failed."

    def test_project(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.project(
            project_from=__import__("codetocad").Sketch("a projected sketch")
        )

        assert value, "Get method failed."

    def test_create_landmark(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.create_landmark(
            landmark_name="String",
            x=Dimension(0, "mm"),
            y=Dimension(0, "mm"),
            z=Dimension(0, "mm"),
        )

        assert value, "Get method failed."

    def test_get_landmark(self):

        instance = Sketch(
            name="String",
            description="String",
            native_instance="value",
            curve_type=CurveTypes.NURBS,
        )

        value = instance.get_landmark(landmark_name=PresetLandmark.leftTop)

        assert value, "Get method failed."
