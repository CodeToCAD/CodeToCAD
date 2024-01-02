# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from unittest import skip

from .test_helper import *
from codetocad.tests_interfaces import VertexTestInterface


class VertexTest(TestProviderCase, VertexTestInterface):
    
    def test_project(self):
        instance = Vertex(location=(0, 0), name="myVertex")

        value = instance.project(project_onto="myProject")

        assert value, "Get method failed."

    
    def test_get_control_points(self):
        instance = Vertex(location=(0, 0), name="myVertex")

        value = instance.get_control_points(parameter="")

        assert value, "Get method failed."
