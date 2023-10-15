
# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

from abc import ABCMeta, abstractmethod
from CodeToCAD.CodeToCADTypes import *


class CameraInterface(metaclass=ABCMeta):
    '''Manipulate a camera object.'''

    
    name:str
    description:Optional[str]=None

    @abstractmethod
    def __init__(self, name:str, description:Optional[str]=None):
        self.name = name
        self.description = description

    @abstractmethod
    def createPerspective(self):
        '''
        Create a perspective camera in the scene.
        '''
        
        print("createPerspective is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def createOrthogonal(self):
        '''
        Create an orthogonal camera in the scene.
        '''
        
        print("createOrthogonal is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def setFocalLength(self, length:float):
        '''
        Set the focal length of the camera.
        '''
        
        print("setFocalLength is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def translateXYZ(self, x:DimensionOrItsFloatOrStringValue, y:DimensionOrItsFloatOrStringValue, z:DimensionOrItsFloatOrStringValue):
        '''
        Translate in the XYZ directions. Pass a number, Dimension or Dimension-String (e.g. '2cm') to scale to a specific length.
        '''
        
        print("translateXYZ is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def rotateXYZ(self, x:AngleOrItsFloatOrStringValue, y:AngleOrItsFloatOrStringValue, z:AngleOrItsFloatOrStringValue):
        '''
        Rotate in the XYZ direction. Default units is degrees. Pass in a number, Angle or Angle-String (e.g. 'PI/4radians' or 'PI/4r' or '90d'
        '''
        
        print("rotateXYZ is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def isExists(self) -> bool:
        '''
        Check if an camera exists
        '''
        
        print("isExists is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def rename(self, newName:str):
        '''
        Rename the camera.
        '''
        
        print("rename is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def delete(self):
        '''
        Delete the camera from the scene.
        '''
        
        print("delete is called in an abstract method. Please override this method.")
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
        Get the camera XYZ location relative to World Space.
        '''
        
        print("getLocationWorld is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def getLocationLocal(self) -> 'Point':
        '''
        Get the camera XYZ location relative to Local Space.
        '''
        
        print("getLocationLocal is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def select(self):
        '''
        Select the entity (in UI).
        '''
        
        print("select is called in an abstract method. Please override this method.")
        return self
        