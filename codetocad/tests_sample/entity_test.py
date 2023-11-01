# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from unittest import skip

from .test_helper import *
from codetocad.tests_interfaces import EntityTestInterface


class EntityTest(TestProviderCase, EntityTestInterface):
    @skip("TODO")
    def test_is_exists(self):
        instance = Entity()

        value = instance.is_exists("")

        assert value, "Get method failed."

    @skip("TODO")
    def test_rename(self):
        instance = Entity()

        value = instance.rename("new_name", "renamelinked_entities_and_landmarks")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_delete(self):
        instance = Entity()

        value = instance.delete("remove_children")

    @skip("TODO")
    def test_is_visible(self):
        instance = Entity()

        value = instance.is_visible("")

        assert value, "Get method failed."

    @skip("TODO")
    def test_set_visible(self):
        instance = Entity()

        value = instance.set_visible("is_visible")

    @skip("TODO")
    def test_apply(self):
        instance = Entity()

        value = instance.apply("rotation", "scale", "location", "modifiers")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_get_native_instance(self):
        instance = Entity()

        value = instance.get_native_instance("")

        assert value, "Get method failed."

    @skip("TODO")
    def test_get_location_world(self):
        instance = Entity()

        value = instance.get_location_world("")

        assert value, "Get method failed."

    @skip("TODO")
    def test_get_location_local(self):
        instance = Entity()

        value = instance.get_location_local("")

        assert value, "Get method failed."

    @skip("TODO")
    def test_select(self):
        instance = Entity()

        value = instance.select("")

    @skip("TODO")
    def test_translate_xyz(self):
        instance = Entity()

        value = instance.translate_xyz("x", "y", "z")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_translate_x(self):
        instance = Entity()

        value = instance.translate_x("amount")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_translate_y(self):
        instance = Entity()

        value = instance.translate_y("amount")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_translate_z(self):
        instance = Entity()

        value = instance.translate_z("amount")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_rotate_xyz(self):
        instance = Entity()

        value = instance.rotate_xyz("x", "y", "z")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_rotate_x(self):
        instance = Entity()

        value = instance.rotate_x("rotation")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_rotate_y(self):
        instance = Entity()

        value = instance.rotate_y("rotation")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_rotate_z(self):
        instance = Entity()

        value = instance.rotate_z("rotation")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_get_bounding_box(self):
        instance = Entity()

        value = instance.get_bounding_box("")

        assert value, "Get method failed."

    @skip("TODO")
    def test_get_dimensions(self):
        instance = Entity()

        value = instance.get_dimensions("")

        assert value, "Get method failed."

    @skip("TODO")
    def test_create_landmark(self):
        instance = Entity()

        value = instance.create_landmark("landmark_name", "x", "y", "z")

        assert value, "Get method failed."

    @skip("TODO")
    def test_get_landmark(self):
        instance = Entity()

        value = instance.get_landmark("landmark_name")

        assert value, "Get method failed."
