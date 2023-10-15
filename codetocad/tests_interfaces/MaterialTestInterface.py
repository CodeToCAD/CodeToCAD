# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod

from codetocad import Material


class MaterialTestInterface(metaclass=ABCMeta):

    @abstractmethod
    def test_assignToPart(self):
        instance = Material("name", "description")

        value = instance.assignToPart("partNameOrInstance")

        assert value, "Modify method failed."

    @abstractmethod
    def test_setColor(self):
        instance = Material("name", "description")

        value = instance.setColor("rValue", "gValue", "bValue", "aValue")

        assert value, "Modify method failed."

    @abstractmethod
    def test_setReflectivity(self):
        instance = Material("name", "description")

        value = instance.setReflectivity("reflectivity")

        assert value, "Modify method failed."

    @abstractmethod
    def test_setRoughness(self):
        instance = Material("name", "description")

        value = instance.setRoughness("roughness")

        assert value, "Modify method failed."

    @abstractmethod
    def test_addImageTexture(self):
        instance = Material("name", "description")

        value = instance.addImageTexture("imageFilePath")

        assert value, "Modify method failed."
