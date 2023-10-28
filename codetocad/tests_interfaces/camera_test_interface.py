# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod

from codetocad import Camera


class CameraTestInterface(metaclass=ABCMeta):
    @abstractmethod
    def test_create_perspective(self):
        instance = Camera("name", "description", "native_instance")

        value = instance.create_perspective("")

        assert value.is_exists(), "Create method failed."

    @abstractmethod
    def test_create_orthogonal(self):
        instance = Camera("name", "description", "native_instance")

        value = instance.create_orthogonal("")

        assert value.is_exists(), "Create method failed."

    @abstractmethod
    def test_set_focal_length(self):
        instance = Camera("name", "description", "native_instance")

        value = instance.set_focal_length("length")

        assert value, "Modify method failed."
