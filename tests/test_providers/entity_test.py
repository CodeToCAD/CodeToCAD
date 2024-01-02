# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from unittest import skip

from .test_helper import *
from codetocad.tests_interfaces import EntityTestInterface


class EntityTest(TestProviderCase, EntityTestInterface):
    def test_is_exists(self):
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        value = instance.is_exists()

        assert value, "Get method failed."

    def test_rename(self):
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        # "renamelinked_entities_and_landmarks")
        value = instance.rename(
            "changeSketchName",
        )

        assert value, "Modify method failed."

    def test_delete(self):
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        value = instance.delete("remove_children")

    def test_is_visible(self):
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        value = instance.is_visible()

        assert value, "Get method failed."

    def test_set_visible(self):
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        value = instance.set_visible(is_visible=False)

    def test_apply(self):
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        value = instance.apply()  # "rotation", "scale", "location", "modifiers")

        assert value, "Modify method failed."

    def test_get_native_instance(self):
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        value = instance.get_native_instance()

        assert value, "Get method failed."

    def test_get_location_world(self):
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        value = instance.get_location_world()

        assert value, "Get method failed."

    def test_get_location_local(self):
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        value = instance.get_location_local()

        assert value, "Get method failed."

    def test_select(self):
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        value = instance.select()

    @skip("TODO")
    def test_translate_xyz(self):  # TypeError
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        value = instance.translate_xyz(x=1, y=2, z=3)

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
    def test_get_bounding_box(self):  # TypeError
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        value = instance.get_bounding_box()

        assert value, "Get method failed."

    def test_get_dimensions(self):
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        value = instance.get_dimensions()

        assert value, "Get method failed."

    def test_create_landmark(self):  # TypeError
        instance = Part("myCube")

        instance.create_cube(1, 1, 1)

        value = instance.create_landmark(landmark_name="test-lm", x=1, y=2, z=3)

        assert value, "Get method failed."

    def test_get_landmark(self):
        instance = Part("myCube")

        instance.create_cube(1, 1, 1)

        instance.create_landmark(landmark_name="test-lm", x=1, y=2, z=3)

        value = instance.get_landmark("test-lm")

        assert value, "Get method failed."
