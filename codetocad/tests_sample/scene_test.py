# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from unittest import skip

from .test_helper import *
from codetocad.tests_interfaces import SceneTestInterface


class SceneTest(TestProviderCase, SceneTestInterface):
    @skip("TODO")
    def test_create(self):
        instance = Scene()

        value = instance.create("")

        assert value.is_exists(), "Create method failed."

    @skip("TODO")
    def test_delete(self):
        instance = Scene()

        value = instance.delete("")

    @skip("TODO")
    def test_get_selected_entity(self):
        instance = Scene()

        value = instance.get_selected_entity("")

        assert value, "Get method failed."

    @skip("TODO")
    def test_export(self):
        instance = Scene()

        value = instance.export("file_path", "entities", "overwrite", "scale")

    @skip("TODO")
    def test_set_default_unit(self):
        instance = Scene()

        value = instance.set_default_unit("unit")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_create_group(self):
        instance = Scene()

        value = instance.create_group("name")

        assert value.is_exists(), "Create method failed."

    @skip("TODO")
    def test_delete_group(self):
        instance = Scene()

        value = instance.delete_group("name", "remove_children")

    @skip("TODO")
    def test_remove_from_group(self):
        instance = Scene()

        value = instance.remove_from_group("entity_name", "group_name")

    @skip("TODO")
    def test_assign_to_group(self):
        instance = Scene()

        value = instance.assign_to_group(
            "entities", "group_name", "remove_from_other_groups"
        )

        assert value, "Modify method failed."

    @skip("TODO")
    def test_set_visible(self):
        instance = Scene()

        value = instance.set_visible("entities", "is_visible")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_set_background_image(self):
        instance = Scene()

        value = instance.set_background_image("file_path", "location_x", "location_y")

        assert value, "Modify method failed."
