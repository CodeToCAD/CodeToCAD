# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run capabilitiesToPyInterface.sh to generate this file.

from abc import ABCMeta, abstractmethod
from typing import Optional, Union, TypeAlias, cast

from core.utilities import Point, Dimension, Dimensions, CurveTypes, Angle, BoundaryBox, Axis, LengthUnit

FloatOrItsStringValue: TypeAlias = Union[str, float]
IntOrFloat: TypeAlias = Union[int, float]
MaterialOrItsName: TypeAlias = Union[str, 'Material']
PartOrItsName: TypeAlias = Union[str, 'Part']
EntityOrItsName: TypeAlias = Union[str, 'Entity']
LandmarkOrItsName: TypeAlias = Union[str, 'Landmark']
AxisOrItsIndexOrItsName: TypeAlias = Union[str, int, Axis]
DimensionOrItsFloatOrStringValue: TypeAlias = Union[str,float, Dimension]
AngleOrItsFloatOrStringValue: TypeAlias = Union[str,float, Angle]
EntityOrItsNameOrLandmark: TypeAlias = Union[str, 'Entity', 'Landmark']
PointOrListOfFloatOrItsStringValue: TypeAlias = Union[str, list[FloatOrItsStringValue], Point]
LengthUnitOrItsName: TypeAlias = Union[str,LengthUnit]

class Entity(metaclass=ABCMeta): 
    
    # Capabilities shared between Parts, Sketches and Landmarks.

    @abstractmethod
    def isExists(self
    ) -> bool:
        print("isExists is called in the interface. Please override this method.") 
        raise NotImplementedError

    @abstractmethod
    def rename(self, newName:str, renamelinkedEntitiesAndLandmarks:bool=True
    ):
        print("rename is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def delete(self, removeChildren:bool
    ):
        print("delete is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def setVisible(self, isVisible:bool
    ):
        print("setVisible is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def apply(self
    ):
        print("apply is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def getNativeInstance(self
    ):
        print("getNativeInstance is called in the interface. Please override this method.") 
        raise NotImplementedError

    @abstractmethod
    def getLocationWorld(self
    ) -> 'Dimensions':
        print("getLocationWorld is called in the interface. Please override this method.") 
        raise NotImplementedError

    @abstractmethod
    def getLocationLocal(self
    ) -> 'Dimensions':
        print("getLocationLocal is called in the interface. Please override this method.") 
        raise NotImplementedError

    @abstractmethod
    def select(self, landmarkName:Optional[LandmarkOrItsName]=None, selectionType:str="vertex"
    ):
        print("select is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def export(self, filePath:str, overwrite:bool=True, scale:float=1.0
    ):
        print("export is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def clone(self, newName:str, copyLandmarks:bool=True
    ):
        print("clone is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def mirror(self, mirrorAcrossEntity:EntityOrItsName, axis:AxisOrItsIndexOrItsName, resultingMirroredEntityName:str
    ):
        print("mirror is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def linearPattern(self, instanceCount:'int', directionAxis:AxisOrItsIndexOrItsName, offset:DimensionOrItsFloatOrStringValue
    ):
        print("linearPattern is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def circularPattern(self, instanceCount:'int', separationAngle:AngleOrItsFloatOrStringValue, normalDirectionAxis:AxisOrItsIndexOrItsName, centerEntityOrLandmark:EntityOrItsNameOrLandmark
    ):
        print("circularPattern is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def scaleX(self, scale:DimensionOrItsFloatOrStringValue
    ):
        print("scaleX is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def scaleY(self, scale:DimensionOrItsFloatOrStringValue
    ):
        print("scaleY is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def scaleZ(self, scale:DimensionOrItsFloatOrStringValue
    ):
        print("scaleZ is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def scaleKeepAspectRatio(self, scale:DimensionOrItsFloatOrStringValue, axis:AxisOrItsIndexOrItsName
    ):
        print("scaleKeepAspectRatio is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def rotateX(self, rotation:AngleOrItsFloatOrStringValue
    ):
        print("rotateX is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def rotateY(self, rotation:AngleOrItsFloatOrStringValue
    ):
        print("rotateY is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def rotateZ(self, rotation:AngleOrItsFloatOrStringValue
    ):
        print("rotateZ is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def twist(self, angle:AngleOrItsFloatOrStringValue, screwPitch:DimensionOrItsFloatOrStringValue, interations:'int'=1, axis:AxisOrItsIndexOrItsName="z"
    ):
        print("twist is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def remesh(self, strategy:str, amount:float
    ):
        print("remesh is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def createLandmark(self, landmarkName:str, x:DimensionOrItsFloatOrStringValue, y:DimensionOrItsFloatOrStringValue, z:DimensionOrItsFloatOrStringValue
    ):
        print("createLandmark is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def getBoundingBox(self
    ) -> 'BoundaryBox':
        print("getBoundingBox is called in the interface. Please override this method.") 
        raise NotImplementedError

    @abstractmethod
    def getDimensions(self
    ) -> 'Dimensions':
        print("getDimensions is called in the interface. Please override this method.") 
        raise NotImplementedError

    @abstractmethod
    def getLandmark(self, landmarkName:str
    ) -> 'Landmark':
        print("getLandmark is called in the interface. Please override this method.") 
        raise NotImplementedError

class Part(Entity,metaclass=ABCMeta): 
    
    # Create and manipulate 3D shapes.
    name:str
    description:Optional[str]=None

    def __init__(self, name:str, description:Optional[str]=None):
        self.name = name
        self.description = description

    @abstractmethod
    def createFromFile(self, filePath:str, fileType:Optional[str]=None
    ):
        print("createFromFile is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def createPrimitive(self, primitiveName:str, dimensions:str, keywordArguments:Optional[dict]=None
    ):
        print("createPrimitive is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def createCube(self, width:DimensionOrItsFloatOrStringValue, length:DimensionOrItsFloatOrStringValue, height:DimensionOrItsFloatOrStringValue, keywordArguments:Optional[dict]=None
    ):
        print("createCube is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def createCone(self, radius:DimensionOrItsFloatOrStringValue, height:DimensionOrItsFloatOrStringValue, draftRadius:DimensionOrItsFloatOrStringValue=0, keywordArguments:Optional[dict]=None
    ):
        print("createCone is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def createCylinder(self, radius:DimensionOrItsFloatOrStringValue, height:DimensionOrItsFloatOrStringValue, keywordArguments:Optional[dict]=None
    ):
        print("createCylinder is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def createTorus(self, innerRadius:DimensionOrItsFloatOrStringValue, outerRadius:DimensionOrItsFloatOrStringValue, keywordArguments:Optional[dict]=None
    ):
        print("createTorus is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def createSphere(self, radius:DimensionOrItsFloatOrStringValue, keywordArguments:Optional[dict]=None
    ):
        print("createSphere is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def createGear(self, outerRadius:DimensionOrItsFloatOrStringValue, addendum:DimensionOrItsFloatOrStringValue, innerRadius:DimensionOrItsFloatOrStringValue, dedendum:DimensionOrItsFloatOrStringValue, height:DimensionOrItsFloatOrStringValue, pressureAngle:AngleOrItsFloatOrStringValue="20d", numberOfTeeth:'int'=12, skewAngle:AngleOrItsFloatOrStringValue=0, conicalAngle:AngleOrItsFloatOrStringValue=0, crownAngle:AngleOrItsFloatOrStringValue=0, keywordArguments:Optional[dict]=None
    ):
        print("createGear is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def loft(self, Landmark1:'Landmark', Landmark2:'Landmark'
    ):
        print("loft is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def union(self, withPart:PartOrItsName, deleteAfterUnion:bool=True, isTransferLandmarks:bool=False
    ):
        print("union is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def subtract(self, withPart:PartOrItsName, deleteAfterUnion:bool=True, isTransferLandmarks:bool=False
    ):
        print("subtract is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def intersect(self, withPart:PartOrItsName, deleteAfterUnion:bool=True, isTransferLandmarks:bool=False
    ):
        print("intersect is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def hollow(self, thicknessX:DimensionOrItsFloatOrStringValue, thicknessY:DimensionOrItsFloatOrStringValue, thicknessZ:DimensionOrItsFloatOrStringValue, startAxis:AxisOrItsIndexOrItsName="z", flipAxis:bool=False
    ):
        print("hollow is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def hole(self, holeLandmark:LandmarkOrItsName, radius:DimensionOrItsFloatOrStringValue, depth:DimensionOrItsFloatOrStringValue, normalAxis:AxisOrItsIndexOrItsName="z", flip:bool=False, instanceCount:'int'=1, instanceSeparation:DimensionOrItsFloatOrStringValue=0.0, aboutEntityOrLandmark:Optional[EntityOrItsNameOrLandmark]=None, mirror:bool=False, instanceAxis:Optional[AxisOrItsIndexOrItsName]=None, initialRotationX:AngleOrItsFloatOrStringValue=0.0, initialRotationY:AngleOrItsFloatOrStringValue=0.0, initialRotationZ:AngleOrItsFloatOrStringValue=0.0, leaveHoleEntity:bool=False
    ):
        print("hole is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def assignMaterial(self, materialName:MaterialOrItsName
    ):
        print("assignMaterial is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def isCollidingWithPart(self, otherPart:PartOrItsName
    ):
        print("isCollidingWithPart is called in the interface. Please override this method.") 
        raise NotImplementedError

    @abstractmethod
    def filletAllEdges(self, radius:DimensionOrItsFloatOrStringValue, useWidth:bool=False
    ):
        print("filletAllEdges is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def filletEdges(self, radius:DimensionOrItsFloatOrStringValue, landmarksNearEdges:list[LandmarkOrItsName], useWidth:bool=False
    ):
        print("filletEdges is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def filletFaces(self, radius:DimensionOrItsFloatOrStringValue, landmarksNearFaces:list[LandmarkOrItsName], useWidth:bool=False
    ):
        print("filletFaces is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def chamferAllEdges(self, radius:DimensionOrItsFloatOrStringValue
    ):
        print("chamferAllEdges is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def chamferEdges(self, radius:DimensionOrItsFloatOrStringValue, landmarksNearEdges:list[LandmarkOrItsName]
    ):
        print("chamferEdges is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def chamferFaces(self, radius:DimensionOrItsFloatOrStringValue, landmarksNearFaces:list[LandmarkOrItsName]
    ):
        print("chamferFaces is called in the interface. Please override this method.") 
        return self

class Sketch(Entity,metaclass=ABCMeta): 
    
    # Capabilities related to adding, multiplying, and/or modifying a curve.
    name:str
    curveType:Optional['CurveTypes']=None
    description:Optional[str]=None

    def __init__(self, name:str, curveType:Optional['CurveTypes']=None, description:Optional[str]=None):
        self.name = name
        self.curveType = curveType
        self.description = description

    @abstractmethod
    def revolve(self, angle:AngleOrItsFloatOrStringValue, aboutEntityOrLandmark:EntityOrItsNameOrLandmark, axis:AxisOrItsIndexOrItsName="z"
    ):
        print("revolve is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def extrude(self, length:DimensionOrItsFloatOrStringValue, convertToMesh:bool=True
    ):
        print("extrude is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def sweep(self, profileCurveName:str, fillCap:bool=False
    ):
        print("sweep is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def createText(self, text:str, fontSize:DimensionOrItsFloatOrStringValue=1.0, bold:bool=False, italic:bool=False, underlined:bool=False, characterSpacing:'int'=1, wordSpacing:'int'=1, lineSpacing:'int'=1, fontFilePath:Optional[str]=None
    ):
        print("createText is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def createFromVertices(self, coordinates:list[PointOrListOfFloatOrItsStringValue], interpolation:'int'=64
    ):
        print("createFromVertices is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def createPoint(self, coordinate:PointOrListOfFloatOrItsStringValue
    ):
        print("createPoint is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def createLine(self, length:DimensionOrItsFloatOrStringValue, angleX:AngleOrItsFloatOrStringValue=0.0, angleY:AngleOrItsFloatOrStringValue=0.0, symmetric:bool=False
    ):
        print("createLine is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def createLineBetweenPoints(self, endAt:PointOrListOfFloatOrItsStringValue, startAt:Optional[PointOrListOfFloatOrItsStringValue]=None
    ):
        print("createLineBetweenPoints is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def createCircle(self, radius:'Dimension'
    ):
        print("createCircle is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def createEllipse(self, radiusA:'Dimension', radiusB:'Dimension'
    ):
        print("createEllipse is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def createArc(self, radius:'Dimension', angle:AngleOrItsFloatOrStringValue="180d"
    ):
        print("createArc is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def createArcBetweenThreePoints(self, pointA:'Point', pointB:'Point', centerPoint:'Point'
    ):
        print("createArcBetweenThreePoints is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def createSegment(self, innerRadius:'Dimension', outerRadius:'Dimension', angle:AngleOrItsFloatOrStringValue="180d"
    ):
        print("createSegment is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def createRectangle(self, length:'Dimension', width:'Dimension'
    ):
        print("createRectangle is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def createPolygon(self, numberOfSides:'int', length:'Dimension', width:'Dimension'
    ):
        print("createPolygon is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def createTrapezoid(self, lengthUpper:'Dimension', lengthLower:'Dimension', height:'Dimension'
    ):
        print("createTrapezoid is called in the interface. Please override this method.") 
        return self

class Landmark(Entity,metaclass=ABCMeta): 
    
    # Landmarks are named positions on an entity.
    landmarkName:str
    parentEntity:EntityOrItsName

    def __init__(self, landmarkName:str, parentEntity:EntityOrItsName):
        self.landmarkName = landmarkName
        self.parentEntity = parentEntity

    @abstractmethod
    def landmarkEntityName(self
    ) -> str:
        print("landmarkEntityName is called in the interface. Please override this method.") 
        raise NotImplementedError

class Joint(metaclass=ABCMeta): 
    
    # Joints define the relationships and constraints between entities.
    entity1:EntityOrItsNameOrLandmark
    entity2:EntityOrItsNameOrLandmark

    def __init__(self, entity1:EntityOrItsNameOrLandmark, entity2:EntityOrItsNameOrLandmark):
        self.entity1 = entity1
        self.entity2 = entity2

    @abstractmethod
    def translateLandmarkOntoAnother(self
    ):
        print("translateLandmarkOntoAnother is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def pivot(self
    ):
        print("pivot is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def gearRatio(self, ratio:float
    ):
        print("gearRatio is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def limitXLocation(self, min:Optional[PointOrListOfFloatOrItsStringValue]=None, max:Optional[PointOrListOfFloatOrItsStringValue]=None
    ):
        print("limitXLocation is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def limitYLocation(self, min:Optional[PointOrListOfFloatOrItsStringValue]=None, max:Optional[PointOrListOfFloatOrItsStringValue]=None
    ):
        print("limitYLocation is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def limitZLocation(self, min:Optional[PointOrListOfFloatOrItsStringValue]=None, max:Optional[PointOrListOfFloatOrItsStringValue]=None
    ):
        print("limitZLocation is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def limitXRotation(self, min:Optional[AngleOrItsFloatOrStringValue]=None, max:Optional[AngleOrItsFloatOrStringValue]=None
    ):
        print("limitXRotation is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def limitYRotation(self, min:Optional[AngleOrItsFloatOrStringValue]=None, max:Optional[AngleOrItsFloatOrStringValue]=None
    ):
        print("limitYRotation is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def limitZRotation(self, min:Optional[AngleOrItsFloatOrStringValue]=None, max:Optional[AngleOrItsFloatOrStringValue]=None
    ):
        print("limitZRotation is called in the interface. Please override this method.") 
        return self

class Material(metaclass=ABCMeta): 
    
    # Materials affect the appearance and simulation properties of the parts.
    name:str
    description:Optional[str]=None

    def __init__(self, name:str, description:Optional[str]=None):
        self.name = name
        self.description = description

    @abstractmethod
    def assignToPart(self, partName:PartOrItsName
    ):
        print("assignToPart is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def setColor(self, rValue:IntOrFloat, gValue:IntOrFloat, bValue:IntOrFloat, aValue:IntOrFloat=1.0
    ):
        print("setColor is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def addImageTexture(self, imageFilePath:str
    ):
        print("addImageTexture is called in the interface. Please override this method.") 
        return self

class Animation(metaclass=ABCMeta): 
    
    # Camera, lighting, rendering, animation related functionality.

    def __init__(self):
        pass

    @abstractmethod
    def default(self
    ) -> 'Animation':
        print("default is called in the interface. Please override this method.") 
        raise NotImplementedError

    @abstractmethod
    def createKeyFrameLocation(self, entity:EntityOrItsName, frameNumber:'int'
    ):
        print("createKeyFrameLocation is called in the interface. Please override this method.") 
        raise NotImplementedError

    @abstractmethod
    def createKeyFrameRotation(self, entity:EntityOrItsName, frameNumber:'int'
    ):
        print("createKeyFrameRotation is called in the interface. Please override this method.") 
        raise NotImplementedError

class Scene(metaclass=ABCMeta): 
    
    # Scene, camera, lighting, rendering, animation, simulation and GUI related functionality.
    name:Optional[str]=None
    description:Optional[str]=None

    def __init__(self, name:Optional[str]=None, description:Optional[str]=None):
        self.name = name
        self.description = description

    @abstractmethod
    def default(self
    ) -> 'Scene':
        print("default is called in the interface. Please override this method.") 
        raise NotImplementedError

    @abstractmethod
    def create(self
    ):
        print("create is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def delete(self
    ):
        print("delete is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def export(self, filePath:str, entities:list[EntityOrItsName], overwrite:bool=True, scale:float=1.0
    ):
        print("export is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def setDefaultUnit(self, unit:LengthUnitOrItsName
    ):
        print("setDefaultUnit is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def createGroup(self, name:str
    ):
        print("createGroup is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def deleteGroup(self, name:str, removeChildren:bool
    ):
        print("deleteGroup is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def removeFromGroup(self, entityName:str, groupName:str
    ):
        print("removeFromGroup is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def assignToGroup(self, entities:list[EntityOrItsName], groupName:str, removeFromOtherGroups:Optional[bool]=True
    ):
        print("assignToGroup is called in the interface. Please override this method.") 
        return self

    @abstractmethod
    def setVisible(self, entities:list[EntityOrItsName], isVisible:bool
    ):
        print("setVisible is called in the interface. Please override this method.") 
        return self

class Analytics(metaclass=ABCMeta): 
    
    # Tools for collecting data about the entities and scene.

    def __init__(self):
        pass

    @abstractmethod
    def measureDistance(self, entity1:EntityOrItsNameOrLandmark, entity2:EntityOrItsNameOrLandmark
    ) -> 'Dimensions':
        print("measureDistance is called in the interface. Please override this method.") 
        raise NotImplementedError

    @abstractmethod
    def measureAngle(self, entity1:EntityOrItsNameOrLandmark, entity2:EntityOrItsNameOrLandmark, pivot:Optional[EntityOrItsNameOrLandmark]=None
    ) -> 'list[Angle]':
        print("measureAngle is called in the interface. Please override this method.") 
        raise NotImplementedError

    @abstractmethod
    def getWorldPose(self, entity:EntityOrItsName
    ) -> 'list[float]':
        print("getWorldPose is called in the interface. Please override this method.") 
        raise NotImplementedError

    @abstractmethod
    def getBoundingBox(self, entityName:EntityOrItsName
    ) -> 'BoundaryBox':
        print("getBoundingBox is called in the interface. Please override this method.") 
        raise NotImplementedError

    @abstractmethod
    def getDimensions(self, entityName:EntityOrItsName
    ) -> 'Dimensions':
        print("getDimensions is called in the interface. Please override this method.") 
        raise NotImplementedError

