from tests.test_providers import *
from codetocad.tests_interfaces.edge_test_interface import EdgeTestInterface


class EdgeTest(TestProviderCase, EdgeTestInterface):

    def test_mirror(self):
        edge = (
            Sketch.create_line_to(to=(0, 5, 0), start_at=(5, 10, 0))
            .get_wires()[0]
            .get_edges()[0]
        )

        value = edge.mirror(
            mirror_across_entity="mySketch",
            axis=1,
        )

        assert value.is_exists(), "Create method failed."

    def test_linear_pattern(self):
        edge = (
            Sketch.create_line_to(to=(0, 5, 0), start_at=(5, 10, 0))
            .get_wires()[0]
            .get_edges()[0]
        )

        value = edge.linear_pattern(
            instance_count=2,
            offset=50,
        )

        assert value, "Modify method failed."

    def test_circular_pattern(self):
        edge = (
            Sketch.create_line_to(to=(0, 5, 0), start_at=(5, 10, 0))
            .get_wires()[0]
            .get_edges()[0]
        )

        value = edge.circular_pattern(
            instance_count=4,
            separation_angle=90,
            center_entity_or_landmark=Sketch.create_point([0, 0, 0]).translate_x(2),
            # "normal_direction_axis",
        )

        assert value, "Modify method failed."

    def test_remesh(self):
        edge = (
            Sketch.create_line_to(to=(0, 5, 0), start_at=(5, 10, 0))
            .get_wires()[0]
            .get_edges()[0]
        )

        value = edge.remesh(strategy="smooth", amount=100)

        assert value, "Modify method failed."

    def test_subdivide(self):
        edge = (
            Sketch.create_line_to(to=(0, 5, 0), start_at=(5, 10, 0))
            .get_wires()[0]
            .get_edges()[0]
        )

        value = edge.subdivide(amount=10)

        assert value, "Modify method failed."

    def test_decimate(self):
        edge = (
            Sketch.create_line_to(to=(0, 5, 0), start_at=(5, 10, 0))
            .get_wires()[0]
            .get_edges()[0]
        )

        value = edge.decimate(amount=0.5)

        assert value, "Modify method failed."

    def test_project(self):
        edge = (
            Sketch.create_line_to(to=(0, 5, 0), start_at=(5, 10, 0))
            .get_wires()[0]
            .get_edges()[0]
        )

        value = edge.project(project_from="test-project")

        assert value, "Get method failed."

    def test_offset(self):
        edge = (
            Sketch.create_line_to(to=(0, 5, 0), start_at=(5, 10, 0))
            .get_wires()[0]
            .get_edges()[0]
        )

        value = edge.offset(distance=10)

        assert value, "Get method failed."

    def test_fillet(self):
        edge = (
            Sketch.create_line_to(to=(0, 5, 0), start_at=(5, 10, 0))
            .get_wires()[0]
            .get_edges()[0]
        )

        edge2 = (
            Sketch.create_line_to(to=(0, 5, 0), start_at=(5, 10, 0))
            .get_wires()[0]
            .get_edges()[0]
        )

        value = edge.fillet(other_edge=edge2, amount=2)

        assert value, "Modify method failed."

    def test_set_is_construction(self):
        edge = (
            Sketch.create_line_to(to=(0, 5, 0), start_at=(5, 10, 0))
            .get_wires()[0]
            .get_edges()[0]
        )

        value = edge.set_is_construction(is_construction=False)

        assert value, "Modify method failed."

    def test_get_is_construction(self):
        edge = (
            Sketch.create_line_to(to=(0, 5, 0), start_at=(5, 10, 0))
            .get_wires()[0]
            .get_edges()[0]
        )

        value = edge.get_is_construction()

        assert value, "Get method failed."

    def test_get_vertices(self):

        edge = (
            Sketch.create_line_to(to=(0, 5, 0), start_at=(5, 10, 0))
            .get_wires()[0]
            .get_edges()[0]
        )

        value = edge.get_vertices()

        assert value, "Get method failed."
