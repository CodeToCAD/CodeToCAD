import math
from codetocad.interfaces.sketch_interface import SketchInterface
from tests.test_providers import *
from codetocad.tests_interfaces.wire_test_interface import WireTestInterface
from codetocad.enums.curve_types import CurveTypes


class WireTest(TestProviderCase, WireTestInterface):
    def test_mirror(self):
        instance = Sketch.create_ellipse(0.5, 0.25).get_wires()[0]

        value = instance.mirror(
            mirror_across_entity=instance.get_parent(),
            axis="z",
        )

        assert value.is_exists(), "Create method failed."

    def test_linear_pattern(self):
        instance = Sketch.create_ellipse(0.5, 0.25).get_wires()[0]

        value = instance.linear_pattern(
            instance_count=2,
            offset=2,
        )

        assert value, "Modify method failed."

    def test_circular_pattern(self):
        instance = Sketch.create_ellipse(0.5, 0.25).get_wires()[0]

        value = instance.circular_pattern(
            instance_count=2,
            separation_angle=30,
            center_entity_or_landmark=instance.get_parent(),
            # "normal_direction_axis",
        )

        assert value, "Modify method failed."

    def test_project(self):
        ellipse_sketch = Sketch.create_ellipse(0.5, 0.25).get_wires()[0]

        value = Sketch.create_point([0, 0, 0]).project(project_from=ellipse_sketch)

        assert value, "Get method failed."

    def test_get_normal(self):
        instance = Sketch.create_ellipse(0.5, 0.25).get_wires()[0]

        value = instance.get_vertices()

        assert value, "Create method failed."

        value = instance.get_normal(False)

        assert value, "Get method failed."

    def test_get_edges(self):
        instance = Sketch.create_ellipse(0.5, 0.25).get_wires()[0]

        value = instance.get_edges()

        assert value, "Get method failed."

    def test_get_vertices(self):
        instance = Sketch.create_ellipse(0.5, 0.25).get_wires()[0]

        value = instance.get_vertices()

        assert value, "Get method failed."

    def test_get_is_closed(self):
        instance = Sketch.create_ellipse(0.5, 0.25).get_wires()[0]

        value = instance.get_is_closed()

        assert value, "Get method failed."

    def test_loft(self):
        ellipse = Sketch.create_ellipse(0.5, 0.25).get_wires()[0]

        circle = Sketch.create_circle(radius=0.5).get_wires()[0]

        value = ellipse.loft(other=circle, new_name="myLoft")

        assert value, "Get method failed."

    def test_revolve(self):
        instance = Sketch.create_rectangle(length=5, width=5).get_wires()[0]

        value = instance.revolve(
            angle=math.pi,
            about_entity_or_landmark=Sketch.create_point([0, 0, 0]).translate_x(5),
            axis="x",
        )

        assert value, "Get method failed."

    def test_twist(self):
        instance = Sketch.create_line_to(start_at=(0, 0), to=(10, 10)).get_wires()[0]
        value = instance.twist(
            angle=30,
            screw_pitch=5,
            iterations=10,
        )

        assert value, "Modify method failed."

    def test_extrude(self):
        instance = Sketch.create_rectangle(length=5, width=5).get_wires()[0]

        value = instance.extrude(length=5)

        assert value, "Get method failed."

    def test_sweep(self):
        line = Sketch.create_line_to(start_at=(0, 0), to=(10, 10)).get_wires()[0]

        instance = Sketch.create_rectangle(length=5, width=5).get_wires()[0]

        value = instance.sweep(
            profile=line,
        )

        assert value, "Get method failed."

    def test_offset(
        self,
    ):
        instance = Sketch.create_circle(radius=5).get_wires()[0]

        value = instance.offset(radius=2)

        assert value, "Modify method failed."

    def test_profile(self):

        value = Sketch.create_circle(2).get_wires()[0].profile(profile_curve="Curve")

        assert value, "Modify method failed."

    def test_create_from_vertices(self):

        instance = Sketch.create_point([0, 0, 0]).get_wires()[0]

        value = instance.create_from_vertices(
            points=["Point.from_list_of_float_or_string([0,0,0])"]
        )

        assert value, "Modify method failed."

    def test_create_point(self):

        instance = Sketch.create_point([0, 0, 0]).get_wires()[0]

        value = instance.create_point(
            point=Point.from_list_of_float_or_string([0, 0, 0])
        )

        assert value, "Modify method failed."

    def test_create_line(self):

        instance = Sketch.create_point([0, 0, 0]).get_wires()[0]

        value = instance.create_line(
            length=Dimension(0, "mm"), angle=Angle(90), start_at="PresetLandmark.end"
        )

        assert value, "Modify method failed."

    def test_create_line_to(self):

        instance = Sketch.create_point([0, 0, 0]).get_wires()[0]

        value = instance.create_line_to(
            to=["Point.from_list_of_float_or_string([0,0,0])"],
            start_at="PresetLandmark.end",
        )

        assert value, "Modify method failed."

    def test_create_arc(self):

        instance = Sketch.create_point([0, 0, 0]).get_wires()[0]

        value = instance.create_arc(
            end_at=Point.from_list_of_float_or_string([0, 0, 0]),
            radius=Dimension(0, "mm"),
            start_at="PresetLandmark.end",
            flip=False,
        )

        assert value, "Modify method failed."

    def test_get_parent(self):

        instance = Sketch.create_point([0, 0, 0]).get_wires()[0]

        value = instance.get_parent()

        assert value, "Get method failed."
