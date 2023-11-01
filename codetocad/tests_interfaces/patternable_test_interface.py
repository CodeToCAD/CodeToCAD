# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod

from codetocad import Patternable


class PatternableTestInterface(metaclass=ABCMeta):
    @abstractmethod
    def test_linear_pattern(self):
        instance = Patternable()

        value = instance.linear_pattern("instance_count", "offset", "direction_axis")

        assert value, "Modify method failed."

    @abstractmethod
    def test_circular_pattern(self):
        instance = Patternable()

        value = instance.circular_pattern(
            "instance_count",
            "separation_angle",
            "center_entity_or_landmark",
            "normal_direction_axis",
        )

        assert value, "Modify method failed."
