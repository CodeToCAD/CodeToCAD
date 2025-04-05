from tests.test_providers import *
from codetocad.tests_interfaces.camera_test_interface import CameraTestInterface


class CameraTest(TestProviderCase, CameraTestInterface):
    def test_create_perspective(self):
        value = Camera.create_perspective()

        assert value.is_exists(), "Create method failed."

    def test_create_orthogonal(self):
        value = Camera.create_orthogonal()

        assert value.is_exists(), "Create method failed."

    def test_create_panoramic(self):

        value = Camera.create_panoramic()

        assert value.is_exists(), "Create method failed."

    def test_set_focal_length(self):
        value = Camera.create_orthogonal().set_focal_length(length=2)

        assert value, "Modify method failed."
