from tests.test_providers import *
from codetocad.tests_interfaces.scene_test_interface import SceneTestInterface


class SceneTest(TestProviderCase, SceneTestInterface):
    def test_default(self):
        instance = Scene(name="String", description="String")

        value = instance.default()

        assert value, "Get method failed."

    def test_create(self):
        instance = Scene("myScene")

        value = instance.create()

        assert value.is_exists(), "Create method failed."

    def test_delete(self):
        instance = Scene("myScene")

        value = instance.delete()

    def test_is_exists(self):
        instance = Scene()

        value = instance.is_exists()

        assert value, "Get method failed."

    def test_get_selected_entity(self):
        instance = Scene("myScene")

        value = instance.get_selected_entity()

        assert value, "Get method failed."

    def test_export(self):
        instance = Scene("myScene")

        value = instance.export(
            file_path="scene-export.png",
            entities=[Entity("myEntity")],
        )

    def test_set_default_unit(self):
        instance = Scene("myScene")

        value = instance.set_default_unit(unit="mm")

        assert value, "Modify method failed."

    def test_create_group(self):
        instance = Scene("myScene")

        value = instance.create_group(name="test-scene-group")

        assert value.is_exists(), "Create method failed."

    def test_delete_group(self):
        instance = Scene("myScene")

        value = instance.delete_group(name="test-scene-group", remove_children=True)

    def test_remove_from_group(self):
        instance = Scene("myScene")

        value = instance.remove_from_group(
            entity_name="myEntity", group_name="test-scene-group"
        )

    def test_assign_to_group(self):
        instance = Scene("myScene")

        value = instance.assign_to_group(
            entities=["myEntity"],
            group_name="test-scene-group",  # "remove_from_other_groups"
        )

        assert value, "Modify method failed."

    def test_set_visible(self):
        instance = Scene("myScene")

        value = instance.set_visible(entities=["myEntity"], is_visible=True)

        assert value, "Modify method failed."

    def test_set_background_image(self):
        instance = Scene("myScene")

        value = instance.set_background_image(
            file_path="bg-image.png", location_x=0, location_y=0
        )

        assert value, "Modify method failed."
