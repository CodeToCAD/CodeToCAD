from .test_helper import *
from codetocad.tests_interfaces import LandmarkTestInterface


class LandmarkTest(TestProviderCase, LandmarkTestInterface):
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
