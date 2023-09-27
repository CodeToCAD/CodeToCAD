# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

import BlenderActions
import BlenderDefinitions

from CodeToCAD.interfaces import MaterialInterface, PartInterface
from CodeToCAD.CodeToCADTypes import *
from CodeToCAD.utilities import *


class Material(MaterialInterface):

    name: str
    description: Optional[str] = None

    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description

        try:
            BlenderActions.getMaterial(self.name)
        except:
            BlenderActions.createMaterial(self.name)

    def assignToPart(self, partName: PartOrItsName
                     ):
        if isinstance(partName, PartInterface):
            partName = partName.name
        BlenderActions.setMaterialToObject(self.name, partName)
        return self

    def setColor(self, rValue: IntOrFloat, gValue: IntOrFloat, bValue: IntOrFloat, aValue: IntOrFloat = 1.0
                 ):
        BlenderActions.setMaterialColor(
            self.name, rValue, gValue, bValue, aValue)
        return self

    def setReflectivity(self, reflectivity: float):

        BlenderActions.setMaterialMetallicness(self.name, reflectivity)

        return self

    def setRoughness(self, roughness: float):

        BlenderActions.setMaterialRoughness(self.name, roughness)

        return self

    def addImageTexture(self, imageFilePath: str
                        ):
        absoluteFilePath = getAbsoluteFilepath(imageFilePath)

        BlenderActions.addTextureToMaterial(self.name, absoluteFilePath)
        return self
