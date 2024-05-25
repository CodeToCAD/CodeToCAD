from tests.test_providers import *
from codetocad.tests_interfaces.vertex_test_interface import VertexTestInterface


class VertexTest(TestProviderCase, VertexTestInterface):
    def test_project(self):
        instance = Vertex(location=(0, 0, 0), name="myVertex")

        value = instance.project(project_from="myProject")

        assert value, "Get method failed."

    def test_get_control_points(self):
        instance = Vertex(location=(0, 0, 0), name="myVertex")

        value = instance.get_control_points()

        assert value, "Get method failed."

    def test_set_control_points(self):

        instance = Vertex(location=(0, 0, 0), name="myVertex")

        value = instance.set_control_points(
            points=[Point.from_list_of_float_or_string([0, 0, 0])]
        )

        assert value, "Modify method failed."
