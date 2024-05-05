import math
from tests.test_providers import *
from codetocad.tests_interfaces.wire_test_interface import WireTestInterface
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

        value = instance.project(project_from="myProject")

        assert value, "Get method failed."

    def test_get_normal(self):
        ellipse_sketch = Sketch("ellipse", curve_type=CurveTypes.BEZIER)
        instance = ellipse_sketch.create_ellipse(0.5, 0.25)

        value = instance.get_vertices()

        assert value, "Create method failed."

        value = instance.get_normal(False)

        assert value, "Get method failed."

    def test_get_edges(self):

        instance = Wire(
            name="myWire",
            edges=[
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
            description="String",
            native_instance="value",
            parent_entity=__import__("codetocad").Part("an entity"),
        )

        value = instance.get_edges()

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

    def test_revolve(self):  # meshes error
        instance = Sketch("mySketch")

        instance = instance.create_rectangle(length=5, width=5)

        value = instance.revolve(
            angle=math.pi, about_entity_or_landmark="mySketch", axis=2
        )

        assert value, "Get method failed."

    def test_twist(self):  # not know implement
        instance = Sketch("mySketch")
        instance = instance.create_line(start_at=(0, 0), end_at=(10, 10))
        value = instance.twist(
            angle=30,
            screw_pitch=5,
            iterations=10,
        )

        assert value, "Modify method failed."

    # @skip("TODO")
    def test_extrude(self):  # meshes error
        instance = Sketch("mySketch")

        instance = instance.create_rectangle(length=5, width=5)

        value = instance.extrude(length=5)

        assert value, "Get method failed."

    def test_sweep(self):  # Meshes error
        instance = Sketch("mySketch")

        instance = instance.create_rectangle(length=5, width=5)

        value = instance.sweep(
            profile_name_or_instance="mySketch",
        )

        assert value, "Get method failed."

    def test_offset(
        self,
    ):
        instance = Sketch("mySketch")

        instance = instance.create_circle(radius=5)

        value = instance.offset(radius=2)

        assert value, "Modify method failed."

    def test_profile(self):
        instance = Sketch("mySketch")

        value = instance.create_circle(2).profile(profile_curve_name="Curve")

        assert value, "Modify method failed."
