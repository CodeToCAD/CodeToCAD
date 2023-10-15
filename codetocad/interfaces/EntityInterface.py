
# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

from abc import ABCMeta, abstractmethod
from CodeToCAD.CodeToCADTypes import *


class EntityInterface(metaclass=ABCMeta):
    '''Capabilities shared between Parts and Sketches.'''

    
    name:str
    description:Optional[str]=None

    @abstractmethod
    def __init__(self, name:str, description:Optional[str]=None):
        self.name = name
        self.description = description

    @abstractmethod
    def createFromFile(self, filePath:str, fileType:Optional[str]=None):
        '''
        Adds geometry to a part from a file. If the part does not exist, this will create it.
        '''
        
        print("createFromFile is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def isExists(self) -> bool:
        '''
        Check if an entity exists
        '''
        
        print("isExists is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def rename(self, newName:str, renamelinkedEntitiesAndLandmarks:bool=True):
        '''
        Rename the entity, with an option to rename linked landmarks and underlying data.
        '''
        
        print("rename is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def delete(self, removeChildren:bool):
        '''
        Delete the entity from the scene. You may need to delete an associated joint or other features.
        '''
        
        print("delete is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def isVisible(self) -> bool:
        '''
        Returns whether the entity is visible in the scene.
        '''
        
        print("isVisible is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def setVisible(self, isVisible:bool):
        '''
        Toggles visibility of an entity in the scene.
        '''
        
        print("setVisible is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def apply(self, rotation:bool=True, scale:bool=True, location:bool=False, modifiers:bool=True):
        '''
        Apply any modifications. This is application specific, but a general function is that it finalizes any changes made to an entity.
        '''
        
        print("apply is called in an abstract method. Please override this method.")
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
        Get the entities XYZ location relative to World Space.
        '''
        
        print("getLocationWorld is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def getLocationLocal(self) -> 'Point':
        '''
        Get the entities XYZ location relative to Local Space.
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
        

    @abstractmethod
    def export(self, filePath:str, overwrite:bool=True, scale:float=1.0):
        '''
        Export Entity. Use the filePath to control the export type, e.g. '/path/to/cube.obj' or '/path/to/curve.svg'
        '''
        
        print("export is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def mirror(self, mirrorAcrossEntityOrLandmark:EntityOrItsNameOrLandmark, axis:AxisOrItsIndexOrItsName, resultingMirroredEntityName:Optional[str]=None):
        '''
        Mirror an existing entity with respect to a landmark. If a name is provided, the mirror becomes a separate entity.
        '''
        
        print("mirror is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def linearPattern(self, instanceCount:'int', offset:DimensionOrItsFloatOrStringValue, directionAxis:AxisOrItsIndexOrItsName="z"):
        '''
        Pattern in a uniform direction.
        '''
        
        print("linearPattern is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def circularPattern(self, instanceCount:'int', separationAngle:AngleOrItsFloatOrStringValue, centerEntityOrLandmark:EntityOrItsNameOrLandmark, normalDirectionAxis:AxisOrItsIndexOrItsName="z"):
        '''
        Pattern in a circular direction.
        '''
        
        print("circularPattern is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def translateXYZ(self, x:DimensionOrItsFloatOrStringValue, y:DimensionOrItsFloatOrStringValue, z:DimensionOrItsFloatOrStringValue):
        '''
        Translate in the XYZ directions. Pass a number, Dimension or Dimension-String (e.g. '2cm') to scale to a specific length.
        '''
        
        print("translateXYZ is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def translateX(self, amount:DimensionOrItsFloatOrStringValue):
        '''
        Translate in the X direction. Pass a number or Dimension or Dimension-String (e.g. '2cm') to translate to a specific length.
        '''
        
        print("translateX is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def translateY(self, amount:DimensionOrItsFloatOrStringValue):
        '''
        Translate in the Y direction. Pass a number or Dimension or Dimension-String (e.g. '2cm') to translate to a specific length.
        '''
        
        print("translateY is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def translateZ(self, amount:DimensionOrItsFloatOrStringValue):
        '''
        Translate in the z direction. Pass a number or Dimension or Dimension-String (e.g. '2cm') to translate to a specific length.
        '''
        
        print("translateZ is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def scaleXYZ(self, x:DimensionOrItsFloatOrStringValue, y:DimensionOrItsFloatOrStringValue, z:DimensionOrItsFloatOrStringValue):
        '''
        Scale in the XYZ directions. Pass a number, Dimension or Dimension-String (e.g. '2cm') to scale to a specific length.
        '''
        
        print("scaleXYZ is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def scaleX(self, scale:DimensionOrItsFloatOrStringValue):
        '''
        Scale in the X direction. Pass a number, Dimension or Dimension-String (e.g. '2cm') to scale to a specific length.
        '''
        
        print("scaleX is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def scaleY(self, scale:DimensionOrItsFloatOrStringValue):
        '''
        Scale in the Y direction. Pass a number, Dimension or Dimension-String (e.g. '2cm') to scale to a specific length.
        '''
        
        print("scaleY is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def scaleZ(self, scale:DimensionOrItsFloatOrStringValue):
        '''
        Scale in the Z direction. Pass a number, Dimension or Dimension-String (e.g. '2cm') to scale to a specific length.
        '''
        
        print("scaleZ is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def scaleXByFactor(self, scaleFactor:float):
        '''
        Scale in the X direction by a multiple.
        '''
        
        print("scaleXByFactor is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def scaleYByFactor(self, scaleFactor:float):
        '''
        Scale in the Y direction by a multiple.
        '''
        
        print("scaleYByFactor is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def scaleZByFactor(self, scaleFactor:float):
        '''
        Scale in the X direction by a multiple.
        '''
        
        print("scaleZByFactor is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def scaleKeepAspectRatio(self, scale:DimensionOrItsFloatOrStringValue, axis:AxisOrItsIndexOrItsName):
        '''
        Scale in one axis and maintain the others. Pass a Dimension or Dimension-String (e.g. '2cm') to scale to a specific length.
        '''
        
        print("scaleKeepAspectRatio is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def rotateXYZ(self, x:AngleOrItsFloatOrStringValue, y:AngleOrItsFloatOrStringValue, z:AngleOrItsFloatOrStringValue):
        '''
        Rotate in the XYZ direction. Default units is degrees. Pass in a number, Angle or Angle-String (e.g. 'PI/4radians' or 'PI/4r' or '90d'
        '''
        
        print("rotateXYZ is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def rotateX(self, rotation:AngleOrItsFloatOrStringValue):
        '''
        Rotate in the X direction. Default units is degrees. Pass in a number, Angle or Angle-String (e.g. 'PI/4radians' or 'PI/4r' or '90d'
        '''
        
        print("rotateX is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def rotateY(self, rotation:AngleOrItsFloatOrStringValue):
        '''
        Rotate in the Y direction. Default units is degrees. Pass in a number, Angle or Angle-String (e.g. 'PI/4radians' or 'PI/4r' or '90d'
        '''
        
        print("rotateY is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def rotateZ(self, rotation:AngleOrItsFloatOrStringValue):
        '''
        Rotate in the Z direction. Default units is degrees. Pass in a number, Angle or Angle-String (e.g. 'PI/4radians' or 'PI/4r' or '90d'
        '''
        
        print("rotateZ is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def twist(self, angle:AngleOrItsFloatOrStringValue, screwPitch:DimensionOrItsFloatOrStringValue, interations:'int'=1, axis:AxisOrItsIndexOrItsName="z"):
        '''
        AKA Helix, Screw. Revolve an entity
        '''
        
        print("twist is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def remesh(self, strategy:str, amount:float):
        '''
        Remeshing should be capable of voxel or vertex based reconstruction, including decimating unnecessary vertices (if applicable).
        '''
        
        print("remesh is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def createLandmark(self, landmarkName:str, x:DimensionOrItsFloatOrStringValue, y:DimensionOrItsFloatOrStringValue, z:DimensionOrItsFloatOrStringValue) -> 'LandmarkInterface':
        '''
        Shortcut for creating and assigning a landmark to this entity. Returns a Landmark instance.
        '''
        
        print("createLandmark is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def getBoundingBox(self) -> 'BoundaryBox':
        '''
        Get the Boundary Box around the entity.
        '''
        
        print("getBoundingBox is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def getDimensions(self) -> 'Dimensions':
        '''
        Get the length span in each coordinate axis (X,Y,Z).
        '''
        
        print("getDimensions is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def getLandmark(self, landmarkName:PresetLandmarkOrItsName) -> 'LandmarkInterface':
        '''
        Get the landmark by name
        '''
        
        print("getLandmark is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        