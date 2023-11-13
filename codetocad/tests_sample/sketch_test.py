# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from unittest import skip

from .test_helper import *
from codetocad.tests_interfaces import SketchTestInterface


class SketchTest(TestProviderCase, SketchTestInterface):
    @skip("TODO")
    def test_mirror(self):
        instance = Sketch()

        value = instance.mirror(
            "mirror_across_entity", "axis", "resulting_mirrored_entity_name"
        )

        assert value.is_exists(), "Create method failed."

    @skip("TODO")
    def test_linear_pattern(self):
        instance = Sketch()

        value = instance.linear_pattern("instance_count", "offset", "direction_axis")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_circular_pattern(self):
        instance = Sketch()

        value = instance.circular_pattern(
            "instance_count",
            "separation_angle",
            "center_entity_or_landmark",
            "normal_direction_axis",
        )

        assert value, "Modify method failed."

    @skip("TODO")
    def test_create_from_file(self):
        instance = Sketch()

        value = instance.create_from_file("file_path", "file_type")

        assert value.is_exists(), "Create method failed."

    @skip("TODO")
    def test_export(self):
        instance = Sketch()

        value = instance.export("file_path", "overwrite", "scale")

    @skip("TODO")
    def test_scale_xyz(self):
        instance = Sketch()

        value = instance.scale_xyz("x", "y", "z")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_scale_x(self):
        instance = Sketch()

        value = instance.scale_x("scale")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_scale_y(self):
        instance = Sketch()

        value = instance.scale_y("scale")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_scale_z(self):
        instance = Sketch()

        value = instance.scale_z("scale")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_scale_x_by_factor(self):
        instance = Sketch()

        value = instance.scale_x_by_factor("scale_factor")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_scale_y_by_factor(self):
        instance = Sketch()

        value = instance.scale_y_by_factor("scale_factor")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_scale_z_by_factor(self):
        instance = Sketch()

        value = instance.scale_z_by_factor("scale_factor")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_scale_keep_aspect_ratio(self):
        instance = Sketch()

        value = instance.scale_keep_aspect_ratio("scale", "axis")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_clone(self):
        instance = Sketch()

        value = instance.clone("new_name", "copy_landmarks")

        assert value, "Get method failed."

    @skip("TODO")
    def test_revolve(self):
        instance = Sketch()

        value = instance.revolve("angle", "about_entity_or_landmark", "axis")

        assert value, "Get method failed."

    @skip("TODO")
    def test_twist(self):
        instance = Sketch()

        value = instance.twist("angle", "screw_pitch", "interations", "axis")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_extrude(self):
        instance = Sketch()

        value = instance.extrude("length")

        assert value, "Get method failed."

    @skip("TODO")
    def test_sweep(self):
        instance = Sketch()

        value = instance.sweep("profile_name_or_instance", "fill_cap")

        assert value, "Get method failed."

    @skip("TODO")
    def test_offset(self):
        instance = Sketch()

        value = instance.offset("radius")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_profile(self):
        instance = Sketch()

        value = instance.profile("profile_curve_name")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_create_text(self):
        instance = Sketch()

        value = instance.create_text(
            "text",
            "font_size",
            "bold",
            "italic",
            "underlined",
            "character_spacing",
            "word_spacing",
            "line_spacing",
            "font_file_path",
        )

        assert value.is_exists(), "Create method failed."

    @skip("TODO")
    def test_create_from_vertices(self):
        instance = Sketch()

        value = instance.create_from_vertices("coordinates")

        assert value, "Get method failed."

    @skip("TODO")
    def test_create_point(self):
        instance = Sketch()

        value = instance.create_point("coordinate")

        assert value, "Get method failed."

    @skip("TODO")
    def test_create_line_between_points(self):
        instance = Sketch()

        value = instance.create_line_between_points("start_at", "end_at")

        assert value.is_exists(), "Create method failed."

    @skip("TODO")
    def test_create_circle(self):
        instance = Sketch()

        value = instance.create_circle("radius")

        assert value, "Get method failed."

    @skip("TODO")
    def test_create_ellipse(self):
        instance = Sketch()

        value = instance.create_ellipse("radius_minor", "radius_major")

        assert value, "Get method failed."

    @skip("TODO")
    def test_create_arc(self):
        instance = Sketch()

        value = instance.create_arc("start_at", "center_at", "end_at")

        assert value, "Get method failed."

    @skip("TODO")
    def test_create_rectangle(self):
        instance = Sketch()

        value = instance.create_rectangle("length", "width")

        assert value, "Get method failed."

    @skip("TODO")
    def test_create_polygon(self):
        instance = Sketch()

        value = instance.create_polygon("number_of_sides", "length", "width")

        assert value, "Get method failed."

    @skip("TODO")
    def test_create_trapezoid(self):
        instance = Sketch()

        value = instance.create_trapezoid("length_upper", "length_lower", "height")

        assert value, "Get method failed."

    @skip("TODO")
    def test_create_spiral(self):
        instance = Sketch()

        value = instance.create_spiral(
            "number_of_turns", "height", "radius", "is_clockwise", "radius_end"
        )

        assert value, "Get method failed."
