from tests.test_providers import *
from codetocad.enums.preset_material import PresetMaterial
from codetocad.tests_interfaces.material_test_interface import MaterialTestInterface


class MaterialTest(TestProviderCase, MaterialTestInterface):
    def test_get_preset(self):
        instance = Material("myMaterial")

        value = instance.get_preset(PresetMaterial.blue)

        assert value, "Get method failed."

    def test_set_color(self):
        instance = Material("myMaterial")

        value = instance.set_color(r_value=100, g_value=100, b_value=100, a_value=0.6)

        assert value, "Modify method failed."

    def test_set_reflectivity(self):
        instance = Material("myMaterial")

        value = instance.set_reflectivity(reflectivity=2)

        assert value, "Modify method failed."

    def test_set_roughness(self):
        instance = Material("myMaterial")

        value = instance.set_roughness(roughness=250)

        assert value, "Modify method failed."

    def test_set_image_texture(self):
        instance = Material("myMaterial")

        value = instance.set_image_texture(image_file_path="test-material-texture.png")

        assert value, "Modify method failed."
