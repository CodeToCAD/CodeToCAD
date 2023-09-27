
# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

from abc import ABCMeta, abstractmethod
from CodeToCAD.CodeToCADTypes import *


class SceneInterface(metaclass=ABCMeta):
    '''Scene, camera, lighting, rendering, animation, simulation and GUI related functionality.'''

    
    name:Optional[str]=None
    description:Optional[str]=None

    @abstractmethod
    def __init__(self, name:Optional[str]=None, description:Optional[str]=None):
        self.name = name
        self.description = description

    @staticmethod
    def default() -> 'SceneInterface':
        raise RuntimeError()
        

    @abstractmethod
    def create(self):
        '''
        Creates a new scene.
        '''
        
        print("create is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def delete(self):
        '''
        Deletes a scene.
        '''
        
        print("delete is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def getSelectedEntity(self) -> 'EntityInterface':
        '''
        Get the selected entity in the Scene.
        '''
        
        print("getSelectedEntity is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def export(self, filePath:str, entities:list[EntityOrItsName], overwrite:bool=True, scale:float=1.0):
        '''
        Export the entire scene or specific entities.
        '''
        
        print("export is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def setDefaultUnit(self, unit:LengthUnitOrItsName):
        '''
        Set the document's default measurements system.
        '''
        
        print("setDefaultUnit is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def createGroup(self, name:str):
        '''
        Create a new group
        '''
        
        print("createGroup is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def deleteGroup(self, name:str, removeChildren:bool):
        '''
        Delete a new group
        '''
        
        print("deleteGroup is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def removeFromGroup(self, entityName:str, groupName:str):
        '''
        Removes an existing entity from a group
        '''
        
        print("removeFromGroup is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def assignToGroup(self, entities:list[EntityOrItsName], groupName:str, removeFromOtherGroups:Optional[bool]=True):
        '''
        Assigns an existing entity to a new group
        '''
        
        print("assignToGroup is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def setVisible(self, entities:list[EntityOrItsName], isVisible:bool):
        '''
        Change the visibiltiy of the entity.
        '''
        
        print("setVisible is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def setBackgroundImage(self, filePath:str, locationX:Optional[DimensionOrItsFloatOrStringValue]=0, locationY:Optional[DimensionOrItsFloatOrStringValue]=0):
        '''
        Set the scene background image. This can be an image or an HDRI texture.
        '''
        
        print("setBackgroundImage is called in an abstract method. Please override this method.")
        return self
        