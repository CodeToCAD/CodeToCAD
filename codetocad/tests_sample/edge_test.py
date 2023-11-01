# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from unittest import skip

from .test_helper import *
from codetocad.tests_interfaces import EdgeTestInterface


class EdgeTest(TestProviderCase, EdgeTestInterface):
    @skip("TODO")
    def test_mirror(self):
        instance = Edge()

        value = instance.mirror(
            "mirror_across_entity", "axis", "resulting_mirrored_entity_name"
        )

        assert value.is_exists(), "Create method failed."

    @skip("TODO")
    def test_linear_pattern(self):
        instance = Edge()

        value = instance.linear_pattern("instance_count", "offset", "direction_axis")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_circular_pattern(self):
        instance = Edge()

        value = instance.circular_pattern(
            "instance_count",
            "separation_angle",
            "center_entity_or_landmark",
            "normal_direction_axis",
        )

        assert value, "Modify method failed."

    @skip("TODO")
    def test_remesh(self):
        instance = Edge()

        value = instance.remesh("strategy", "amount")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_subdivide(self):
        instance = Edge()

        value = instance.subdivide("amount")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_decimate(self):
        instance = Edge()

        value = instance.decimate("amount")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_project(self):
        instance = Edge()

        value = instance.project("project_onto")

        assert value, "Get method failed."

    @skip("TODO")
    def test_offset(self):
        instance = Edge()

        value = instance.offset("distance")

        assert value, "Get method failed."

    @skip("TODO")
    def test_fillet(self):
        instance = Edge()

        value = instance.fillet("other_edge", "amount")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_set_is_construction(self):
        instance = Edge()

        value = instance.set_is_construction("is_construction")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_get_is_construction(self):
        instance = Edge()

        value = instance.get_is_construction("")

        assert value, "Get method failed."
