# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from unittest import skip

from tests.test_providers.sample import *
from tests.test_providers import TestProviderCase

from codetocad.tests_interfaces import AnimationTestInterface


from codetocad import Animation, Entity


class AnimationTest(TestProviderCase, AnimationTestInterface):
    @skip("TODO")
    def test_default(self):
        instance = Animation()

        value = instance.default()

        assert value, "Get method failed."

    @skip("TODO")
    def test_set_frame_start(self):
        instance = Animation()

        value = instance.set_frame_start(frame_number=0)

        assert value, "Modify method failed."

    @skip("TODO")
    def test_set_frame_end(self):
        instance = Animation()

        value = instance.set_frame_end(frame_number=0)

        assert value, "Modify method failed."

    @skip("TODO")
    def test_set_frame_current(self):
        instance = Animation()

        value = instance.set_frame_current(frame_number=0)

        assert value, "Modify method failed."

    @skip("TODO")
    def test_create_key_frame_location(self):
        instance = Animation()

        value = instance.create_key_frame_location(
            entity=__import__("codetocad").Part("an entity"), frame_number=0
        )

        assert value, "Modify method failed."

    @skip("TODO")
    def test_create_key_frame_rotation(self):
        instance = Animation()

        value = instance.create_key_frame_rotation(
            entity=__import__("codetocad").Part("an entity"), frame_number=0
        )

        assert value, "Modify method failed."
