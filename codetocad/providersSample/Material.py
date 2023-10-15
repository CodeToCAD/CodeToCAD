# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from CodeToCAD.interfaces import MaterialInterface
from CodeToCAD.CodeToCADTypes import *
from CodeToCAD.utilities import *


class Material(MaterialInterface): 
    
    
    name:str
    description:Optional[str]=None

    def __init__(self, name:str, description:Optional[str]=None):
        self.name = name
        self.description = description

    def assignToPart(self, partNameOrInstance:PartOrItsName):
        
        return self
        

    def setColor(self, rValue:IntOrFloat, gValue:IntOrFloat, bValue:IntOrFloat, aValue:IntOrFloat=1.0):
        
        return self
        

    def setReflectivity(self, reflectivity:float):
        
        return self
        

    def setRoughness(self, roughness:float):
        
        return self
        

    def addImageTexture(self, imageFilePath:str):
        
        return self
        
    