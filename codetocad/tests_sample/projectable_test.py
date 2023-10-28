# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from unittest import skip

from .test_helper import *
from codetocad.tests_interfaces import ProjectableTestInterface


class ProjectableTest(TestProviderCase, ProjectableTestInterface):
    @skip("TODO")
    def test_project(self):
        instance = Projectable("")

        value = instance.project("project_onto")

        assert value, "Get method failed."
