# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod

from codetocad import Landmark


class LandmarkTestInterface(metaclass=ABCMeta):

    @abstractmethod
    def test_getLandmarkEntityName(self):
        instance = Landmark("name", "parentEntity", "description")

        value = instance.getLandmarkEntityName("")

        assert value, "Get method failed."

    @abstractmethod
    def test_getParentEntity(self):
        instance = Landmark("name", "parentEntity", "description")

        value = instance.getParentEntity("")

        assert value, "Get method failed."

    @abstractmethod
    def test_isExists(self):
        instance = Landmark("name", "parentEntity", "description")

        value = instance.isExists("")

        assert value, "Get method failed."

    @abstractmethod
    def test_rename(self):
        instance = Landmark("name", "parentEntity", "description")

        value = instance.rename("newName")

        assert value, "Modify method failed."

    @abstractmethod
    def test_delete(self):
        instance = Landmark("name", "parentEntity", "description")

        value = instance.delete("")

    @abstractmethod
    def test_isVisible(self):
        instance = Landmark("name", "parentEntity", "description")

        value = instance.isVisible("")

        assert value, "Get method failed."

    @abstractmethod
    def test_setVisible(self):
        instance = Landmark("name", "parentEntity", "description")

        value = instance.setVisible("isVisible")

    @abstractmethod
    def test_getNativeInstance(self):
        instance = Landmark("name", "parentEntity", "description")

        value = instance.getNativeInstance("")

        assert value, "Get method failed."

    @abstractmethod
    def test_getLocationWorld(self):
        instance = Landmark("name", "parentEntity", "description")

        value = instance.getLocationWorld("")

        assert value, "Get method failed."

    @abstractmethod
    def test_getLocationLocal(self):
        instance = Landmark("name", "parentEntity", "description")

        value = instance.getLocationLocal("")

        assert value, "Get method failed."

    @abstractmethod
    def test_select(self):
        instance = Landmark("name", "parentEntity", "description")

        value = instance.select("")
