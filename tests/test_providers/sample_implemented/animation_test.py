from tests.test_providers import *
from codetocad.tests_interfaces.animation_test_interface import AnimationTestInterface


class AnimationTest(TestProviderCase, AnimationTestInterface):
    def test_default(self):
        instance = Animation()

        value = instance.default()

        assert value, "Get method failed."

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
