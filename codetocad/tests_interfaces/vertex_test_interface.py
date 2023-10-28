# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod

from codetocad import Vertex


class VertexTestInterface(metaclass=ABCMeta):
    @abstractmethod
    def test_get_control_points(self):
        instance = Vertex(
            "location", "parent_sketch", "name", "description", "native_instance"
        )

        value = instance.get_control_points("parameter")

        assert value, "Get method failed."
