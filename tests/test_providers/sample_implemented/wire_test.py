import math
from tests.test_providers import *
from codetocad.tests_interfaces.wire_test_interface import WireTestInterface
from codetocad.enums.curve_types import CurveTypes


class WireTest(TestProviderCase, WireTestInterface):
    def test_mirror(self):
        ellipse_sketch = Sketch("ellipse", curve_type=CurveTypes.BEZIER)
        instance = ellipse_sketch.create_ellipse(0.5, 0.25)

        value = instance.mirror(
            mirror_across_entity=ellipse_sketch,
            axis="z",  # "separate_resulting_entity"
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
            center_entity_or_landmark=ellipse_sketch,
            # "normal_direction_axis",
        )

        assert value, "Modify method failed."

    def test_project(self):
        ellipse_sketch = Sketch("ellipse", curve_type=CurveTypes.BEZIER)
        instance = ellipse_sketch.create_ellipse(0.5, 0.25)

        projected_sketch = Sketch("projected_sketch", curve_type=CurveTypes.BEZIER)
        value = projected_sketch.project(project_from=ellipse_sketch)

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

        value = instance.loft(other="circle", new_name="myLoft")

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
        instance = instance.create_line_to(start_at=(0, 0), to=(10, 10))
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
            profile="mySketch",
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

        value = instance.create_circle(2).profile(profile_curve="Curve")

        assert value, "Modify method failed."

    def test_create_from_vertices(self):

        instance = Wire(
            name="String",
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
        )

        value = instance.create_from_vertices(
            points=["Point.from_list_of_float_or_string([0,0,0])"]
        )

        assert value, "Modify method failed."

    def test_create_point(self):

        instance = Wire(
            name="String",
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
        )

        value = instance.create_point(
            point=Point.from_list_of_float_or_string([0, 0, 0])
        )

        assert value, "Modify method failed."

    def test_create_line(self):

        instance = Wire(
            name="String",
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
        )

        value = instance.create_line(
            length=Dimension(0, "mm"), angle=Angle(90), start_at="PresetLandmark.end"
        )

        assert value, "Modify method failed."

    def test_create_line_to(self):

        instance = Wire(
            name="String",
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
        )

        value = instance.create_line_to(
            to=["Point.from_list_of_float_or_string([0,0,0])"],
            start_at="PresetLandmark.end",
        )

        assert value, "Modify method failed."

    def test_create_arc(self):

        instance = Wire(
            name="String",
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
        )

        value = instance.create_arc(
            end_at=Point.from_list_of_float_or_string([0, 0, 0]),
            radius=Dimension(0, "mm"),
            start_at="PresetLandmark.end",
            flip=False,
        )

        assert value, "Modify method failed."

    def test_get_parent(self):

        instance = Wire(
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
            name="String",
            description="String",
            native_instance="value",
        )

        value = instance.get_parent()

        assert value, "Get method failed."
