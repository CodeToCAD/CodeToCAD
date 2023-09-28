# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from unittest import skip, TestCase

from CodeToCAD import Analytics
from CodeToCAD.testsInterfaces import AnalyticsTestInterface


class AnalyticsTest(TestCase, AnalyticsTestInterface):

    @skip("TODO")
    def test_measureDistance(self):
        instance = Analytics("")

        value = instance.measureDistance("entity1", "entity2")

        assert value, "Get method failed."

    @skip("TODO")
    def test_measureAngle(self):
        instance = Analytics("")

        value = instance.measureAngle("entity1", "entity2", "pivot")

        assert value, "Get method failed."

    @skip("TODO")
    def test_getWorldPose(self):
        instance = Analytics("")

        value = instance.getWorldPose("entity")

        assert value, "Get method failed."

    @skip("TODO")
    def test_getBoundingBox(self):
        instance = Analytics("")

        value = instance.getBoundingBox("entityName")

        assert value, "Get method failed."

    @skip("TODO")
    def test_getDimensions(self):
        instance = Analytics("")

        value = instance.getDimensions("entityName")

        assert value, "Get method failed."

    @skip("TODO")
    def test_log(self):
        instance = Analytics("")

        value = instance.log("message")

        assert value, "Modify method failed."
