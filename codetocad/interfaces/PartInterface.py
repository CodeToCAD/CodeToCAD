
# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

from abc import ABCMeta, abstractmethod
from CodeToCAD.CodeToCADTypes import *

from CodeToCAD.interfaces import EntityInterface


class PartInterface(EntityInterface, metaclass=ABCMeta):
    '''Create and manipulate 3D shapes.'''

    

    @abstractmethod
    def createCube(self, width:DimensionOrItsFloatOrStringValue, length:DimensionOrItsFloatOrStringValue, height:DimensionOrItsFloatOrStringValue, keywordArguments:Optional[dict]=None):
        '''
        Adds cuboid geometry to a part.
        '''
        
        print("createCube is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def createCone(self, radius:DimensionOrItsFloatOrStringValue, height:DimensionOrItsFloatOrStringValue, draftRadius:DimensionOrItsFloatOrStringValue=0, keywordArguments:Optional[dict]=None):
        '''
        Adds cone geometry to a part.
        '''
        
        print("createCone is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def createCylinder(self, radius:DimensionOrItsFloatOrStringValue, height:DimensionOrItsFloatOrStringValue, keywordArguments:Optional[dict]=None):
        '''
        Adds cylinder geometry to a part.
        '''
        
        print("createCylinder is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def createTorus(self, innerRadius:DimensionOrItsFloatOrStringValue, outerRadius:DimensionOrItsFloatOrStringValue, keywordArguments:Optional[dict]=None):
        '''
        Adds torus geometry to a part.
        '''
        
        print("createTorus is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def createSphere(self, radius:DimensionOrItsFloatOrStringValue, keywordArguments:Optional[dict]=None):
        '''
        Adds sphere geometry to a part.
        '''
        
        print("createSphere is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def createGear(self, outerRadius:DimensionOrItsFloatOrStringValue, addendum:DimensionOrItsFloatOrStringValue, innerRadius:DimensionOrItsFloatOrStringValue, dedendum:DimensionOrItsFloatOrStringValue, height:DimensionOrItsFloatOrStringValue, pressureAngle:AngleOrItsFloatOrStringValue="20d", numberOfTeeth:'int'=12, skewAngle:AngleOrItsFloatOrStringValue=0, conicalAngle:AngleOrItsFloatOrStringValue=0, crownAngle:AngleOrItsFloatOrStringValue=0, keywordArguments:Optional[dict]=None):
        '''
        Adds gear geometry to a part.
        '''
        
        print("createGear is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def clone(self, newName:str, copyLandmarks:bool=True) -> 'PartInterface':
        '''
        Clone an existing Part with its geometry and properties. Returns the new Part.
        '''
        
        print("clone is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def loft(self, Landmark1:'LandmarkInterface', Landmark2:'LandmarkInterface'):
        '''
        Interpolate between two existing parts.
        '''
        
        print("loft is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def union(self, withPart:PartOrItsName, deleteAfterUnion:bool=True, isTransferLandmarks:bool=False):
        '''
        Boolean union
        '''
        
        print("union is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def subtract(self, withPart:PartOrItsName, deleteAfterSubtract:bool=True, isTransferLandmarks:bool=False):
        '''
        Boolean subtraction
        '''
        
        print("subtract is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def intersect(self, withPart:PartOrItsName, deleteAfterIntersect:bool=True, isTransferLandmarks:bool=False):
        '''
        Boolean intersection
        '''
        
        print("intersect is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def hollow(self, thicknessX:DimensionOrItsFloatOrStringValue, thicknessY:DimensionOrItsFloatOrStringValue, thicknessZ:DimensionOrItsFloatOrStringValue, startAxis:AxisOrItsIndexOrItsName="z", flipAxis:bool=False):
        '''
        Remove vertices, if necessary, until the part has a specified wall thickness.
        '''
        
        print("hollow is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def thicken(self, radius:DimensionOrItsFloatOrStringValue):
        '''
        Uniformly add a wall around a Part.
        '''
        
        print("thicken is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def hole(self, holeLandmark:LandmarkOrItsName, radius:DimensionOrItsFloatOrStringValue, depth:DimensionOrItsFloatOrStringValue, normalAxis:AxisOrItsIndexOrItsName="z", flipAxis:bool=False, initialRotationX:AngleOrItsFloatOrStringValue=0.0, initialRotationY:AngleOrItsFloatOrStringValue=0.0, initialRotationZ:AngleOrItsFloatOrStringValue=0.0, mirrorAboutEntityOrLandmark:Optional[EntityOrItsNameOrLandmark]=None, mirrorAxis:AxisOrItsIndexOrItsName="x", mirror:bool=False, circularPatternInstanceCount:'int'=1, circularPatternInstanceSeparation:AngleOrItsFloatOrStringValue=0.0, circularPatternInstanceAxis:AxisOrItsIndexOrItsName="z", circularPatternAboutEntityOrLandmark:Optional[EntityOrItsNameOrLandmark]=None, linearPatternInstanceCount:'int'=1, linearPatternInstanceSeparation:DimensionOrItsFloatOrStringValue=0.0, linearPatternInstanceAxis:AxisOrItsIndexOrItsName="x", linearPattern2ndInstanceCount:'int'=1, linearPattern2ndInstanceSeparation:DimensionOrItsFloatOrStringValue=0.0, linearPattern2ndInstanceAxis:AxisOrItsIndexOrItsName="y"):
        '''
        Create a hole.
        '''
        
        print("hole is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def setMaterial(self, materialName:MaterialOrItsName):
        '''
        Assign a known material to this part.
        '''
        
        print("setMaterial is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def isCollidingWithPart(self, otherPart:PartOrItsName) -> bool:
        '''
        Check if this part is colliding with another.
        '''
        
        print("isCollidingWithPart is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def filletAllEdges(self, radius:DimensionOrItsFloatOrStringValue, useWidth:bool=False):
        '''
        Fillet all edges.
        '''
        
        print("filletAllEdges is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def filletEdges(self, radius:DimensionOrItsFloatOrStringValue, landmarksNearEdges:list[LandmarkOrItsName], useWidth:bool=False):
        '''
        Fillet specific edges.
        '''
        
        print("filletEdges is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def filletFaces(self, radius:DimensionOrItsFloatOrStringValue, landmarksNearFaces:list[LandmarkOrItsName], useWidth:bool=False):
        '''
        Fillet specific faces.
        '''
        
        print("filletFaces is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def chamferAllEdges(self, radius:DimensionOrItsFloatOrStringValue):
        '''
        Chamfer all edges.
        '''
        
        print("chamferAllEdges is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def chamferEdges(self, radius:DimensionOrItsFloatOrStringValue, landmarksNearEdges:list[LandmarkOrItsName]):
        '''
        Chamfer specific edges.
        '''
        
        print("chamferEdges is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def chamferFaces(self, radius:DimensionOrItsFloatOrStringValue, landmarksNearFaces:list[LandmarkOrItsName]):
        '''
        Chamfer specific faces.
        '''
        
        print("chamferFaces is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def selectVertexNearLandmark(self, landmarkName:Optional[LandmarkOrItsName]=None):
        '''
        Select the vertex closest to a Landmark on the entity (in UI).
        '''
        
        print("selectVertexNearLandmark is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def selectEdgeNearLandmark(self, landmarkName:Optional[LandmarkOrItsName]=None):
        '''
        Select an edge closest to a landmark on the entity (in UI).
        '''
        
        print("selectEdgeNearLandmark is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def selectFaceNearLandmark(self, landmarkName:Optional[LandmarkOrItsName]=None):
        '''
        Select a face closest to a landmark on the entity (in UI).
        '''
        
        print("selectFaceNearLandmark is called in an abstract method. Please override this method.")
        return self
        