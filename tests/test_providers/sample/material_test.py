# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from unittest import skip

from tests.test_providers.sample import *
from tests.test_providers import TestProviderCase

from codetocad.tests_interfaces import MaterialTestInterface


from codetocad import Material


class MaterialTest(TestProviderCase, MaterialTestInterface):
    @skip("TODO")
    def test_get_preset(self):
        instance = Material(name="String", description="String")

        value = instance.get_preset(material_name=PresetMaterial.red)

        assert value, "Get method failed."

    @skip("TODO")
    def test_set_color(self):
        instance = Material(name="String", description="String")

        value = instance.set_color(r_value=0, g_value=0, b_value=0, a_value=1.0)

        assert value, "Modify method failed."

    @skip("TODO")
    def test_set_reflectivity(self):
        instance = Material(name="String", description="String")

        value = instance.set_reflectivity(reflectivity=0.0)

        assert value, "Modify method failed."

    @skip("TODO")
    def test_set_roughness(self):
        instance = Material(name="String", description="String")

        value = instance.set_roughness(roughness=0.0)

        assert value, "Modify method failed."

    @skip("TODO")
    def test_set_image_texture(self):
        instance = Material(name="String", description="String")

        value = instance.set_image_texture(image_file_path="String")

        assert value, "Modify method failed."
