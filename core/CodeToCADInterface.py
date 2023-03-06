# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

from abc import ABCMeta, abstractmethod
from typing import Optional, TypeAlias, Union

from core.utilities import (Angle, Axis, BoundaryBox, CurveTypes, Dimension,
                            Dimensions, LengthUnit, Point)

FloatOrItsStringValue: TypeAlias = Union[str, float]
IntOrFloat: TypeAlias = Union[int, float]
MaterialOrItsName: TypeAlias = Union[str, 'Material']
PartOrItsName: TypeAlias = Union[str, 'Part']
EntityOrItsName: TypeAlias = Union[str, 'Entity']
LandmarkOrItsName: TypeAlias = Union[str, 'Landmark']
AxisOrItsIndexOrItsName: TypeAlias = Union[str, int, Axis]
DimensionOrItsFloatOrStringValue: TypeAlias = Union[str, float, Dimension]
AngleOrItsFloatOrStringValue: TypeAlias = Union[str, float, Angle]
EntityOrItsNameOrLandmark: TypeAlias = Union[str, 'Entity', 'Landmark']
PointOrListOfFloatOrItsStringValue: TypeAlias = Union[str,
                                                      list[FloatOrItsStringValue], Point]
LengthUnitOrItsName: TypeAlias = Union[str, LengthUnit]


class Entity(metaclass=ABCMeta):
    '''Capabilities shared between Parts, Sketches and Landmarks.'''

    name: str
    description: Optional[str] = None

    @abstractmethod
    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description

    @abstractmethod
    def isExists(self
                 ) -> bool:
        '''
        Check if an entity exists
        '''

        print("isExists is called in an abstract method. Please override this method.")
        raise NotImplementedError()

    @abstractmethod
    def rename(self, newName: str, renamelinkedEntitiesAndLandmarks: bool = True
               ):
        '''
        Rename the entity, with an option to rename linked landmarks and underlying data.
        '''

        print("rename is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def delete(self, removeChildren: bool
               ):
        '''
        Delete the entity from the scene. You may need to delete an associated joint or other features.
        '''

        print("delete is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def isVisible(self
                  ) -> bool:
        '''
        Returns whether the entity is visible in the scene.
        '''

        print("isVisible is called in an abstract method. Please override this method.")
        raise NotImplementedError()

    @abstractmethod
    def setVisible(self, isVisible: bool
                   ):
        '''
        Toggles visibility of an entity in the scene.
        '''

        print("setVisible is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def apply(self
              ):
        '''
        Apply any modifications. This is application specific, but a general function is that it finalizes any changes made to an entity.
        '''

        print("apply is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def getNativeInstance(self
                          ):
        '''
        Get the native API's object instance. For example, in Blender API, this would return a bpy.object instance.
        '''

        print("getNativeInstance is called in an abstract method. Please override this method.")
        raise NotImplementedError()

    @abstractmethod
    def getLocationWorld(self
                         ) -> 'Point':
        '''
        Get the entities XYZ location relative to World Space.
        '''

        print(
            "getLocationWorld is called in an abstract method. Please override this method.")
        raise NotImplementedError()

    @abstractmethod
    def getLocationLocal(self
                         ) -> 'Point':
        '''
        Get the entities XYZ location relative to Local Space.
        '''

        print(
            "getLocationLocal is called in an abstract method. Please override this method.")
        raise NotImplementedError()

    @abstractmethod
    def select(self, landmarkName: Optional[LandmarkOrItsName] = None, selectionType: str = "vertex"
               ):
        '''
        Select the entity (in UI). If a landmark is specified, select the closest vertex or edge or face to a landmark.
        '''

        print("select is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def export(self, filePath: str, overwrite: bool = True, scale: float = 1.0
               ):
        '''
        Export Entity. Use the filePath to control the export type, e.g. '/path/to/cube.obj' or '/path/to/curve.svg'
        '''

        print("export is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def clone(self, newName: str, copyLandmarks: bool = True
              ):
        '''
        Clone an existing entity with its geometry and properties.
        '''

        print("clone is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def mirror(self, mirrorAcrossEntity: EntityOrItsName, axis: AxisOrItsIndexOrItsName, resultingMirroredEntityName: Optional[str] = None
               ):
        '''
        Mirror an existing entity with respect to a landmark. If a name is provided, the mirror becomes a separate entity.
        '''

        print("mirror is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def linearPattern(self, instanceCount: 'int', offset: DimensionOrItsFloatOrStringValue, directionAxis: AxisOrItsIndexOrItsName = "z"
                      ):
        '''
        Pattern in a uniform direction.
        '''

        print("linearPattern is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def circularPattern(self, instanceCount: 'int', separationAngle: AngleOrItsFloatOrStringValue, centerEntityOrLandmark: EntityOrItsNameOrLandmark, normalDirectionAxis: AxisOrItsIndexOrItsName = "z"
                        ):
        '''
        Pattern in a circular direction.
        '''

        print(
            "circularPattern is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def translateXYZ(self, x: DimensionOrItsFloatOrStringValue, y: DimensionOrItsFloatOrStringValue, z: DimensionOrItsFloatOrStringValue
                     ):
        '''
        Translate in the XYZ directions. Pass a number, Dimension or Dimension-String (e.g. '2cm') to scale to a specific length.
        '''

        print("translateXYZ is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def translateX(self, amount: DimensionOrItsFloatOrStringValue
                   ):
        '''
        Translate in the X direction. Pass a number or Dimension or Dimension-String (e.g. '2cm') to translate to a specific length.
        '''

        print("translateX is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def translateY(self, amount: DimensionOrItsFloatOrStringValue
                   ):
        '''
        Translate in the Y direction. Pass a number or Dimension or Dimension-String (e.g. '2cm') to translate to a specific length.
        '''

        print("translateY is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def translateZ(self, amount: DimensionOrItsFloatOrStringValue
                   ):
        '''
        Translate in the z direction. Pass a number or Dimension or Dimension-String (e.g. '2cm') to translate to a specific length.
        '''

        print("translateZ is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def scaleXYZ(self, x: DimensionOrItsFloatOrStringValue, y: DimensionOrItsFloatOrStringValue, z: DimensionOrItsFloatOrStringValue
                 ):
        '''
        Scale in the XYZ directions. Pass a number, Dimension or Dimension-String (e.g. '2cm') to scale to a specific length.
        '''

        print("scaleXYZ is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def scaleX(self, scale: DimensionOrItsFloatOrStringValue
               ):
        '''
        Scale in the X direction. Pass a number, Dimension or Dimension-String (e.g. '2cm') to scale to a specific length.
        '''

        print("scaleX is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def scaleY(self, scale: DimensionOrItsFloatOrStringValue
               ):
        '''
        Scale in the Y direction. Pass a number, Dimension or Dimension-String (e.g. '2cm') to scale to a specific length.
        '''

        print("scaleY is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def scaleZ(self, scale: DimensionOrItsFloatOrStringValue
               ):
        '''
        Scale in the Z direction. Pass a number, Dimension or Dimension-String (e.g. '2cm') to scale to a specific length.
        '''

        print("scaleZ is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def scaleXByFactor(self, scaleFactor: float
                       ):
        '''
        Scale in the X direction by a multiple.
        '''

        print(
            "scaleXByFactor is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def scaleYByFactor(self, scaleFactor: float
                       ):
        '''
        Scale in the Y direction by a multiple.
        '''

        print(
            "scaleYByFactor is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def scaleZByFactor(self, scaleFactor: float
                       ):
        '''
        Scale in the X direction by a multiple.
        '''

        print(
            "scaleZByFactor is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def scaleKeepAspectRatio(self, scale: DimensionOrItsFloatOrStringValue, axis: AxisOrItsIndexOrItsName
                             ):
        '''
        Scale in one axis and maintain the others. Pass a Dimension or Dimension-String (e.g. '2cm') to scale to a specific length.
        '''

        print("scaleKeepAspectRatio is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def rotateXYZ(self, x: AngleOrItsFloatOrStringValue, y: AngleOrItsFloatOrStringValue, z: AngleOrItsFloatOrStringValue
                  ):
        '''
        Rotate in the XYZ direction. Default units is degrees. Pass in a number, Angle or Angle-String (e.g. 'PI/4radians' or 'PI/4r' or '90d'
        '''

        print("rotateXYZ is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def rotateX(self, rotation: AngleOrItsFloatOrStringValue
                ):
        '''
        Rotate in the X direction. Default units is degrees. Pass in a number, Angle or Angle-String (e.g. 'PI/4radians' or 'PI/4r' or '90d'
        '''

        print("rotateX is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def rotateY(self, rotation: AngleOrItsFloatOrStringValue
                ):
        '''
        Rotate in the Y direction. Default units is degrees. Pass in a number, Angle or Angle-String (e.g. 'PI/4radians' or 'PI/4r' or '90d'
        '''

        print("rotateY is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def rotateZ(self, rotation: AngleOrItsFloatOrStringValue
                ):
        '''
        Rotate in the Z direction. Default units is degrees. Pass in a number, Angle or Angle-String (e.g. 'PI/4radians' or 'PI/4r' or '90d'
        '''

        print("rotateZ is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def twist(self, angle: AngleOrItsFloatOrStringValue, screwPitch: DimensionOrItsFloatOrStringValue, interations: 'int' = 1, axis: AxisOrItsIndexOrItsName = "z"
              ):
        '''
        AKA Helix, Screw. Revolve an entity
        '''

        print("twist is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def remesh(self, strategy: str, amount: float
               ):
        '''
        Remeshing should be capable of voxel or vertex based reconstruction, including decimating unnecessary vertices (if applicable).
        '''

        print("remesh is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def createLandmark(self, landmarkName: str, x: DimensionOrItsFloatOrStringValue, y: DimensionOrItsFloatOrStringValue, z: DimensionOrItsFloatOrStringValue
                       ):
        '''
        Shortcut for creating and assigning a landmark to this entity.
        '''

        print(
            "createLandmark is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def getBoundingBox(self
                       ) -> 'BoundaryBox':
        '''
        Get the Boundary Box around the entity.
        '''

        print(
            "getBoundingBox is called in an abstract method. Please override this method.")
        raise NotImplementedError()

    @abstractmethod
    def getDimensions(self
                      ) -> 'Dimensions':
        '''
        Get the length span in each coordinate axis (X,Y,Z).
        '''

        print("getDimensions is called in an abstract method. Please override this method.")
        raise NotImplementedError()

    @abstractmethod
    def getLandmark(self, landmarkName: str
                    ) -> 'Landmark':
        '''
        Get the landmark by name
        '''

        print("getLandmark is called in an abstract method. Please override this method.")
        raise NotImplementedError()


class Part(Entity, metaclass=ABCMeta):
    '''Create and manipulate 3D shapes.'''

    @abstractmethod
    def createFromFile(self, filePath: str, fileType: Optional[str] = None
                       ):
        '''
        Adds geometry to a part from a file. If the part does not exist, this will create it.
        '''

        print(
            "createFromFile is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def createPrimitive(self, primitiveName: str, dimensions: str, keywordArguments: Optional[dict] = None
                        ):
        '''
        Adds geometry to a part from a primitive named primitive shape.
        '''

        print(
            "createPrimitive is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def createCube(self, width: DimensionOrItsFloatOrStringValue, length: DimensionOrItsFloatOrStringValue, height: DimensionOrItsFloatOrStringValue, keywordArguments: Optional[dict] = None
                   ):
        '''
        Adds cuboid geometry to a part.
        '''

        print("createCube is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def createCone(self, radius: DimensionOrItsFloatOrStringValue, height: DimensionOrItsFloatOrStringValue, draftRadius: DimensionOrItsFloatOrStringValue = 0, keywordArguments: Optional[dict] = None
                   ):
        '''
        Adds cone geometry to a part.
        '''

        print("createCone is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def createCylinder(self, radius: DimensionOrItsFloatOrStringValue, height: DimensionOrItsFloatOrStringValue, keywordArguments: Optional[dict] = None
                       ):
        '''
        Adds cylinder geometry to a part.
        '''

        print(
            "createCylinder is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def createTorus(self, innerRadius: DimensionOrItsFloatOrStringValue, outerRadius: DimensionOrItsFloatOrStringValue, keywordArguments: Optional[dict] = None
                    ):
        '''
        Adds torus geometry to a part.
        '''

        print("createTorus is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def createSphere(self, radius: DimensionOrItsFloatOrStringValue, keywordArguments: Optional[dict] = None
                     ):
        '''
        Adds sphere geometry to a part.
        '''

        print("createSphere is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def createGear(self, outerRadius: DimensionOrItsFloatOrStringValue, addendum: DimensionOrItsFloatOrStringValue, innerRadius: DimensionOrItsFloatOrStringValue, dedendum: DimensionOrItsFloatOrStringValue, height: DimensionOrItsFloatOrStringValue, pressureAngle: AngleOrItsFloatOrStringValue = "20d", numberOfTeeth: 'int' = 12, skewAngle: AngleOrItsFloatOrStringValue = 0, conicalAngle: AngleOrItsFloatOrStringValue = 0, crownAngle: AngleOrItsFloatOrStringValue = 0, keywordArguments: Optional[dict] = None
                   ):
        '''
        Adds gear geometry to a part.
        '''

        print("createGear is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def loft(self, Landmark1: 'Landmark', Landmark2: 'Landmark'
             ):
        '''
        Interpolate between two existing parts.
        '''

        print("loft is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def union(self, withPart: PartOrItsName, deleteAfterUnion: bool = True, isTransferLandmarks: bool = False
              ):
        '''
        Boolean union
        '''

        print("union is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def subtract(self, withPart: PartOrItsName, deleteAfterSubtract: bool = True, isTransferLandmarks: bool = False
                 ):
        '''
        Boolean subtraction
        '''

        print("subtract is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def intersect(self, withPart: PartOrItsName, deleteAfterIntersect: bool = True, isTransferLandmarks: bool = False
                  ):
        '''
        Boolean intersection
        '''

        print("intersect is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def hollow(self, thicknessX: DimensionOrItsFloatOrStringValue, thicknessY: DimensionOrItsFloatOrStringValue, thicknessZ: DimensionOrItsFloatOrStringValue, startAxis: AxisOrItsIndexOrItsName = "z", flipAxis: bool = False
               ):
        '''
        Remove vertices, if necessary, until the part has a specified wall thickness.
        '''

        print("hollow is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def hole(self, holeLandmark: LandmarkOrItsName, radius: DimensionOrItsFloatOrStringValue, depth: DimensionOrItsFloatOrStringValue, normalAxis: AxisOrItsIndexOrItsName = "z", flip: bool = False, instanceCount: 'int' = 1, instanceSeparation: DimensionOrItsFloatOrStringValue = 0.0, aboutEntityOrLandmark: Optional[EntityOrItsNameOrLandmark] = None, mirror: bool = False, instanceAxis: Optional[AxisOrItsIndexOrItsName] = None, initialRotationX: AngleOrItsFloatOrStringValue = 0.0, initialRotationY: AngleOrItsFloatOrStringValue = 0.0, initialRotationZ: AngleOrItsFloatOrStringValue = 0.0, leaveHoleEntity: bool = False
             ):
        '''
        Create a hole.
        '''

        print("hole is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def assignMaterial(self, materialName: MaterialOrItsName
                       ):
        '''
        Assign a known material to this part.
        '''

        print(
            "assignMaterial is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def isCollidingWithPart(self, otherPart: PartOrItsName
                            ):
        '''
        Check if this part is colliding with another.
        '''

        print("isCollidingWithPart is called in an abstract method. Please override this method.")
        raise NotImplementedError()

    @abstractmethod
    def filletAllEdges(self, radius: DimensionOrItsFloatOrStringValue, useWidth: bool = False
                       ):
        '''
        Fillet all edges.
        '''

        print(
            "filletAllEdges is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def filletEdges(self, radius: DimensionOrItsFloatOrStringValue, landmarksNearEdges: list[LandmarkOrItsName], useWidth: bool = False
                    ):
        '''
        Fillet specific edges.
        '''

        print("filletEdges is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def filletFaces(self, radius: DimensionOrItsFloatOrStringValue, landmarksNearFaces: list[LandmarkOrItsName], useWidth: bool = False
                    ):
        '''
        Fillet specific faces.
        '''

        print("filletFaces is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def chamferAllEdges(self, radius: DimensionOrItsFloatOrStringValue
                        ):
        '''
        Chamfer all edges.
        '''

        print(
            "chamferAllEdges is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def chamferEdges(self, radius: DimensionOrItsFloatOrStringValue, landmarksNearEdges: list[LandmarkOrItsName]
                     ):
        '''
        Chamfer specific edges.
        '''

        print("chamferEdges is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def chamferFaces(self, radius: DimensionOrItsFloatOrStringValue, landmarksNearFaces: list[LandmarkOrItsName]
                     ):
        '''
        Chamfer specific faces.
        '''

        print("chamferFaces is called in an abstract method. Please override this method.")
        return self


class Sketch(Entity, metaclass=ABCMeta):
    '''Capabilities related to adding, multiplying, and/or modifying a curve.'''

    name: str
    curveType: Optional['CurveTypes'] = None
    description: Optional[str] = None

    @abstractmethod
    def __init__(self, name: str, curveType: Optional['CurveTypes'] = None, description: Optional[str] = None):
        super().__init__(name, description)

        self.name = name
        self.curveType = curveType
        self.description = description

    @abstractmethod
    def revolve(self, angle: AngleOrItsFloatOrStringValue, aboutEntityOrLandmark: EntityOrItsNameOrLandmark, axis: AxisOrItsIndexOrItsName = "z"
                ):
        '''
        Revolve a Sketch around another Entity or Landmark
        '''

        print("revolve is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def extrude(self, length: DimensionOrItsFloatOrStringValue, convertToMesh: bool = True
                ):
        '''
        Extrude a curve by a specified length.
        '''

        print("extrude is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def sweep(self, profileCurveName: str, fillCap: bool = False
              ):
        '''
        Extrude this  curve along the path of another
        '''

        print("sweep is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def createText(self, text: str, fontSize: DimensionOrItsFloatOrStringValue = 1.0, bold: bool = False, italic: bool = False, underlined: bool = False, characterSpacing: 'int' = 1, wordSpacing: 'int' = 1, lineSpacing: 'int' = 1, fontFilePath: Optional[str] = None
                   ):
        '''
        Adds text to a sketch.
        '''

        print("createText is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def createFromVertices(self, coordinates: list[PointOrListOfFloatOrItsStringValue], interpolation: 'int' = 64
                           ):
        '''
        Create a curve from 2D/3D points.
        '''

        print("createFromVertices is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def createPoint(self, coordinate: PointOrListOfFloatOrItsStringValue
                    ):
        '''
        Create a point
        '''

        print("createPoint is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def createLine(self, length: DimensionOrItsFloatOrStringValue, angleX: AngleOrItsFloatOrStringValue = 0.0, angleY: AngleOrItsFloatOrStringValue = 0.0, symmetric: bool = False
                   ):
        '''
        Create a line
        '''

        print("createLine is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def createLineBetweenPoints(self, endAt: PointOrListOfFloatOrItsStringValue, startAt: Optional[PointOrListOfFloatOrItsStringValue] = None
                                ):
        '''
        Create a line between two points
        '''

        print("createLineBetweenPoints is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def createCircle(self, radius: 'Dimension'
                     ):
        '''
        Create a circle
        '''

        print("createCircle is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def createEllipse(self, radiusA: 'Dimension', radiusB: 'Dimension'
                      ):
        '''
        Create an ellipse
        '''

        print("createEllipse is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def createArc(self, radius: 'Dimension', angle: AngleOrItsFloatOrStringValue = "180d"
                  ):
        '''
        Create an arc
        '''

        print("createArc is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def createArcBetweenThreePoints(self, pointA: 'Point', pointB: 'Point', centerPoint: 'Point'
                                    ):
        '''
        Create a 3-point arc
        '''

        print("createArcBetweenThreePoints is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def createSegment(self, innerRadius: 'Dimension', outerRadius: 'Dimension', angle: AngleOrItsFloatOrStringValue = "180d"
                      ):
        '''
        Create a segment (intersection of two circles)
        '''

        print("createSegment is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def createRectangle(self, length: 'Dimension', width: 'Dimension'
                        ):
        '''
        Create a rectangle
        '''

        print(
            "createRectangle is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def createPolygon(self, numberOfSides: 'int', length: 'Dimension', width: 'Dimension'
                      ):
        '''
        Create an n-gon
        '''

        print("createPolygon is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def createTrapezoid(self, lengthUpper: 'Dimension', lengthLower: 'Dimension', height: 'Dimension'
                        ):
        '''
        Create a trapezoid
        '''

        print(
            "createTrapezoid is called in an abstract method. Please override this method.")
        return self


class Landmark(Entity, metaclass=ABCMeta):
    '''Landmarks are named positions on an entity.'''

    name: str
    parentEntity: EntityOrItsName
    description: Optional[str] = None

    @abstractmethod
    def __init__(self, name: str, parentEntity: EntityOrItsName, description: Optional[str] = None):
        super().__init__(name, description)

        self.name = name
        self.parentEntity = parentEntity
        self.description = description

    @abstractmethod
    def getLandmarkEntityName(self
                              ) -> str:

        print("getLandmarkEntityName is called in an abstract method. Please override this method.")
        raise NotImplementedError()


class Joint(metaclass=ABCMeta):
    '''Joints define the relationships and constraints between entities.'''

    entity1: EntityOrItsNameOrLandmark
    entity2: EntityOrItsNameOrLandmark

    @abstractmethod
    def __init__(self, entity1: EntityOrItsNameOrLandmark, entity2: EntityOrItsNameOrLandmark):
        self.entity1 = entity1
        self.entity2 = entity2

    @abstractmethod
    def translateLandmarkOntoAnother(self
                                     ):
        '''
        Transforms one landmark onto another
        '''

        print("translateLandmarkOntoAnother is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def pivot(self
              ):
        '''
        Constraint the rotation origin of entity B to entity A's landmark.
        '''

        print("pivot is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def gearRatio(self, ratio: float
                  ):
        '''
        Constraint the rotation of entity B to be a percentage of entity A's
        '''

        print("gearRatio is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def limitLocationX(self, min: Optional[DimensionOrItsFloatOrStringValue] = None, max: Optional[DimensionOrItsFloatOrStringValue] = None
                       ):
        '''
        Constraint the translation of entity B, relative to entity A's landmark.
        '''

        print(
            "limitLocationX is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def limitLocationY(self, min: Optional[DimensionOrItsFloatOrStringValue] = None, max: Optional[DimensionOrItsFloatOrStringValue] = None
                       ):
        '''
        Constraint the translation of entity B, relative to entity A's landmark.
        '''

        print(
            "limitLocationY is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def limitLocationZ(self, min: Optional[DimensionOrItsFloatOrStringValue] = None, max: Optional[DimensionOrItsFloatOrStringValue] = None
                       ):
        '''
        Constraint the translation of entity B, relative to entity A's landmark.
        '''

        print(
            "limitLocationZ is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def limitRotationX(self, min: Optional[AngleOrItsFloatOrStringValue] = None, max: Optional[AngleOrItsFloatOrStringValue] = None
                       ):
        '''
        Constraint the rotation of entity B, relative to entity A's landmark.
        '''

        print(
            "limitRotationX is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def limitRotationY(self, min: Optional[AngleOrItsFloatOrStringValue] = None, max: Optional[AngleOrItsFloatOrStringValue] = None
                       ):
        '''
        Constraint the rotation of entity B, relative to entity A's landmark.
        '''

        print(
            "limitRotationY is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def limitRotationZ(self, min: Optional[AngleOrItsFloatOrStringValue] = None, max: Optional[AngleOrItsFloatOrStringValue] = None
                       ):
        '''
        Constraint the rotation of entity B, relative to entity A's landmark.
        '''

        print(
            "limitRotationZ is called in an abstract method. Please override this method.")
        return self


class Material(metaclass=ABCMeta):
    '''Materials affect the appearance and simulation properties of the parts.'''

    name: str
    description: Optional[str] = None

    @abstractmethod
    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description

    @abstractmethod
    def assignToPart(self, partName: PartOrItsName
                     ):

        print("assignToPart is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def setColor(self, rValue: IntOrFloat, gValue: IntOrFloat, bValue: IntOrFloat, aValue: IntOrFloat = 1.0
                 ):

        print("setColor is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def addImageTexture(self, imageFilePath: str
                        ):

        print(
            "addImageTexture is called in an abstract method. Please override this method.")
        return self


class Animation(metaclass=ABCMeta):
    '''Camera, lighting, rendering, animation related functionality.'''

    @abstractmethod
    def __init__(self):
        pass

    @staticmethod
    def default(
    ) -> 'Animation':
        raise RuntimeError()

    @abstractmethod
    def createKeyFrameLocation(self, entity: EntityOrItsName, frameNumber: 'int'
                               ):

        print("createKeyFrameLocation is called in an abstract method. Please override this method.")
        raise NotImplementedError()

    @abstractmethod
    def createKeyFrameRotation(self, entity: EntityOrItsName, frameNumber: 'int'
                               ):

        print("createKeyFrameRotation is called in an abstract method. Please override this method.")
        raise NotImplementedError()


class Scene(metaclass=ABCMeta):
    '''Scene, camera, lighting, rendering, animation, simulation and GUI related functionality.'''

    name: Optional[str] = None
    description: Optional[str] = None

    @abstractmethod
    def __init__(self, name: Optional[str] = None, description: Optional[str] = None):
        self.name = name
        self.description = description

    @staticmethod
    def default(
    ) -> 'Scene':
        raise RuntimeError()

    @abstractmethod
    def create(self
               ):
        '''
        Creates a new scene
        '''

        print("create is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def delete(self
               ):
        '''
        Deletes a scene
        '''

        print("delete is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def export(self, filePath: str, entities: list[EntityOrItsName], overwrite: bool = True, scale: float = 1.0
               ):
        '''
        Export the entire scene or specific entities.
        '''

        print("export is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def setDefaultUnit(self, unit: LengthUnitOrItsName
                       ):
        '''
        Set the document's default measurements system.
        '''

        print(
            "setDefaultUnit is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def createGroup(self, name: str
                    ):
        '''
        Create a new group
        '''

        print("createGroup is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def deleteGroup(self, name: str, removeChildren: bool
                    ):
        '''
        Delete a new group
        '''

        print("deleteGroup is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def removeFromGroup(self, entityName: str, groupName: str
                        ):
        '''
        Removes an existing entity from a group
        '''

        print(
            "removeFromGroup is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def assignToGroup(self, entities: list[EntityOrItsName], groupName: str, removeFromOtherGroups: Optional[bool] = True
                      ):
        '''
        Assigns an existing entity to a new group
        '''

        print("assignToGroup is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def setVisible(self, entities: list[EntityOrItsName], isVisible: bool
                   ):
        '''
        Change the visibiltiy of the entity.
        '''

        print("setVisible is called in an abstract method. Please override this method.")
        return self


class Analytics(metaclass=ABCMeta):
    '''Tools for collecting data about the entities and scene.'''

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def measureDistance(self, entity1: EntityOrItsNameOrLandmark, entity2: EntityOrItsNameOrLandmark
                        ) -> 'Dimensions':
        '''
        The ubiquitous ruler.
        '''

        print(
            "measureDistance is called in an abstract method. Please override this method.")
        raise NotImplementedError()

    @abstractmethod
    def measureAngle(self, entity1: EntityOrItsNameOrLandmark, entity2: EntityOrItsNameOrLandmark, pivot: Optional[EntityOrItsNameOrLandmark] = None
                     ) -> 'list[Angle]':
        '''
        The ubiquitous ruler.
        '''

        print("measureAngle is called in an abstract method. Please override this method.")
        raise NotImplementedError()

    @abstractmethod
    def getWorldPose(self, entity: EntityOrItsName
                     ) -> 'list[float]':
        '''
        Returns the world pose of an entity.
        '''

        print("getWorldPose is called in an abstract method. Please override this method.")
        raise NotImplementedError()

    @abstractmethod
    def getBoundingBox(self, entityName: EntityOrItsName
                       ) -> 'BoundaryBox':
        '''
        Returns the bounding box of an entity.
        '''

        print(
            "getBoundingBox is called in an abstract method. Please override this method.")
        raise NotImplementedError()

    @abstractmethod
    def getDimensions(self, entityName: EntityOrItsName
                      ) -> 'Dimensions':
        '''
        Returns the dimensions of an entity.
        '''

        print("getDimensions is called in an abstract method. Please override this method.")
        raise NotImplementedError()
