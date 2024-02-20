# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from unittest import skip

from .test_helper import *
from codetocad.tests_interfaces import JointTestInterface


from codetocad import Entity


class JointTest(TestProviderCase, JointTestInterface):
    @skip("TODO")
    def test_translate_landmark_onto_another(self):
        instance = Joint(
            entity1=__import__("codetocad").Part("an entity"),
            entity2=__import__("codetocad").Part("an entity"),
        )

        value = instance.translate_landmark_onto_another()

        assert value, "Modify method failed."

    @skip("TODO")
    def test_pivot(self):
        instance = Joint(
            entity1=__import__("codetocad").Part("an entity"),
            entity2=__import__("codetocad").Part("an entity"),
        )

        value = instance.pivot()

        assert value, "Modify method failed."

    @skip("TODO")
    def test_gear_ratio(self):
        instance = Joint(
            entity1=__import__("codetocad").Part("an entity"),
            entity2=__import__("codetocad").Part("an entity"),
        )

        value = instance.gear_ratio(ratio=0.0)

        assert value, "Modify method failed."

    @skip("TODO")
    def test_limit_location_xyz(self):
        instance = Joint(
            entity1=__import__("codetocad").Part("an entity"),
            entity2=__import__("codetocad").Part("an entity"),
        )

        value = instance.limit_location_xyz(
            x=Dimension(0, "mm"), y=Dimension(0, "mm"), z=Dimension(0, "mm")
        )

        assert value, "Modify method failed."

    @skip("TODO")
    def test_limit_location_x(self):
        instance = Joint(
            entity1=__import__("codetocad").Part("an entity"),
            entity2=__import__("codetocad").Part("an entity"),
        )

        value = instance.limit_location_x(
            min=Dimension(0, "mm"), max=Dimension(0, "mm")
        )

        assert value, "Modify method failed."

    @skip("TODO")
    def test_limit_location_y(self):
        instance = Joint(
            entity1=__import__("codetocad").Part("an entity"),
            entity2=__import__("codetocad").Part("an entity"),
        )

        value = instance.limit_location_y(
            min=Dimension(0, "mm"), max=Dimension(0, "mm")
        )

        assert value, "Modify method failed."

    @skip("TODO")
    def test_limit_location_z(self):
        instance = Joint(
            entity1=__import__("codetocad").Part("an entity"),
            entity2=__import__("codetocad").Part("an entity"),
        )

        value = instance.limit_location_z(
            min=Dimension(0, "mm"), max=Dimension(0, "mm")
        )

        assert value, "Modify method failed."

    @skip("TODO")
    def test_limit_rotation_xyz(self):
        instance = Joint(
            entity1=__import__("codetocad").Part("an entity"),
            entity2=__import__("codetocad").Part("an entity"),
        )

        value = instance.limit_rotation_xyz(x=Angle("90"), y=Angle("90"), z=Angle("90"))

        assert value, "Modify method failed."

    @skip("TODO")
    def test_limit_rotation_x(self):
        instance = Joint(
            entity1=__import__("codetocad").Part("an entity"),
            entity2=__import__("codetocad").Part("an entity"),
        )

        value = instance.limit_rotation_x(min=Angle("90"), max=Angle("90"))

        assert value, "Modify method failed."

    @skip("TODO")
    def test_limit_rotation_y(self):
        instance = Joint(
            entity1=__import__("codetocad").Part("an entity"),
            entity2=__import__("codetocad").Part("an entity"),
        )

        value = instance.limit_rotation_y(min=Angle("90"), max=Angle("90"))

        assert value, "Modify method failed."

    @skip("TODO")
    def test_limit_rotation_z(self):
        instance = Joint(
            entity1=__import__("codetocad").Part("an entity"),
            entity2=__import__("codetocad").Part("an entity"),
        )

        value = instance.limit_rotation_z(min=Angle("90"), max=Angle("90"))

        assert value, "Modify method failed."
