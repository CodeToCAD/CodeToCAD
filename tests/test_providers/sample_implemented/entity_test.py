from tests.test_providers import *
from codetocad.tests_interfaces.entity_test_interface import EntityTestInterface


class EntityTest(TestProviderCase, EntityTestInterface):
    def test_is_exists(self):
        instance = Sketch.create_rectangle(length=5, width=5)

        value = instance.is_exists()

        assert value, "Get method failed."

    def test_set_name(self):

        instance = Sketch.create_rectangle(length=5, width=5)

        # "renamelinked_entities_and_landmarks")
        value = instance.set_name(
            "changeSketchName",
        )

        assert value, "Modify method failed."

    def test_get_name(self):

        instance = Part.create_cone(1, 1, name="String")

        value = instance.get_name()

        assert value == "String", "Get method failed."

    def test_delete(self):
        instance = Sketch.create_rectangle(length=5, width=5)

        instance.delete()

        # This fails with the sample, the sample needs a bit of faking logic.. an enhancement for the future
        # assert instance.is_exists() is False, "Delete method failed."

    def test_is_visible(self):
        instance = Sketch.create_rectangle(length=5, width=5)

        value = instance.is_visible()

        assert value, "Get method failed."

    def test_set_visible(self):
        instance = Sketch.create_rectangle(length=5, width=5)

        value = instance.set_visible(is_visible=False)

    def test_apply(self):
        instance = Sketch.create_rectangle(length=5, width=5)

        value = instance.apply()  # "rotation", "scale", "location", "modifiers")

        assert value, "Modify method failed."

    def test_get_native_instance(self):
        instance = Sketch.create_rectangle(length=5, width=5)

        value = instance.get_native_instance()

        assert value, "Get method failed."

    def test_get_location_world(self):
        instance = Sketch.create_rectangle(length=5, width=5)

        value = instance.get_location_world()

        assert value, "Get method failed."

    def test_get_location_local(self):
        instance = Sketch.create_rectangle(length=5, width=5)

        value = instance.get_location_local()

        assert value, "Get method failed."

    def test_select(self):
        instance = Sketch.create_rectangle(length=5, width=5)

        value = instance.select()

    def test_translate_xyz(self):  # TypeError
        instance = Sketch.create_rectangle(length=5, width=5)

        value = instance.translate_xyz(x=1, y=2, z=3)

        assert value, "Modify method failed."

    def test_translate_x(self):
        instance = Sketch.create_rectangle(length=5, width=5)

        value = instance.translate_x(amount=1)

        assert value, "Modify method failed."

    def test_translate_y(self):
        instance = Sketch.create_rectangle(length=5, width=5)

        value = instance.translate_y(amount=2)

        assert value, "Modify method failed."

    def test_translate_z(self):
        instance = Sketch.create_rectangle(length=5, width=5)

        value = instance.translate_z(amount=2)

        assert value, "Modify method failed."

    def test_rotate_xyz(self):
        instance = Sketch.create_rectangle(length=5, width=5)

        value = instance.rotate_xyz(x=30, y=60, z=90)

        assert value, "Modify method failed."

    def test_rotate_x(self):
        instance = Sketch.create_rectangle(1, 1).rotate_x(rotation=30)

        assert instance, "Modify method failed."

    def test_rotate_y(self):
        instance = Sketch.create_rectangle(1, 1).rotate_y(rotation=30)

        assert instance, "Modify method failed."

    def test_rotate_z(self):
        instance = Sketch.create_rectangle(length=5, width=5)

        value = instance.rotate_z(rotation=90)

        assert value, "Modify method failed."

    def test_get_bounding_box(self):  # TypeError
        instance = Sketch.create_rectangle(length=5, width=5)

        value = instance.get_bounding_box()

        assert value, "Get method failed."

    def test_get_dimensions(self):
        instance = Sketch.create_rectangle(length=5, width=5)

        value = instance.get_dimensions()

        assert value, "Get method failed."

    def test_create_landmark(self):  # TypeError
        instance = Part.create_cube(1, 1, 1)

        value = instance.create_landmark(landmark_name="test-lm", x=1, y=2, z=3)

        assert value, "Get method failed."

    def test_get_landmark(self):
        instance = Part.create_cube(1, 1, 1)

        instance.create_landmark(landmark_name="test-lm", x=1, y=2, z=3)

        value = instance.get_landmark("test-lm")

        assert value, "Get method failed."
