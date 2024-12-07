from tests.test_providers import *
from codetocad.tests_interfaces.joint_test_interface import JointTestInterface


def get_dummy_obj():
    instance = Sketch("mySketch")

    edge = instance.create_line_to(to=(0, 5, 0), start_at=(5, 10, 0))

    instance = Sketch("mySketch")

    edge2 = instance.create_line_to(to=(5, 10, 0), start_at=(5, 5, 0))

    return Joint(
        entity_1=edge,
        entity_2=edge2,
    )


class JointTest(TestProviderCase, JointTestInterface):
    def test_translate_landmark_onto_another(self):
        instance = get_dummy_obj()

        value = instance.translate_landmark_onto_another()

        assert value, "Modify method failed."

    def test_pivot(self):
        instance = get_dummy_obj()

        value = instance.pivot()

        assert value, "Modify method failed."

    def test_gear_ratio(self):
        instance = get_dummy_obj()

        value = instance.gear_ratio(ratio=0.5)

        assert value, "Modify method failed."

    def test_limit_location_xyz(self):
        instance = get_dummy_obj()

        value = instance.limit_location_xyz(x=0.5, y=1, z=-1)

        assert value, "Modify method failed."

    def test_limit_location_x(self):
        instance = get_dummy_obj()

        value = instance.limit_location_x(min=1, max=2)

        assert value, "Modify method failed."

    def test_limit_location_y(self):
        instance = get_dummy_obj()

        value = instance.limit_location_y(min=1, max=2)

        assert value, "Modify method failed."

    def test_limit_location_z(self):
        instance = get_dummy_obj()

        value = instance.limit_location_z(min=1, max=2)

        assert value, "Modify method failed."

    def test_limit_rotation_xyz(self):
        instance = get_dummy_obj()

        value = instance.limit_rotation_xyz(x=30, y=60, z=45)

        assert value, "Modify method failed."

    def test_limit_rotation_x(self):
        instance = get_dummy_obj()

        value = instance.limit_rotation_x(min=30, max=45)

        assert value, "Modify method failed."

    def test_limit_rotation_y(self):
        instance = get_dummy_obj()

        value = instance.limit_rotation_y(min=30, max=45)

        assert value, "Modify method failed."

    def test_limit_rotation_z(self):
        instance = get_dummy_obj()

        value = instance.limit_rotation_z(min=30, max=60)

        assert value, "Modify method failed."
