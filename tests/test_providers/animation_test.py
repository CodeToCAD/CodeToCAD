# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from unittest import skip

from .test_helper import *
from codetocad.tests_interfaces import AnimationTestInterface


class AnimationTest(TestProviderCase, AnimationTestInterface):
    
    def test_set_frame_start(self):
        instance = Animation()

        value = instance.set_frame_start(frame_number=100)

        assert value, "Modify method failed."

    
    def test_set_frame_end(self):
        instance = Animation()

        value = instance.set_frame_end(frame_number=200)

        assert value, "Modify method failed."

    
    def test_set_frame_current(self):
        instance = Animation()

        value = instance.set_frame_current(frame_number=50)

        assert value, "Modify method failed."

    
    def test_create_key_frame_location(self):
        instance = Sketch("myCircle")

        instance.create_circle(radius="5mm")

        animation = Animation()

        value = animation.create_key_frame_location(entity="myCircle", frame_number=250)

        assert value, "Modify method failed."

    
    def test_create_key_frame_rotation(self):
        instance = Sketch("myCircle")

        instance.create_circle(radius="5mm")

        instance = Animation()

        value = instance.create_key_frame_rotation(entity="myCircle", frame_number=200)

        assert value, "Modify method failed."
