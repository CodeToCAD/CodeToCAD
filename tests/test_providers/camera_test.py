# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from unittest import skip

from .test_helper import *
from codetocad.tests_interfaces import CameraTestInterface


class CameraTest(TestProviderCase, CameraTestInterface):
    @skip("TODO")
    def test_create_perspective(self):
        instance = Camera()

        value = instance.create_perspective("")

        assert value.is_exists(), "Create method failed."

    @skip("TODO")
    def test_create_orthogonal(self):
        instance = Camera()

        value = instance.create_orthogonal("")

        assert value.is_exists(), "Create method failed."

    @skip("TODO")
    def test_set_focal_length(self):
        instance = Camera()

        value = instance.set_focal_length("length")

        assert value, "Modify method failed."
