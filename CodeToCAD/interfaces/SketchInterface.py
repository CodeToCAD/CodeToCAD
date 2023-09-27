
# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

from abc import ABCMeta, abstractmethod
from CodeToCAD.CodeToCADTypes import *

from CodeToCAD.interfaces import EntityInterface


class SketchInterface(EntityInterface, metaclass=ABCMeta):
    '''Capabilities related to adding, multiplying, and/or modifying a curve.'''

    
    name:str
    curveType:Optional['CurveTypes']=None
    description:Optional[str]=None

    @abstractmethod
    def __init__(self, name:str, curveType:Optional['CurveTypes']=None, description:Optional[str]=None):
        super().__init__(name,description)
    
        self.name = name
        self.curveType = curveType
        self.description = description

    @abstractmethod
    def clone(self, newName:str, copyLandmarks:bool=True) -> 'SketchInterface':
        '''
        Clone an existing sketch with its geometry and properties. Returns the new Sketch.
        '''
        
        print("clone is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def revolve(self, angle:AngleOrItsFloatOrStringValue, aboutEntityOrLandmark:EntityOrItsNameOrLandmark, axis:AxisOrItsIndexOrItsName="z") -> 'PartInterface':
        '''
        Revolve a Sketch around another Entity or Landmark
        '''
        
        print("revolve is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def extrude(self, length:DimensionOrItsFloatOrStringValue) -> 'PartInterface':
        '''
        Extrude a curve by a specified length. Returns a Part type.
        '''
        
        print("extrude is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def sweep(self, profileNameOrInstance:SketchOrItsName, fillCap:bool=True) -> 'PartInterface':
        '''
        Extrude this Sketch along the path of another Sketch
        '''
        
        print("sweep is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def offset(self, radius:DimensionOrItsFloatOrStringValue):
        '''
        Uniformly add a wall around a Sketch.
        '''
        
        print("offset is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def profile(self, profileCurveName:str):
        '''
        Bend this curve along the path of another
        '''
        
        print("profile is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def createText(self, text:str, fontSize:DimensionOrItsFloatOrStringValue=1.0, bold:bool=False, italic:bool=False, underlined:bool=False, characterSpacing:'int'=1, wordSpacing:'int'=1, lineSpacing:'int'=1, fontFilePath:Optional[str]=None):
        '''
        Adds text to a sketch.
        '''
        
        print("createText is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def createFromVertices(self, coordinates:list[PointOrListOfFloatOrItsStringValue], interpolation:'int'=64):
        '''
        Create a curve from 2D/3D points.
        '''
        
        print("createFromVertices is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def createPoint(self, coordinate:PointOrListOfFloatOrItsStringValue):
        '''
        Create a point
        '''
        
        print("createPoint is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def createLine(self, length:DimensionOrItsFloatOrStringValue, angleX:AngleOrItsFloatOrStringValue=0.0, angleY:AngleOrItsFloatOrStringValue=0.0, symmetric:bool=False):
        '''
        Create a line
        '''
        
        print("createLine is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def createLineBetweenPoints(self, endAt:PointOrListOfFloatOrItsStringValue, startAt:Optional[PointOrListOfFloatOrItsStringValue]=None):
        '''
        Create a line between two points
        '''
        
        print("createLineBetweenPoints is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def createCircle(self, radius:DimensionOrItsFloatOrStringValue):
        '''
        Create a circle
        '''
        
        print("createCircle is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def createEllipse(self, radiusA:DimensionOrItsFloatOrStringValue, radiusB:DimensionOrItsFloatOrStringValue):
        '''
        Create an ellipse
        '''
        
        print("createEllipse is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def createArc(self, radius:DimensionOrItsFloatOrStringValue, angle:AngleOrItsFloatOrStringValue="180d"):
        '''
        Create an arc
        '''
        
        print("createArc is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def createArcBetweenThreePoints(self, pointA:'Point', pointB:'Point', centerPoint:'Point'):
        '''
        Create a 3-point arc
        '''
        
        print("createArcBetweenThreePoints is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def createSegment(self, innerRadius:DimensionOrItsFloatOrStringValue, outerRadius:DimensionOrItsFloatOrStringValue, angle:AngleOrItsFloatOrStringValue="180d"):
        '''
        Create a segment (intersection of two circles)
        '''
        
        print("createSegment is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def createRectangle(self, length:DimensionOrItsFloatOrStringValue, width:DimensionOrItsFloatOrStringValue):
        '''
        Create a rectangle
        '''
        
        print("createRectangle is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def createPolygon(self, numberOfSides:'int', length:DimensionOrItsFloatOrStringValue, width:DimensionOrItsFloatOrStringValue):
        '''
        Create an n-gon
        '''
        
        print("createPolygon is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def createTrapezoid(self, lengthUpper:DimensionOrItsFloatOrStringValue, lengthLower:DimensionOrItsFloatOrStringValue, height:DimensionOrItsFloatOrStringValue):
        '''
        Create a trapezoid
        '''
        
        print("createTrapezoid is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def createSpiral(self, numberOfTurns:'int', height:DimensionOrItsFloatOrStringValue, radius:DimensionOrItsFloatOrStringValue, isClockwise:bool=True, radiusEnd:Optional[DimensionOrItsFloatOrStringValue]=None):
        '''
        Create a trapezoid
        '''
        
        print("createSpiral is called in an abstract method. Please override this method.")
        return self
        