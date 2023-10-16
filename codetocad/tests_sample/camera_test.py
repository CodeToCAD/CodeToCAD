# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from unittest import skip

from .test_helper import *
from codetocad.tests_interfaces import CameraTestInterface


class CameraTest(TestProviderCase, CameraTestInterface):

    @skip("TODO")
    def test_create_perspective(self):
        instance = Camera("name", "description")

        value = instance.create_perspective("")

        assert value.isExists(), "Create method failed."

    @skip("TODO")
    def test_create_orthogonal(self):
        instance = Camera("name", "description")

        value = instance.create_orthogonal("")

        assert value.isExists(), "Create method failed."

    @skip("TODO")
    def test_set_focal_length(self):
        instance = Camera("name", "description")

        value = instance.set_focal_length("length")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_translate_xyz(self):
        instance = Camera("name", "description")

        value = instance.translate_xyz("x", "y", "z")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_rotate_xyz(self):
        instance = Camera("name", "description")

        value = instance.rotate_xyz("x", "y", "z")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_is_exists(self):
        instance = Camera("name", "description")

        value = instance.is_exists("")

        assert value, "Get method failed."

    @skip("TODO")
    def test_rename(self):
        instance = Camera("name", "description")

        value = instance.rename("new_name")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_delete(self):
        instance = Camera("name", "description")

        value = instance.delete("")

    @skip("TODO")
    def test_get_native_instance(self):
        instance = Camera("name", "description")

        value = instance.get_native_instance("")

        assert value, "Get method failed."

    @skip("TODO")
    def test_get_location_world(self):
        instance = Camera("name", "description")

        value = instance.get_location_world("")

        assert value, "Get method failed."

    @skip("TODO")
    def test_get_location_local(self):
        instance = Camera("name", "description")

        value = instance.get_location_local("")

        assert value, "Get method failed."

    @skip("TODO")
    def test_select(self):
        instance = Camera("name", "description")

        value = instance.select("")
