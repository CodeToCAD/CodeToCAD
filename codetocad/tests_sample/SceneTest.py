# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from unittest import skip

from .test_helper import *
from codetocad.testsInterfaces import SceneTestInterface


class SceneTest(TestProviderCase, SceneTestInterface):

    @skip("TODO")
    def test_create(self):
        instance = Scene("name", "description")

        value = instance.create("")

        assert value.isExists(), "Create method failed."

    @skip("TODO")
    def test_delete(self):
        instance = Scene("name", "description")

        value = instance.delete("")

    @skip("TODO")
    def test_getSelectedEntity(self):
        instance = Scene("name", "description")

        value = instance.getSelectedEntity("")

        assert value, "Get method failed."

    @skip("TODO")
    def test_export(self):
        instance = Scene("name", "description")

        value = instance.export("filePath", "entities", "overwrite", "scale")

    @skip("TODO")
    def test_setDefaultUnit(self):
        instance = Scene("name", "description")

        value = instance.setDefaultUnit("unit")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_createGroup(self):
        instance = Scene("name", "description")

        value = instance.createGroup("name")

        assert value.isExists(), "Create method failed."

    @skip("TODO")
    def test_deleteGroup(self):
        instance = Scene("name", "description")

        value = instance.deleteGroup("name", "removeChildren")

    @skip("TODO")
    def test_removeFromGroup(self):
        instance = Scene("name", "description")

        value = instance.removeFromGroup("entityName", "groupName")

    @skip("TODO")
    def test_assignToGroup(self):
        instance = Scene("name", "description")

        value = instance.assignToGroup(
            "entities", "groupName", "removeFromOtherGroups")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_setVisible(self):
        instance = Scene("name", "description")

        value = instance.setVisible("entities", "isVisible")

        assert value, "Modify method failed."

    @skip("TODO")
    def test_setBackgroundImage(self):
        instance = Scene("name", "description")

        value = instance.setBackgroundImage(
            "filePath", "locationX", "locationY")

        assert value, "Modify method failed."
