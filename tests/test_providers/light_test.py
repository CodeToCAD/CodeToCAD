# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from unittest import skip

from .test_helper import *
from codetocad.tests_interfaces import LightTestInterface


class LightTest(TestProviderCase, LightTestInterface):
    def test_set_color(self):
        instance = Light.get_sample_light()

        value = instance.set_color(r_value=120, g_value=60, b_value=45)

        assert value, "Modify method failed."

    def test_create_sun(self):
        instance = Light.get_sample_light()

        value = instance.create_sun(energy_level=5.5)

        assert value.is_exists(), "Create method failed."

    def test_create_spot(self):
        instance = Light.get_sample_light()

        value = instance.create_spot(energy_level=2.1)

        assert value.is_exists(), "Create method failed."

    def test_create_point(self):
        instance = Light.get_sample_light()

        value = instance.create_point(energy_level=2.5)

        assert value.is_exists(), "Create method failed."

    def test_create_area(self):
        instance = Light.get_sample_light()

        value = instance.create_area(energy_level=5.5)

        assert value.is_exists(), "Create method failed."
