from tests.test_providers import *
from codetocad.tests_interfaces.landmark_test_interface import LandmarkTestInterface


class LandmarkTest(TestProviderCase, LandmarkTestInterface):

    def test_get_location_world(self):
        part = Part.create_cube(1, 1, 1)

        instance = part.create_landmark(0, 0, 0)

        value = instance.get_location_world()

        assert value, "Get method failed."

    def test_get_location_local(self):
        part = Part.create_cube(1, 1, 1)

        instance = part.create_landmark(0, 0, 0)

        value = instance.get_location_local()

        assert value, "Get method failed."

    def test_translate_xyz(self):
        part = Part.create_cube(1, 1, 1)

        instance = part.create_landmark(0, 0, 0)

        value = instance.translate_xyz(1, 1, 1)

        assert value, "Modify method failed."

    def test_clone(self):
        part = Part.create_cube(1, 1, 1)

        instance = part.create_landmark(0, 0, 0)

        value = instance.clone("new_name", "offset")

        assert value, "Get method failed."

    def test_get_parent(self):
        part = Part.create_cube(1, 1, 1)

        instance = part.create_landmark(0, 0, 0)

        value = instance.parent

        assert value, "Get method failed."
