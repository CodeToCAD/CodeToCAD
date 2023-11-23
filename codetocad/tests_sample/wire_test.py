# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from unittest import skip

from .test_helper import *
from codetocad.tests_interfaces import WireTestInterface


class WireTest(TestProviderCase, WireTestInterface):
    @skip("TODO")
    def test_mirror(self):
        instance = Wire()

        value = instance.mirror(
            "mirror_across_entity", "axis", "resulting_mirrored_entity_name"
        )

        assert value.is_exists(), "Create method failed."

    @skip("TODO")
    def test_linear_pattern(self):
        instance = Wire()

        value = instance.linear_pattern("instance_count", "offset", "direction_axis")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_circular_pattern(self):
        instance = Wire()

        value = instance.circular_pattern(
            "instance_count",
            "separation_angle",
            "center_entity_or_landmark",
            "normal_direction_axis",
        )

        assert value, "Modify method failed."

    @skip("TODO")
    def test_project(self):
        instance = Wire()

        value = instance.project("project_onto")

        assert value, "Get method failed."

    @skip("TODO")
    def test_is_closed(self):
        instance = Wire()

        value = instance.is_closed("")

        assert value, "Get method failed."

    @skip("TODO")
    def test_loft(self):
        instance = Wire()

        value = instance.loft("other", "new_part_name")

        assert value, "Get method failed."
