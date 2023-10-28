# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod

from codetocad import Light


class LightTestInterface(metaclass=ABCMeta):
    @abstractmethod
    def test_set_color(self):
        instance = Light("name", "description", "native_instance")

        value = instance.set_color("r_value", "g_value", "b_value")

        assert value, "Modify method failed."

    @abstractmethod
    def test_create_sun(self):
        instance = Light("name", "description", "native_instance")

        value = instance.create_sun("energy_level")

        assert value.is_exists(), "Create method failed."

    @abstractmethod
    def test_create_spot(self):
        instance = Light("name", "description", "native_instance")

        value = instance.create_spot("energy_level")

        assert value.is_exists(), "Create method failed."

    @abstractmethod
    def test_create_point(self):
        instance = Light("name", "description", "native_instance")

        value = instance.create_point("energy_level")

        assert value.is_exists(), "Create method failed."

    @abstractmethod
    def test_create_area(self):
        instance = Light("name", "description", "native_instance")

        value = instance.create_area("energy_level")

        assert value.is_exists(), "Create method failed."
