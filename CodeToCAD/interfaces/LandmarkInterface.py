
# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

from abc import ABCMeta, abstractmethod
from CodeToCAD.CodeToCADTypes import *


class LandmarkInterface(metaclass=ABCMeta):
    '''Landmarks are named positions on an entity.'''

    
    name:str
    parentEntity:EntityOrItsName
    description:Optional[str]=None

    @abstractmethod
    def __init__(self, name:str, parentEntity:EntityOrItsName, description:Optional[str]=None):
        self.name = name
        self.parentEntity = parentEntity
        self.description = description

    @abstractmethod
    def getLandmarkEntityName(self) -> str:
        '''
        Get the landmark object name in the scene, which may be different to the name of the landmark when it was first created. For example, the generated name may be {parentName}_{landmarkName}.
        '''
        
        print("getLandmarkEntityName is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def getParentEntity(self) -> 'EntityInterface':
        '''
        Get the name of the entity this landmark belongs to.
        '''
        
        print("getParentEntity is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def isExists(self) -> bool:
        '''
        Check if an landmark exists
        '''
        
        print("isExists is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def rename(self, newName:str):
        '''
        Rename the landmark.
        '''
        
        print("rename is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def delete(self):
        '''
        Delete the landmark from the scene.
        '''
        
        print("delete is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def isVisible(self) -> bool:
        '''
        Returns whether the landmark is visible in the scene.
        '''
        
        print("isVisible is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def setVisible(self, isVisible:bool):
        '''
        Toggles visibility of an landmark in the scene.
        '''
        
        print("setVisible is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def getNativeInstance(self) -> object:
        '''
        Get the native API's object instance. For example, in Blender API, this would return a bpy.object instance.
        '''
        
        print("getNativeInstance is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def getLocationWorld(self) -> 'Point':
        '''
        Get the landmark XYZ location relative to World Space.
        '''
        
        print("getLocationWorld is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def getLocationLocal(self) -> 'Point':
        '''
        Get the landmark XYZ location relative to Local Space.
        '''
        
        print("getLocationLocal is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def select(self):
        '''
        Select the landmark (in UI).
        '''
        
        print("select is called in an abstract method. Please override this method.")
        return self
        