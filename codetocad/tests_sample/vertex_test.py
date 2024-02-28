# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from unittest import skip

from .test_helper import *
from codetocad.tests_interfaces import VertexTestInterface


from codetocad import Entity, Vertex


class VertexTest(TestProviderCase, VertexTestInterface):
    @skip("TODO")
    def test_get_control_points(self):
        instance = Vertex(
            name="String",
            location=Point.from_list_of_float_or_string([0, 0, 0]),
            description="String",
            native_instance=value,
            parent_entity=__import__("codetocad").Part("an entity"),
        )

        value = instance.get_control_points()

        assert value, "Get method failed."

    @skip("TODO")
    def test_project(self):
        instance = Vertex(
            name="String",
            location=Point.from_list_of_float_or_string([0, 0, 0]),
            description="String",
            native_instance=value,
            parent_entity=__import__("codetocad").Part("an entity"),
        )

        value = instance.project(
            project_from=__import__("codetocad").Sketch("a projected sketch")
        )

        assert value, "Get method failed."
