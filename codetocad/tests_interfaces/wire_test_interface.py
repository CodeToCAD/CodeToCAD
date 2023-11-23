# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod


from codetocad import Wire


from codetocad.tests_interfaces import (
    MirrorableTestInterface,
    PatternableTestInterface,
    ProjectableTestInterface,
)


class WireTestInterface(
    MirrorableTestInterface,
    PatternableTestInterface,
    ProjectableTestInterface,
    metaclass=ABCMeta,
):
    @abstractmethod
    def test_is_closed(self):
        instance = Wire()

        value = instance.is_closed("")

        assert value, "Get method failed."

    @abstractmethod
    def test_loft(self):
        instance = Wire()

        value = instance.loft("other", "new_part_name")

        assert value, "Get method failed."
