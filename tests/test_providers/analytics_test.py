# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from unittest import skip

from .test_helper import *
from codetocad.tests_interfaces import AnalyticsTestInterface


class AnalyticsTest(TestProviderCase, AnalyticsTestInterface):
    def test_measure_distance(self):
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        instance = Sketch("mySketch2")

        instance.create_line(start_at=(0, 0, 0), end_at=(1, 1, 0))

        analytics = Analytics()

        value = analytics.measure_distance(entity1="mySketch", entity2="mySketch2")

        assert value, "Get method failed."

    def test_measure_angle(self):
        instance = Sketch("mySketch")

        instance.create_rectangle(length=5, width=5)

        instance = Sketch("mySketch2")

        instance.create_line(start_at=(0, 0, 0), end_at=(1, 1, 0))

        analytics = Analytics()

        value = analytics.measure_angle(
            entity1="mySketch",
            entity2="mySketch2",
        )
        # "pivot")

        assert value, "Get method failed."

    def test_get_world_pose(self):
        instance = Part("myCube")

        instance.create_cube(1, 1, 1)

        instance = Analytics()

        value = instance.get_world_pose(entity="mySketch")

        assert value, "Get method failed."

    def test_get_bounding_box(self):  # TypeError
        instance = Sketch("myCircle")

        instance.create_circle(radius="5mm")

        analytics = Analytics()

        value = analytics.get_bounding_box(entity_name="myCircle")

        assert value, "Get method failed."

    def test_get_dimensions(self):
        instance = Sketch("myCircle")

        instance.create_circle(radius="5mm")

        analytics = Analytics()

        value = analytics.get_dimensions(entity_name="myCircle")

        assert value, "Get method failed."

    def test_log(self):  #'Ops' object has no attribute 'codetocad'
        instance = Analytics()

        value = instance.log("message")

        assert value, "Modify method failed."
