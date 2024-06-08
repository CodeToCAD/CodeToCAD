# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from tests.test_providers import *

from codetocad.tests_interfaces.entity_test_interface import EntityTestInterface


class EntityTest(TestProviderCase, EntityTestInterface):

    def test_is_exists(self):

        instance = Entity(name="String", description="String", native_instance="value")

        value = instance.is_exists()

        assert value, "Get method failed."

    def test_rename(self):

        instance = Entity(name="String", description="String", native_instance="value")

        value = instance.rename(
            new_name="String", renamelinked_entities_and_landmarks=True
        )

        assert value, "Modify method failed."

    def test_delete(self):

        instance = Entity(name="String", description="String", native_instance="value")

        value = instance.delete(remove_children=True)

    def test_is_visible(self):

        instance = Entity(name="String", description="String", native_instance="value")

        value = instance.is_visible()

        assert value, "Get method failed."

    def test_set_visible(self):

        instance = Entity(name="String", description="String", native_instance="value")

        value = instance.set_visible(is_visible=True)

    def test_apply(self):

        instance = Entity(name="String", description="String", native_instance="value")

        value = instance.apply(
            rotation=True, scale=True, location=False, modifiers=True
        )

        assert value, "Modify method failed."

    def test_get_native_instance(self):

        instance = Entity(name="String", description="String", native_instance="value")

        value = instance.get_native_instance()

        assert value, "Get method failed."

    def test_get_location_world(self):

        instance = Entity(name="String", description="String", native_instance="value")

        value = instance.get_location_world()

        assert value, "Get method failed."

    def test_get_location_local(self):

        instance = Entity(name="String", description="String", native_instance="value")

        value = instance.get_location_local()

        assert value, "Get method failed."

    def test_select(self):

        instance = Entity(name="String", description="String", native_instance="value")

        value = instance.select()

    def test_translate_xyz(self):

        instance = Entity(name="String", description="String", native_instance="value")

        value = instance.translate_xyz(
            x=Dimension(0, "mm"), y=Dimension(0, "mm"), z=Dimension(0, "mm")
        )

        assert value, "Modify method failed."

    def test_translate_x(self):

        instance = Entity(name="String", description="String", native_instance="value")

        value = instance.translate_x(amount=Dimension(0, "mm"))

        assert value, "Modify method failed."

    def test_translate_y(self):

        instance = Entity(name="String", description="String", native_instance="value")

        value = instance.translate_y(amount=Dimension(0, "mm"))

        assert value, "Modify method failed."

    def test_translate_z(self):

        instance = Entity(name="String", description="String", native_instance="value")

        value = instance.translate_z(amount=Dimension(0, "mm"))

        assert value, "Modify method failed."

    def test_rotate_xyz(self):

        instance = Entity(name="String", description="String", native_instance="value")

        value = instance.rotate_xyz(x=Angle(90), y=Angle(90), z=Angle(90))

        assert value, "Modify method failed."

    def test_rotate_x(self):

        instance = Entity(name="String", description="String", native_instance="value")

        value = instance.rotate_x(rotation=Angle(90))

        assert value, "Modify method failed."

    def test_rotate_y(self):

        instance = Entity(name="String", description="String", native_instance="value")

        value = instance.rotate_y(rotation=Angle(90))

        assert value, "Modify method failed."

    def test_rotate_z(self):

        instance = Entity(name="String", description="String", native_instance="value")

        value = instance.rotate_z(rotation=Angle(90))

        assert value, "Modify method failed."

    def test_get_bounding_box(self):

        instance = Entity(name="String", description="String", native_instance="value")

        value = instance.get_bounding_box()

        assert value, "Get method failed."

    def test_get_dimensions(self):

        instance = Entity(name="String", description="String", native_instance="value")

        value = instance.get_dimensions()

        assert value, "Get method failed."
