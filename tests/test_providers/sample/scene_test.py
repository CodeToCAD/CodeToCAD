# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from tests.test_providers import *

from codetocad.tests_interfaces.scene_test_interface import SceneTestInterface


class SceneTest(TestProviderCase, SceneTestInterface):

    def test_default(self):

        instance = Scene(name="String", description="String")

        value = instance.default()

        assert value, "Get method failed."

    def test_create(self):

        instance = Scene(name="String", description="String")

        value = instance.create()

        assert value.is_exists(), "Create method failed."

    def test_delete(self):

        instance = Scene(name="String", description="String")

        value = instance.delete()

    def test_is_exists(self):

        instance = Scene(name="String", description="String")

        value = instance.is_exists()

        assert value, "Get method failed."

    def test_get_selected_entity(self):

        instance = Scene(name="String", description="String")

        value = instance.get_selected_entity()

        assert value, "Get method failed."

    def test_export(self):

        instance = Scene(name="String", description="String")

        value = instance.export(
            file_path="String",
            entities=[__import__("codetocad").Part("an exportable part")],
            overwrite=True,
            scale=1.0,
        )

    def test_set_default_unit(self):

        instance = Scene(name="String", description="String")

        value = instance.set_default_unit(unit="mm")

        assert value, "Modify method failed."

    def test_create_group(self):

        instance = Scene(name="String", description="String")

        value = instance.create_group(name="String")

        assert value.is_exists(), "Create method failed."

    def test_delete_group(self):

        instance = Scene(name="String", description="String")

        value = instance.delete_group(name="String", remove_children=True)

    def test_remove_from_group(self):

        instance = Scene(name="String", description="String")

        value = instance.remove_from_group(entity_name="String", group_name="String")

    def test_assign_to_group(self):

        instance = Scene(name="String", description="String")

        value = instance.assign_to_group(
            entities=["__import__(\"codetocad\").Part('an entity')"],
            group_name="String",
            remove_from_other_groups=True,
        )

        assert value, "Modify method failed."

    def test_set_visible(self):

        instance = Scene(name="String", description="String")

        value = instance.set_visible(
            entities=["__import__(\"codetocad\").Part('an entity')"], is_visible=True
        )

        assert value, "Modify method failed."

    def test_set_background_image(self):

        instance = Scene(name="String", description="String")

        value = instance.set_background_image(
            file_path="String", location_x=0, location_y=0
        )

        assert value, "Modify method failed."
