# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod

from codetocad import Edge


from codetocad.tests_interfaces import (
    MirrorableTestInterface,
    PatternableTestInterface,
    SubdividableTestInterface,
    ProjectableTestInterface,
)


class EdgeTestInterface(
    MirrorableTestInterface,
    PatternableTestInterface,
    SubdividableTestInterface,
    ProjectableTestInterface,
    metaclass=ABCMeta,
):
    @abstractmethod
    def test_offset(self):
        instance = Edge()

        value = instance.offset("distance")

        assert value, "Get method failed."

    @abstractmethod
    def test_fillet(self):
        instance = Edge()

        value = instance.fillet("other_edge", "amount")

        assert value, "Modify method failed."

    @abstractmethod
    def test_set_is_construction(self):
        instance = Edge()

        value = instance.set_is_construction("is_construction")

        assert value, "Modify method failed."

    @abstractmethod
    def test_get_is_construction(self):
        instance = Edge()

        value = instance.get_is_construction("")

        assert value, "Get method failed."
