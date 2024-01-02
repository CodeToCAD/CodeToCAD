# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from unittest import skip

from .test_helper import *
from codetocad.tests_interfaces import MaterialTestInterface


class MaterialTest(TestProviderCase, MaterialTestInterface):
    
    def test_assign_to_part(self):
        instance = Material.get_sample_mat_instance()

        value = instance.assign_to_part(part_name_or_instance="myPart")

        assert value, "Modify method failed."

    
    def test_set_color(self):
        instance = Material.get_sample_mat_instance()

        value = instance.set_color(r_value=100, g_value=100, b_value=100, a_value=0.6)

        assert value, "Modify method failed."

    
    def test_set_reflectivity(self):
        instance = Material.get_sample_mat_instance()

        value = instance.set_reflectivity(reflectivity=2)

        assert value, "Modify method failed."

    
    def test_set_roughness(self):
        instance = Material.get_sample_mat_instance()

        value = instance.set_roughness(roughness=250)

        assert value, "Modify method failed."

    
    def test_set_image_texture(self):
        instance = Material.get_sample_mat_instance()

        value = instance.set_image_texture(image_file_path="test-material-texture.png")

        assert value, "Modify method failed."
