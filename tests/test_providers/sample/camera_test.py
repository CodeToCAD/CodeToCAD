# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from tests.test_providers import *

from codetocad.tests_interfaces.camera_test_interface import CameraTestInterface


class CameraTest(TestProviderCase, CameraTestInterface):

    def test_create_perspective(self):

        instance = Camera(name="String", description="String", native_instance="value")

        value = instance.create_perspective()

        assert value.is_exists(), "Create method failed."

    def test_create_orthogonal(self):

        instance = Camera(name="String", description="String", native_instance="value")

        value = instance.create_orthogonal()

        assert value.is_exists(), "Create method failed."

    def test_create_panoramic(self):

        instance = Camera(name="String", description="String", native_instance="value")

        value = instance.create_panoramic()

        assert value.is_exists(), "Create method failed."

    def test_set_focal_length(self):

        instance = Camera(name="String", description="String", native_instance="value")

        value = instance.set_focal_length(length=0.0)

        assert value, "Modify method failed."
