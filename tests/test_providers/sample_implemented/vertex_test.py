from tests.test_providers import *
from codetocad.tests_interfaces.vertex_test_interface import VertexTestInterface


class VertexTest(TestProviderCase, VertexTestInterface):

    def test_project(self):
        instance = Sketch.create_point([0, 0, 0]).get_wires()[0].get_vertices()[0]

        value = instance.project(project_from="myProject")  # TODO: Fix this

        assert value, "Get method failed."

    def test_get_control_points(self):
        instance = Sketch.create_point([0, 0, 0]).get_wires()[0].get_vertices()[0]
        value = instance.get_control_points()

        assert value, "Get method failed."

    def test_set_control_points(self):

        instance = Sketch.create_point([0, 0, 0]).get_wires()[0].get_vertices()[0]

        value = instance.set_control_points(
            points=[Point.from_list_of_float_or_string([0, 0, 0])]
        )

        assert value, "Modify method failed."

    def test_get_location(self):

        instance = Sketch.create_point([0, 0, 0]).get_wires()[0].get_vertices()[0]

        value = instance.get_location()

        assert value, "Get method failed."
