from .test_helper import *
from codetocad.tests_interfaces import VertexTestInterface


class VertexTest(TestProviderCase, VertexTestInterface):
    def test_project(self):
        instance = Vertex(location=(0, 0), name="myVertex")

        value = instance.project(project_from="myProject")

        assert value, "Get method failed."

    def test_get_control_points(self):
        instance = Vertex(location=(0, 0), name="myVertex")

        value = instance.get_control_points()

        assert value, "Get method failed."
