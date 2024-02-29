# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from unittest import skip

from tests.test_providers.sample import *
from tests.test_providers import TestProviderCase

from codetocad.tests_interfaces import LandmarkTestInterface


from codetocad import Landmark, Entity


class LandmarkTest(TestProviderCase, LandmarkTestInterface):
    @skip("TODO")
    def test_clone(self):
        instance = Landmark(
            name="String",
            parent_entity=__import__("codetocad").Part("an entity"),
            description="String",
            native_instance=value,
        )

        value = instance.clone(
            new_name="String",
            offset=Dimensions(
                Dimension(0, "mm"), Dimension(0, "mm"), Dimension(0, "mm")
            ),
            new_parent=__import__("codetocad").Part("an entity"),
        )

        assert value, "Get method failed."

    @skip("TODO")
    def test_get_landmark_entity_name(self):
        instance = Landmark(
            name="String",
            parent_entity=__import__("codetocad").Part("an entity"),
            description="String",
            native_instance=value,
        )

        value = instance.get_landmark_entity_name()

        assert value, "Get method failed."

    @skip("TODO")
    def test_get_parent_entity(self):
        instance = Landmark(
            name="String",
            parent_entity=__import__("codetocad").Part("an entity"),
            description="String",
            native_instance=value,
        )

        value = instance.get_parent_entity()

        assert value, "Get method failed."
