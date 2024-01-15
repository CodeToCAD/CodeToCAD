from .test_helper import *
from codetocad.tests_interfaces import WireTestInterface
from codetocad.enums.curve_types import CurveTypes


class WireTest(TestProviderCase, WireTestInterface):
    def test_mirror(self):
        ellipse_sketch = Sketch("ellipse", curve_type=CurveTypes.BEZIER)
        instance = ellipse_sketch.create_ellipse(0.5, 0.25)

        value = instance.mirror(
            mirror_across_entity="ellipse",
            axis="z",  # "resulting_mirrored_entity_name"
        )

        assert value.is_exists(), "Create method failed."

    def test_linear_pattern(self):
        ellipse_sketch = Sketch("ellipse", curve_type=CurveTypes.BEZIER)
        instance = ellipse_sketch.create_ellipse(0.5, 0.25)

        value = instance.linear_pattern(
            instance_count=2,
            offset=2,
        )  # "direction_axis")

        assert value, "Modify method failed."

    def test_circular_pattern(self):
        ellipse_sketch = Sketch("ellipse", curve_type=CurveTypes.BEZIER)
        instance = ellipse_sketch.create_ellipse(0.5, 0.25)

        value = instance.circular_pattern(
            instance_count=2,
            separation_angle=30,
            center_entity_or_landmark="circle",
            # "normal_direction_axis",
        )

        assert value, "Modify method failed."

    def test_project(self):
        ellipse_sketch = Sketch("ellipse", curve_type=CurveTypes.BEZIER)
        instance = ellipse_sketch.create_ellipse(0.5, 0.25)

        value = instance.project(project_onto="myProject")

        assert value, "Get method failed."

    def test_get_vertices(self):
        ellipse_sketch = Sketch("ellipse", curve_type=CurveTypes.BEZIER)
        instance = ellipse_sketch.create_ellipse(0.5, 0.25)

        value = instance.get_vertices()

        assert value, "Get method failed."

    def test_get_is_closed(self):
        ellipse_sketch = Sketch("ellipse", curve_type=CurveTypes.BEZIER)
        instance = ellipse_sketch.create_ellipse(0.5, 0.25)

        value = instance.get_is_closed()

        assert value, "Get method failed."

    def test_loft(self):
        ellipse_sketch = Sketch("ellipse", curve_type=CurveTypes.BEZIER)
        instance = ellipse_sketch.create_ellipse(0.5, 0.25)

        circle_sketch = Sketch("circle", curve_type=CurveTypes.BEZIER)
        instance = ellipse_sketch.create_circle(radius=0.5)

        value = instance.loft(other="circle", new_part_name="myLoft")

        assert value, "Get method failed."
