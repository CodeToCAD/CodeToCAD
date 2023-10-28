# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from unittest import skip

from .test_helper import *
from codetocad.tests_interfaces import SubdividableTestInterface


class SubdividableTest(TestProviderCase, SubdividableTestInterface):
    @skip("TODO")
    def test_remesh(self):
        instance = Subdividable("")

        value = instance.remesh("strategy", "amount")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_subdivide(self):
        instance = Subdividable("")

        value = instance.subdivide("amount")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_decimate(self):
        instance = Subdividable("")

        value = instance.decimate("amount")

        assert value, "Modify method failed."
