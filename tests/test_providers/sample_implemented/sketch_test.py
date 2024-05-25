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

    def test_mirror(self):
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        value = instance.mirror(
            mirror_across_entity="mySketch",
            axis=1,
        )

        assert value.is_exists(), "Create method failed."

    def test_linear_pattern(self):
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        value = instance.linear_pattern(instance_count=2, offset=2)

        assert value, "Modify method failed."

    def test_circular_pattern(self):
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        value = instance.circular_pattern(
            instance_count=2,
            separation_angle=180,
            center_entity_or_landmark="mySketch",
            normal_direction_axis="z",
        )

        assert value, "Modify method failed."

    # @skip("TODO")
    def test_create_from_file(self):
        instance = Sketch("mySketch")

        value = instance.create_from_file(file_path="cube.png", file_type="png")

        assert value.is_exists(), "Create method failed."

    def test_export(self):
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        value = instance.export(file_path="my-sketch-exported.stl")

        assert value.is_exists(), "Create method failed."

    def test_scale_xyz(self):
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        value = instance.scale_xyz(x=0.5, y=0.5, z=0.5)

        assert value, "Modify method failed."

    def test_scale_x(self):
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        value = instance.scale_x(scale=0.5)

        assert value, "Modify method failed."

    def test_scale_y(self):
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        value = instance.scale_y(scale=0.5)

        assert value, "Modify method failed."

    def test_scale_z(self):
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        value = instance.scale_z(scale=0.5)

        assert value, "Modify method failed."

    def test_scale_x_by_factor(self):
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        value = instance.scale_x_by_factor(scale_factor=2)

        assert value, "Modify method failed."

    def test_scale_y_by_factor(self):
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        value = instance.scale_y_by_factor(scale_factor=2)

        assert value, "Modify method failed."

    def test_scale_z_by_factor(self):
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        value = instance.scale_z_by_factor(scale_factor=2)

        assert value, "Modify method failed."

    def test_scale_keep_aspect_ratio(self):
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        value = instance.scale_keep_aspect_ratio(scale=2, axis=1)

        assert value, "Modify method failed."

    def test_clone(self):  # None type object has no attribute name
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        value = instance.clone(new_name="myCloneSketch")

        assert value.is_exists(), "Get method failed."

    def test_create_text(self):
        instance = Sketch("mySketch")

        value = instance.create_text(
            text="sketch-text-test",
        )

        assert value.is_exists(), "Create method failed."

    def test_create_from_vertices(self):
        instance = Sketch("mySketch")

        instance.create_from_vertices(
            points=[(0, 2, 0), (2, 2, 0), (2, 0, 0), (0, 0, 0), (0, 2, 0)]
        )

        assert instance.is_exists(), "Create method failed."

    def test_create_point(self):
        instance = Sketch("mySketch")

        instance.create_point(point=(0, 0, 0))

        assert instance.is_exists(), "Create method failed."

    def test_create_line(self):
        instance = Sketch("mySketch")

        instance.create_line(end_at=(0, 5, 0), start_at=(5, 10, 0))

        assert instance.is_exists(), "Create method failed."

    def test_create_circle(self):
        instance = Sketch("myCircle")

        instance.create_circle(radius="5mm")

        assert instance.is_exists(), "Create method failed."

    def test_create_ellipse(self):
        instance = Sketch("Ellipse")

        instance.create_ellipse(radius_major=5, radius_minor=2)

        assert instance.is_exists(), "Create method failed."

    def test_create_arc(self):
        instance = Sketch("myArc")

        instance.create_arc(start_at=(0, 0, 0), end_at=(5, 0, 0), radius=2.5)

        assert instance.is_exists(), "Create method failed."

    def test_create_rectangle(self):
        instance = Sketch("myRectangle")

        instance.create_rectangle(length=5, width=10)

        assert instance.is_exists(), "Create method failed."

    # @skip("TODO")
    def test_create_polygon(self):
        instance = Sketch("mySketch")

        value = instance.create_polygon(number_of_sides=6, length=5, width=2)

        assert value.is_exists(), "Create method failed."

    # @skip("TODO")
    def test_create_trapezoid(self):
        instance = Sketch("mySketch")

        value = instance.create_trapezoid("length_upper", "length_lower", "height")

        assert value.is_exists(), "Create method failed."

    # @skip("TODO")
    def test_create_spiral(self):
        instance = Sketch("mySketch")

        value = instance.create_spiral(
            "number_of_turns", "height", "radius", "is_clockwise", "radius_end"
        )

        assert value.is_exists(), "Create method failed."
