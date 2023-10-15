
# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

from abc import ABCMeta, abstractmethod
from CodeToCAD.CodeToCADTypes import *


class MaterialInterface(metaclass=ABCMeta):
    '''Materials affect the appearance and simulation properties of the parts.'''

    
    name:str
    description:Optional[str]=None

    @abstractmethod
    def __init__(self, name:str, description:Optional[str]=None):
        self.name = name
        self.description = description

    @abstractmethod
    def assignToPart(self, partNameOrInstance:PartOrItsName):
        '''
        Assigns the material to a part.
        '''
        
        print("assignToPart is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def setColor(self, rValue:IntOrFloat, gValue:IntOrFloat, bValue:IntOrFloat, aValue:IntOrFloat=1.0):
        '''
        Set the RGBA color of an entity. Supports 0-255 int or 0.0-1.0 float values.
        '''
        
        print("setColor is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def setReflectivity(self, reflectivity:float):
        '''
        Change the surface reflectivity (metallic luster) of the material.
        '''
        
        print("setReflectivity is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def setRoughness(self, roughness:float):
        '''
        Change the surface roughness of the material.
        '''
        
        print("setRoughness is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def addImageTexture(self, imageFilePath:str):
        '''
        Add a texture from an image file.
        '''
        
        print("addImageTexture is called in an abstract method. Please override this method.")
        return self
        