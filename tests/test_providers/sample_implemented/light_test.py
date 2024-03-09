from tests.test_providers import *
from codetocad.tests_interfaces.light_test_interface import LightTestInterface


class LightTest(TestProviderCase, LightTestInterface):
    def test_set_color(self):
        instance = Light("myLight")

        value = instance.set_color(r_value=120, g_value=60, b_value=45)

        assert value, "Modify method failed."

    def test_create_sun(self):
        instance = Light("myLight")

        value = instance.create_sun(energy_level=5.5)

        assert value.is_exists(), "Create method failed."

    def test_create_spot(self):
        instance = Light("myLight")

        value = instance.create_spot(energy_level=2.1)

        assert value.is_exists(), "Create method failed."

    def test_create_point(self):
        instance = Light("myLight")

        value = instance.create_point(energy_level=2.5)

        assert value.is_exists(), "Create method failed."

    def test_create_area(self):
        instance = Light("myLight")

        value = instance.create_area(energy_level=5.5)

        assert value.is_exists(), "Create method failed."
