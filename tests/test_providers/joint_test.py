# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from unittest import skip

from .test_helper import *
from codetocad.tests_interfaces import JointTestInterface


class JointTest(TestProviderCase, JointTestInterface):
    
    def test_translate_landmark_onto_another(self):
        instance = Joint.get_dummy_obj()

        value = instance.translate_landmark_onto_another()

        assert value, "Modify method failed."

    
    def test_pivot(self):
        instance = Joint.get_dummy_obj()

        value = instance.pivot()

        assert value, "Modify method failed."

    
    def test_gear_ratio(self):
        instance = Joint.get_dummy_obj()

        value = instance.gear_ratio(ratio=0.5)

        assert value, "Modify method failed."

    
    def test_limit_location_xyz(self):
        instance = Joint.get_dummy_obj()

        value = instance.limit_location_xyz(x=0.5, y=1, z=-1)

        assert value, "Modify method failed."

    
    def test_limit_location_x(self):
        instance = Joint.get_dummy_obj()

        value = instance.limit_location_x(min=1, max=2)

        assert value, "Modify method failed."

    
    def test_limit_location_y(self):
        instance = Joint.get_dummy_obj()

        value = instance.limit_location_y(min=1, max=2)

        assert value, "Modify method failed."

    
    def test_limit_location_z(self):
        instance = Joint.get_dummy_obj()

        value = instance.limit_location_z(min=1, max=2)

        assert value, "Modify method failed."

    
    def test_limit_rotation_xyz(self):
        instance = Joint.get_dummy_obj()

        value = instance.limit_rotation_xyz(x=30, y=60, z=45)

        assert value, "Modify method failed."

    
    def test_limit_rotation_x(self):
        instance = Joint.get_dummy_obj()

        value = instance.limit_rotation_x(min=30, max=45)

        assert value, "Modify method failed."

    
    def test_limit_rotation_y(self):
        instance = Joint.get_dummy_obj()

        value = instance.limit_rotation_y(min=30, max=45)

        assert value, "Modify method failed."

    
    def test_limit_rotation_z(self):
        instance = Joint.get_dummy_obj()

        value = instance.limit_rotation_z(min=30, max=60)

        assert value, "Modify method failed."
