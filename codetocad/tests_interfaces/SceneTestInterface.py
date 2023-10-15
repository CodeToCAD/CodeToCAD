# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod

from codetocad import Scene


class SceneTestInterface(metaclass=ABCMeta):

    @abstractmethod
    def test_create(self):
        instance = Scene("name", "description")

        value = instance.create("")

        assert value.isExists(), "Create method failed."

    @abstractmethod
    def test_delete(self):
        instance = Scene("name", "description")

        value = instance.delete("")

    @abstractmethod
    def test_getSelectedEntity(self):
        instance = Scene("name", "description")

        value = instance.getSelectedEntity("")

        assert value, "Get method failed."

    @abstractmethod
    def test_export(self):
        instance = Scene("name", "description")

        value = instance.export("filePath", "entities", "overwrite", "scale")

    @abstractmethod
    def test_setDefaultUnit(self):
        instance = Scene("name", "description")

        value = instance.setDefaultUnit("unit")

        assert value, "Modify method failed."

    @abstractmethod
    def test_createGroup(self):
        instance = Scene("name", "description")

        value = instance.createGroup("name")

        assert value.isExists(), "Create method failed."

    @abstractmethod
    def test_deleteGroup(self):
        instance = Scene("name", "description")

        value = instance.deleteGroup("name", "removeChildren")

    @abstractmethod
    def test_removeFromGroup(self):
        instance = Scene("name", "description")

        value = instance.removeFromGroup("entityName", "groupName")

    @abstractmethod
    def test_assignToGroup(self):
        instance = Scene("name", "description")

        value = instance.assignToGroup(
            "entities", "groupName", "removeFromOtherGroups")

        assert value, "Modify method failed."

    @abstractmethod
    def test_setVisible(self):
        instance = Scene("name", "description")

        value = instance.setVisible("entities", "isVisible")

        assert value, "Modify method failed."

    @abstractmethod
    def test_setBackgroundImage(self):
        instance = Scene("name", "description")

        value = instance.setBackgroundImage(
            "filePath", "locationX", "locationY")

        assert value, "Modify method failed."
