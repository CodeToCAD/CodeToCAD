# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from CodeToCAD.interfaces import SceneInterface
from CodeToCAD.CodeToCADTypes import *
from CodeToCAD.utilities import *


class Scene(SceneInterface): 
    
    
    name:Optional[str]=None
    description:Optional[str]=None

    def __init__(self, name:Optional[str]=None, description:Optional[str]=None):
        self.name = name
        self.description = description

    @staticmethod
    def default() -> 'SceneInterface':
        return Scene()

    def create(self):
        
        return self
        

    def delete(self):
        
        return self
        

    def getSelectedEntity(self) -> 'EntityInterface':
        
        raise NotImplementedError()
        

    def export(self, filePath:str, entities:list[EntityOrItsName], overwrite:bool=True, scale:float=1.0):
        
        return self
        

    def setDefaultUnit(self, unit:LengthUnitOrItsName):
        
        return self
        

    def createGroup(self, name:str):
        
        return self
        

    def deleteGroup(self, name:str, removeChildren:bool):
        
        return self
        

    def removeFromGroup(self, entityName:str, groupName:str):
        
        return self
        

    def assignToGroup(self, entities:list[EntityOrItsName], groupName:str, removeFromOtherGroups:Optional[bool]=True):
        
        return self
        

    def setVisible(self, entities:list[EntityOrItsName], isVisible:bool):
        
        return self
        

    def setBackgroundImage(self, filePath:str, locationX:Optional[DimensionOrItsFloatOrStringValue]=0, locationY:Optional[DimensionOrItsFloatOrStringValue]=0):
        
        return self
        
    