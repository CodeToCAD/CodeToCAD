from tests.test_providers import *
from codetocad.tests_interfaces.scene_test_interface import SceneTestInterface


class SceneTest(TestProviderCase, SceneTestInterface):
    def test_default(self):
        value = Scene.default()

        assert value, "Get method failed."

    def test_create(self):
        instance = Scene.default()

        value = instance.create()

        assert value.is_exists(), "Create method failed."

    def test_delete(self):
        instance = Scene.default()

        value = instance.delete()

    def test_is_exists(self):
        instance = Scene.default()

        value = instance.is_exists()

        assert value, "Get method failed."

    def test_get_selected_entity(self):
        instance = Scene.default()

        value = instance.get_selected_entity()

        assert value, "Get method failed."

    def test_export(self):
        instance = Scene.default()

        part = Part.create_cube(1, 1, 1)

        value = instance.export(
            file_path="scene-export.png",
            entities=[part],
        )

        assert value, "Modify method failed."

    def test_set_default_unit(self):
        instance = Scene.default()

        value = instance.set_default_unit(unit="mm")

        assert value, "Modify method failed."

    def test_create_group(self):
        instance = Scene.default()

        value = instance.create_group(name="test-scene-group")

        assert value.is_exists(), "Create method failed."

    def test_delete_group(self):
        instance = Scene.default()

        value = instance.delete_group(name="test-scene-group", remove_children=True)

        assert value, "Modify method failed."

    def test_remove_from_group(self):
        instance = Scene.default()

        group_name = "test-scene-group"

        part = Part.create_cube(1, 1, 1)

        instance.assign_to_group([part], group_name)

        value = instance.remove_from_group(part, group_name=group_name)

        assert value, "Modify method failed."

    def test_assign_to_group(self):
        instance = Scene.default()

        part = Part.create_cube(1, 1, 1)

        value = instance.assign_to_group(
            entities=[part],
            group_name="test-scene-group",  # "remove_from_other_groups"
        )

        assert value, "Modify method failed."

    def test_set_visible(self):
        instance = Scene.default()

        part = Part.create_cube(1, 1, 1)

        value = instance.set_visible(entities=[part], is_visible=True)

        assert value, "Modify method failed."

        value = instance.set_visible(entities=[part], is_visible=False)

        assert value, "Modify method failed."

    def test_set_background_image(self):
        instance = Scene.default()

        value = instance.set_background_image(
            file_path="bg-image.png", location_x=0, location_y=0
        )

        assert value, "Modify method failed."

    def test_get_by_name(self):

        Scene.create("test_scene")

        instance = Scene.get_by_name(name="test_scene")

        assert instance.is_exists(), "Create method failed."
