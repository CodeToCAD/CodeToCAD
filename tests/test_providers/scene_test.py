# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from unittest import skip

from .test_helper import *
from codetocad.tests_interfaces import SceneTestInterface


class SceneTest(TestProviderCase, SceneTestInterface):
    def test_create(self):
        instance = Scene.get_sample_scene()

        value = instance.create()

        assert value.is_exists(), "Create method failed."

    def test_delete(self):
        instance = Scene.get_sample_scene()

        value = instance.delete()

    def test_get_selected_entity(self):
        instance = Scene.get_sample_scene()

        value = instance.get_selected_entity()

        assert value, "Get method failed."

    def test_export(self):
        instance = Scene.get_sample_scene()

        value = instance.export(
            file_path="scene-export.png",
            entities=[Entity("myEntity")],
        )

    def test_set_default_unit(self):
        instance = Scene.get_sample_scene()

        value = instance.set_default_unit(unit="mm")

        assert value, "Modify method failed."

    def test_create_group(self):
        instance = Scene.get_sample_scene()

        value = instance.create_group(name="test-scene-group")

        assert value.is_exists(), "Create method failed."

    def test_delete_group(self):
        instance = Scene.get_sample_scene()

        value = instance.delete_group(name="test-scene-group", remove_children=True)

    def test_remove_from_group(self):
        instance = Scene.get_sample_scene()

        value = instance.remove_from_group(
            entity_name="myEntity", group_name="test-scene-group"
        )

    def test_assign_to_group(self):
        instance = Scene.get_sample_scene()

        value = instance.assign_to_group(
            entities=["myEntity"],
            group_name="test-scene-group",  # "remove_from_other_groups"
        )

        assert value, "Modify method failed."

    def test_set_visible(self):
        instance = Scene.get_sample_scene()

        value = instance.set_visible(entities=["myEntity"], is_visible=True)

        assert value, "Modify method failed."

    def test_set_background_image(self):
        instance = Scene.get_sample_scene()

        value = instance.set_background_image(
            file_path="bg-image.png", location_x=0, location_y=0
        )

        assert value, "Modify method failed."
