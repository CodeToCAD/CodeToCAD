from tests.test_providers import *
from codetocad.tests_interfaces.analytics_test_interface import AnalyticsTestInterface


class AnalyticsTest(TestProviderCase, AnalyticsTestInterface):
    def test_measure_distance(self):
        instance = Sketch.create_rectangle(length=5, width=5)

        instance2 = Sketch.create_line_to(start_at=(0, 0, 0), to=(1, 1, 0))

        analytics = Analytics()

        value = analytics.measure_distance(
            entity_1=instance,
            entity_2=instance2,
        )

        assert value, "Get method failed."

    def test_measure_angle(self):
        instance = Sketch.create_rectangle(length=5, width=5)

        instance2 = Sketch.create_line_to(start_at=(0, 0, 0), to=(1, 1, 0))

        analytics = Analytics()

        value = analytics.measure_angle(
            entity_1=instance,
            entity_2=instance2,
        )
        # "pivot")

        assert value, "Get method failed."

    def test_get_world_pose(self):
        instance = Part.create_cube(1, 1, 1)

        value = Analytics().get_world_pose(entity=instance)

        assert value, "Get method failed."

    def test_get_bounding_box(self):  # TypeError
        instance = Sketch.create_circle(radius="5mm")

        value = Analytics().get_bounding_box(instance)

        assert value, "Get method failed."

    def test_get_dimensions(self):
        instance = Sketch.create_circle(radius="5mm")

        value = Analytics().get_dimensions(instance)

        assert value, "Get method failed."

    def test_log(self):
        value = Analytics().log("message")

        assert value is None, "Modify method failed."
