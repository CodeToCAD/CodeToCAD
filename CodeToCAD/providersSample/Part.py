# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from CodeToCAD.interfaces import PartInterface
from CodeToCAD.CodeToCADTypes import *
from CodeToCAD.utilities import *

from . import Entity


class Part(Entity, PartInterface): 
    
    

    def createCube(self, width:DimensionOrItsFloatOrStringValue, length:DimensionOrItsFloatOrStringValue, height:DimensionOrItsFloatOrStringValue, keywordArguments:Optional[dict]=None):
        
        return self
        

    def createCone(self, radius:DimensionOrItsFloatOrStringValue, height:DimensionOrItsFloatOrStringValue, draftRadius:DimensionOrItsFloatOrStringValue=0, keywordArguments:Optional[dict]=None):
        
        return self
        

    def createCylinder(self, radius:DimensionOrItsFloatOrStringValue, height:DimensionOrItsFloatOrStringValue, keywordArguments:Optional[dict]=None):
        
        return self
        

    def createTorus(self, innerRadius:DimensionOrItsFloatOrStringValue, outerRadius:DimensionOrItsFloatOrStringValue, keywordArguments:Optional[dict]=None):
        
        return self
        

    def createSphere(self, radius:DimensionOrItsFloatOrStringValue, keywordArguments:Optional[dict]=None):
        
        return self
        

    def createGear(self, outerRadius:DimensionOrItsFloatOrStringValue, addendum:DimensionOrItsFloatOrStringValue, innerRadius:DimensionOrItsFloatOrStringValue, dedendum:DimensionOrItsFloatOrStringValue, height:DimensionOrItsFloatOrStringValue, pressureAngle:AngleOrItsFloatOrStringValue="20d", numberOfTeeth:'int'=12, skewAngle:AngleOrItsFloatOrStringValue=0, conicalAngle:AngleOrItsFloatOrStringValue=0, crownAngle:AngleOrItsFloatOrStringValue=0, keywordArguments:Optional[dict]=None):
        
        return self
        

    def clone(self, newName:str, copyLandmarks:bool=True) -> 'PartInterface':
        
        raise NotImplementedError()
        

    def loft(self, Landmark1:'LandmarkInterface', Landmark2:'LandmarkInterface'):
        
        return self
        

    def union(self, withPart:PartOrItsName, deleteAfterUnion:bool=True, isTransferLandmarks:bool=False):
        
        return self
        

    def subtract(self, withPart:PartOrItsName, deleteAfterSubtract:bool=True, isTransferLandmarks:bool=False):
        
        return self
        

    def intersect(self, withPart:PartOrItsName, deleteAfterIntersect:bool=True, isTransferLandmarks:bool=False):
        
        return self
        

    def hollow(self, thicknessX:DimensionOrItsFloatOrStringValue, thicknessY:DimensionOrItsFloatOrStringValue, thicknessZ:DimensionOrItsFloatOrStringValue, startAxis:AxisOrItsIndexOrItsName="z", flipAxis:bool=False):
        
        return self
        

    def thicken(self, radius:DimensionOrItsFloatOrStringValue):
        
        return self
        

    def hole(self, holeLandmark:LandmarkOrItsName, radius:DimensionOrItsFloatOrStringValue, depth:DimensionOrItsFloatOrStringValue, normalAxis:AxisOrItsIndexOrItsName="z", flipAxis:bool=False, initialRotationX:AngleOrItsFloatOrStringValue=0.0, initialRotationY:AngleOrItsFloatOrStringValue=0.0, initialRotationZ:AngleOrItsFloatOrStringValue=0.0, mirrorAboutEntityOrLandmark:Optional[EntityOrItsNameOrLandmark]=None, mirrorAxis:AxisOrItsIndexOrItsName="x", mirror:bool=False, circularPatternInstanceCount:'int'=1, circularPatternInstanceSeparation:AngleOrItsFloatOrStringValue=0.0, circularPatternInstanceAxis:AxisOrItsIndexOrItsName="z", circularPatternAboutEntityOrLandmark:Optional[EntityOrItsNameOrLandmark]=None, linearPatternInstanceCount:'int'=1, linearPatternInstanceSeparation:DimensionOrItsFloatOrStringValue=0.0, linearPatternInstanceAxis:AxisOrItsIndexOrItsName="x", linearPattern2ndInstanceCount:'int'=1, linearPattern2ndInstanceSeparation:DimensionOrItsFloatOrStringValue=0.0, linearPattern2ndInstanceAxis:AxisOrItsIndexOrItsName="y"):
        
        return self
        

    def setMaterial(self, materialName:MaterialOrItsName):
        
        return self
        

    def isCollidingWithPart(self, otherPart:PartOrItsName) -> bool:
        
        raise NotImplementedError()
        

    def filletAllEdges(self, radius:DimensionOrItsFloatOrStringValue, useWidth:bool=False):
        
        return self
        

    def filletEdges(self, radius:DimensionOrItsFloatOrStringValue, landmarksNearEdges:list[LandmarkOrItsName], useWidth:bool=False):
        
        return self
        

    def filletFaces(self, radius:DimensionOrItsFloatOrStringValue, landmarksNearFaces:list[LandmarkOrItsName], useWidth:bool=False):
        
        return self
        

    def chamferAllEdges(self, radius:DimensionOrItsFloatOrStringValue):
        
        return self
        

    def chamferEdges(self, radius:DimensionOrItsFloatOrStringValue, landmarksNearEdges:list[LandmarkOrItsName]):
        
        return self
        

    def chamferFaces(self, radius:DimensionOrItsFloatOrStringValue, landmarksNearFaces:list[LandmarkOrItsName]):
        
        return self
        

    def selectVertexNearLandmark(self, landmarkName:Optional[LandmarkOrItsName]=None):
        
        return self
        

    def selectEdgeNearLandmark(self, landmarkName:Optional[LandmarkOrItsName]=None):
        
        return self
        

    def selectFaceNearLandmark(self, landmarkName:Optional[LandmarkOrItsName]=None):
        
        return self
        
    