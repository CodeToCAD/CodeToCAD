# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from unittest import skip

from .test_helper import *
from codetocad.tests_interfaces import LandmarkTestInterface


class LandmarkTest(TestProviderCase, LandmarkTestInterface):
    @skip("TODO")
    def test_clone(self):
        instance = Landmark()

        value = instance.clone("new_name", "offset", "new_parent")

        assert value, "Get method failed."

    @skip("TODO")
    def test_get_landmark_entity_name(self):
        instance = Landmark()

        value = instance.get_landmark_entity_name("")

        assert value, "Get method failed."

    @skip("TODO")
    def test_get_parent_entity(self):
        instance = Landmark()

        value = instance.get_parent_entity("")

        assert value, "Get method failed."
