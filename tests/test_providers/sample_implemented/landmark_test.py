from tests.test_providers import *
from codetocad.tests_interfaces.landmark_test_interface import LandmarkTestInterface


class LandmarkTest(TestProviderCase, LandmarkTestInterface):
    def test_get_location_world(self):
        instance = Landmark("test-landmark", parent_entity="myEntity")

        value = instance.get_location_world()

        assert value, "Get method failed."

    def test_get_location_local(self):
        instance = Landmark("test-landmark", parent_entity="myEntity")

        value = instance.get_location_local()

        assert value, "Get method failed."

    def test_translate_xyz(self):
        instance = Landmark("test-landmark", parent_entity="myEntity")

        value = instance.translate_xyz(1, 1, 1)

        assert value, "Modify method failed."

    def test_clone(self):
        instance = Landmark("test-landmark", parent_entity="myEntity")

        value = instance.clone("new_name", "offset", "new_parent")

        assert value, "Get method failed."

    def test_get_landmark_entity_name(self):
        instance = Landmark("test-landmark", parent_entity="myEntity")

        value = instance.get_landmark_entity_name()

        assert value, "Get method failed."

    def test_get_parent_entity(self):
        instance = Landmark("test-landmark", parent_entity="myEntity")

        value = instance.get_parent_entity()

        assert value, "Get method failed."
