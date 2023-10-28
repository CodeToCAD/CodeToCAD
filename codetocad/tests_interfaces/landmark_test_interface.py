# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod

from codetocad import Landmark


class LandmarkTestInterface(metaclass=ABCMeta):
    @abstractmethod
    def test_get_landmark_entity_name(self):
        instance = Landmark("name", "parent_entity", "description", "native_instance")

        value = instance.get_landmark_entity_name("")

        assert value, "Get method failed."

    @abstractmethod
    def test_get_parent_entity(self):
        instance = Landmark("name", "parent_entity", "description", "native_instance")

        value = instance.get_parent_entity("")

        assert value, "Get method failed."
