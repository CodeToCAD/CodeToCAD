# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from unittest import skip

from .test_helper import *
from codetocad.tests_interfaces import MaterialTestInterface


class MaterialTest(TestProviderCase, MaterialTestInterface):

    @skip("TODO")
    def test_assign_to_part(self):
        instance = Material("name", "description")

        value = instance.assign_to_part("part_name_or_instance")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_set_color(self):
        instance = Material("name", "description")

        value = instance.set_color("r_value", "g_value", "b_value", "a_value")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_set_reflectivity(self):
        instance = Material("name", "description")

        value = instance.set_reflectivity("reflectivity")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_set_roughness(self):
        instance = Material("name", "description")

        value = instance.set_roughness("roughness")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_set_image_texture(self):
        instance = Material("name", "description")

        value = instance.set_image_texture("image_file_path")

        assert value, "Modify method failed."
