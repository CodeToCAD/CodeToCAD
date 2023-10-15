# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from CodeToCAD.interfaces import SketchInterface
from CodeToCAD.CodeToCADTypes import *
from CodeToCAD.utilities import *

from . import Entity


class Sketch(Entity, SketchInterface): 
    
    
    name:str
    curveType:Optional['CurveTypes']=None
    description:Optional[str]=None

    def __init__(self, name:str, curveType:Optional['CurveTypes']=None, description:Optional[str]=None):
        self.name = name
        self.curveType = curveType
        self.description = description

    def clone(self, newName:str, copyLandmarks:bool=True) -> 'SketchInterface':
        
        raise NotImplementedError()
        

    def revolve(self, angle:AngleOrItsFloatOrStringValue, aboutEntityOrLandmark:EntityOrItsNameOrLandmark, axis:AxisOrItsIndexOrItsName="z") -> 'PartInterface':
        
        raise NotImplementedError()
        

    def extrude(self, length:DimensionOrItsFloatOrStringValue) -> 'PartInterface':
        
        raise NotImplementedError()
        

    def sweep(self, profileNameOrInstance:SketchOrItsName, fillCap:bool=True) -> 'PartInterface':
        
        raise NotImplementedError()
        

    def offset(self, radius:DimensionOrItsFloatOrStringValue):
        
        return self
        

    def profile(self, profileCurveName:str):
        
        return self
        

    def createText(self, text:str, fontSize:DimensionOrItsFloatOrStringValue=1.0, bold:bool=False, italic:bool=False, underlined:bool=False, characterSpacing:'int'=1, wordSpacing:'int'=1, lineSpacing:'int'=1, fontFilePath:Optional[str]=None):
        
        return self
        

    def createFromVertices(self, coordinates:list[PointOrListOfFloatOrItsStringValue], interpolation:'int'=64):
        
        return self
        

    def createPoint(self, coordinate:PointOrListOfFloatOrItsStringValue):
        
        return self
        

    def createLine(self, length:DimensionOrItsFloatOrStringValue, angleX:AngleOrItsFloatOrStringValue=0.0, angleY:AngleOrItsFloatOrStringValue=0.0, symmetric:bool=False):
        
        return self
        

    def createLineBetweenPoints(self, endAt:PointOrListOfFloatOrItsStringValue, startAt:Optional[PointOrListOfFloatOrItsStringValue]=None):
        
        return self
        

    def createCircle(self, radius:DimensionOrItsFloatOrStringValue):
        
        return self
        

    def createEllipse(self, radiusA:DimensionOrItsFloatOrStringValue, radiusB:DimensionOrItsFloatOrStringValue):
        
        return self
        

    def createArc(self, radius:DimensionOrItsFloatOrStringValue, angle:AngleOrItsFloatOrStringValue="180d"):
        
        return self
        

    def createArcBetweenThreePoints(self, pointA:'Point', pointB:'Point', centerPoint:'Point'):
        
        return self
        

    def createSegment(self, innerRadius:DimensionOrItsFloatOrStringValue, outerRadius:DimensionOrItsFloatOrStringValue, angle:AngleOrItsFloatOrStringValue="180d"):
        
        return self
        

    def createRectangle(self, length:DimensionOrItsFloatOrStringValue, width:DimensionOrItsFloatOrStringValue):
        
        return self
        

    def createPolygon(self, numberOfSides:'int', length:DimensionOrItsFloatOrStringValue, width:DimensionOrItsFloatOrStringValue):
        
        return self
        

    def createTrapezoid(self, lengthUpper:DimensionOrItsFloatOrStringValue, lengthLower:DimensionOrItsFloatOrStringValue, height:DimensionOrItsFloatOrStringValue):
        
        return self
        

    def createSpiral(self, numberOfTurns:'int', height:DimensionOrItsFloatOrStringValue, radius:DimensionOrItsFloatOrStringValue, isClockwise:bool=True, radiusEnd:Optional[DimensionOrItsFloatOrStringValue]=None):
        
        return self
        
    