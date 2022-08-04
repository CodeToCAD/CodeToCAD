import math
import CodeToCAD.utilities as Utilities
import BlenderDefinitions
import BlenderActions

from pathlib import Path
from types import LambdaType

def debugOnReceiveBlenderDependencyGraphUpdateEvent(scene, depsgraph):
    for update in depsgraph.updates:
        print("Received Event: {} Type: {}".format(update.id.name, type(update.id)))

BlenderActions.addDependencyGraphUpdateListener(debugOnReceiveBlenderDependencyGraphUpdateEvent)

class Entity:
    def translate(self,
    dimensions:str\
    ):
        dimensionsList:list[Utilities.Dimension] = Utilities.getDimensionsFromString(dimensions) or []
        
        dimensionsList = BlenderDefinitions.BlenderLength.convertDimensionsToBlenderUnit(dimensionsList)

        while len(dimensionsList) < 3:
            dimensionsList.append(Utilities.Dimension("1"))
    
        BlenderActions.translateObject(self.name, dimensionsList, BlenderDefinitions.BlenderTranslationTypes.RELATIVE)

        return self

    def setPosition(self,
    dimensions:str\
    ):
        dimensionsList:list[Utilities.Dimension] = Utilities.getDimensionsFromString(dimensions) or []
        
        dimensionsList = BlenderDefinitions.BlenderLength.convertDimensionsToBlenderUnit(dimensionsList)

        while len(dimensionsList) < 3:
            dimensionsList.append(Utilities.Dimension("1"))

        BlenderActions.translateObject(self.name, dimensionsList, BlenderDefinitions.BlenderTranslationTypes.ABSOLUTE)

        return self
        
    def scale(self,
    dimensions:str
    ):
        dimensionsList:list[Utilities.Dimension] = Utilities.getDimensionsFromString(dimensions) or []
        
        dimensionsList = BlenderDefinitions.BlenderLength.convertDimensionsToBlenderUnit(dimensionsList)

        while len(dimensionsList) < 3:
            dimensionsList.append(Utilities.Dimension("1"))
    
        BlenderActions.scaleObject(self.name, dimensionsList)
        
        BlenderActions.applyObjectRotationAndScale(self.name)
        
        return self

    def rotate(self,
    rotation:str \
    ):
        angleList:list[Utilities.Angle] = Utilities.getAnglesFromString(rotation) or []

        while len(angleList) < 3:
            angleList.append(Utilities.Angle("1"))
    
        BlenderActions.rotateObject(self.name, angleList, BlenderDefinitions.BlenderRotationTypes.EULER)

        BlenderActions.applyObjectRotationAndScale(self.name)

        return self

    def rename(self,
    newName:str,
    renameData = True,
    renameLandmarks = True
    ):
        BlenderActions.updateObjectName(self.name, newName)

        if renameData:
            BlenderActions.updateObjectDataName(newName, newName)

        if renameLandmarks:
            BlenderActions.updateObjectLandmarkNames(newName, self.name, newName)

        return self


    def clone(self,
    partName:str \
    ):
        BlenderActions.duplicateObject(partName, self.name)

        return self
        
    def revolve(self,
    angle:str,
    axis:Utilities.Axis,
    entityNameToDetermineAxis = None
    ):
        BlenderActions.applyScrewModifier(self.name, Utilities.Angle(angle).toRadians(), axis, entityNameToDetermineAxis=entityNameToDetermineAxis)

        return self

    def thicken(self,
    thickness:int
    ):
        BlenderActions.applySolidifyModifier(self.name, Utilities.Dimension(thickness))

        return self
        
    def screw(self,
    angle:str,
    axis:Utilities.Axis,
    screwPitch:str = 0,
    iterations:int = 1
    ):
        BlenderActions.applyScrewModifier(self.name, Utilities.Angle(angle).toRadians(), axis, screwPitch=Utilities.Dimension(screwPitch), iterations=iterations)
        
        return self

    def remesh(self,
    strategy:str = None,  \
    amount:float = None \
    ):
    
        BlenderActions.applyModifier(self.name, BlenderDefinitions.BlenderModifiers.EDGE_SPLIT, {"name": "EdgeDiv", "split_angle": math.radians(30)})
        
        BlenderActions.applyModifier(self.name, BlenderDefinitions.BlenderModifiers.SUBSURF, {"name": "Subdivision", "levels": 2})

        return self

    def mirror(self,
    mirrorAcrossEntityName:str, \
    axis = (True, True, True)
    ):
    
        BlenderActions.applyMirrorModifier(self.name, mirrorAcrossEntityName, axis)
        
        return self

    def linearPattern(self,
        instanceCount,
        direction:str,
        offset:int,
    ):

        axis = Utilities.Axis.fromString(direction)

        [offset] = Utilities.getDimensionsFromString(offset)
        offset = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(offset)
        offset = offset.value
        
        BlenderActions.applyLinearPattern(self.name, instanceCount, axis, offset)

        return self

    def circularPattern(self,
        instanceCount,
        separationAngle,
        normalDirection:str,
        centerPartName,
        centerLandmarkName = None
    ):

        centerObjectName = Landmark(centerPartName, centerLandmarkName).entityName if centerLandmarkName else centerPartName

        pivotLandmark = Landmark("circularPatternPivot", self.name)

        self.landmark(pivotLandmark.landmarkName, [0,0,0])
        
        BlenderActions.applyPivotConstraint(pivotLandmark.entityName, centerObjectName)
        

        [separationAngle] = Utilities.getAnglesFromString(separationAngle)
        axis = Utilities.Axis.fromString(normalDirection)
        angles = [Utilities.Angle(0) for _ in range(3)]
        angles[axis.value] = separationAngle
        
        BlenderActions.rotateObject(pivotLandmark.entityName, angles, BlenderDefinitions.BlenderRotationTypes.EULER)
        
        BlenderActions.applyCircularPattern(self.name, instanceCount, pivotLandmark.entityName)

        return self

    def contourPattern(self
    ):
        print("contourPattern is not implemented") # implement 
        return self


    def delete(self,
        removeChildren = True
    ):
        BlenderActions.removeObject(self.name, removeChildren)
        
        return self
    
    # This is a blender specific action to apply the dependency graph modifiers onto a mesh
    def apply(self):
        
        BlenderActions.applyDependencyGraph(self.name)
        
        BlenderActions.removeMesh(self.name)
        
        BlenderActions.updateObjectDataName(self.name, self.name)

        BlenderActions.clearModifiers(self.name)

        return self
        
    def landmarkRelative(
            self,
            landmarkName,
            otherEntityName,
            otherLandmarkName,
            offset
        ):
        landmarkObjectName = Landmark(landmarkName, self.name).entityName
        
        # Create an Empty object to represent the landmark
        # Using an Empty object allows us to parent the object to this Empty.
        # Parenting inherently transforms the landmark whenever the object is translated/rotated/scaled.
        # This might not work in other CodeToCAD implementations, but it does in Blender
        Part(landmarkObjectName).createPrimitive("Empty", "0")
        
        # Assign the landmark to the parent's collection
        BlenderActions.assignObjectToCollection(landmarkObjectName, BlenderActions.getObjectCollection(self.name))

        # Parent the landmark to the object
        BlenderActions.makeParent(landmarkObjectName, self.name)

        BlenderActions.transformLandmarkRelativeToAnother(self.name, landmarkObjectName, otherEntityName, otherLandmarkName, offset)

    def landmark(self, landmarkName, localPosition):

        landmarkObjectName = Landmark(landmarkName, self.name).entityName
        
        # Create an Empty object to represent the landmark
        # Using an Empty object allows us to parent the object to this Empty.
        # Parenting inherently transforms the landmark whenever the object is translated/rotated/scaled.
        # This might not work in other CodeToCAD implementations, but it does in Blender
        Part(landmarkObjectName).createPrimitive("Empty", "0")

        # Assign the landmark to the parent's collection
        BlenderActions.assignObjectToCollection(landmarkObjectName, BlenderActions.getObjectCollection(self.name))

        # Parent the landmark to the object
        BlenderActions.makeParent(landmarkObjectName, self.name)

        BlenderActions.transformLandmarkInsideParent(self.name, landmarkObjectName, localPosition)

        return self
        

    def setVisible(self,
    isVisible:bool \
    ):
        BlenderActions.setObjectVisibility(self.name, isVisible)

        return self

    def getNativeInstance(self
    ): 
        return BlenderActions.getObject(self.name)
        
    def select(self,
    landmarkName:str,  \
    selectionType:str = "face" \
    ):
        landmarkObject = Landmark(landmarkName, self.name)
        landmarkLocation = BlenderActions.getObjectWorldLocation(landmarkObject.entityName)
        [closestPoint, normal, blenderPolygon, blenderVertices] = BlenderActions.getClosestPointsToVertex(self.name, landmarkLocation)

        if blenderVertices != None:
            for vertex in blenderVertices:
                vertex.select = True

        return self

class Part(Entity):

    name = None
    description = None

    def __init__(self,
    name:str, \
    description:str=None \
    ):
        self.name = name
        self.description = description

    def createFromFile(self,
    filePath:str,  \
    fileType:str=None \
    ):
    
        path = Path(filePath)

        fileName = path.stem
        
        BlenderActions.importFile(filePath, fileType)
        
        # Since we're using Blender's bpy.ops API, we cannot provide a name for the newly created object,
        # therefore, we'll use the object's "expected" name and rename it to what it should be
        # note: this will fail if the "expected" name is incorrect
        Part(fileName).rename(self.name)
        
        return self

    def createPrimitive(self,
    primitiveName:str,  \
    dimensions:str,  \
    keywordArguments:dict=None \
    ):
        # TODO: account for blender auto-renaming with sequential numbers
        primitiveType = getattr(BlenderDefinitions.BlenderObjectPrimitiveTypes, primitiveName.lower(), None)
        expectedNameOfObjectInBlender = primitiveType.defaultNameInBlender() if primitiveType else None

        assert expectedNameOfObjectInBlender != None, \
            f"Primitive type with name {primitiveName} is not supported."
        
        BlenderActions.addPrimitive(primitiveType, dimensions, keywordArguments)

        # Since we're using Blender's bpy.ops API, we cannot provide a name for the newly created object,
        # therefore, we'll use the object's "expected" name and rename it to what it should be
        # note: this will fail if the "expected" name is incorrect
        Part(expectedNameOfObjectInBlender).rename(self.name, primitiveType.hasData())

        return self


    def createCube(self,
    width:str,  \
    length:str,  \
    height:str,  \
    keywordArguments:dict=None \
    ):
        return self.createPrimitive("cube", "{},{},{}".format(width,length,height), keywordArguments)

    def createCone(self,
    radius:str,  \
    height:str,  \
    draftRadius:str,  \
    keywordArguments:dict=None \
    ):
        return self.createPrimitive("cone", "{},{},{}".format(radius,height,draftRadius), keywordArguments)

    def createCylinder(self,
    radius:str,  \
    height:str,  \
    keywordArguments:dict=None \
    ):
        return self.createPrimitive("cylinder", "{},{}".format(radius,height), keywordArguments)

    def createTorus(self,
    innerRadius:str,  \
    outerRadius:str,  \
    keywordArguments:dict=None \
    ):
        return self.createPrimitive("torus", "{},{}".format(innerRadius,outerRadius), keywordArguments)

    def createSphere(self,
    radius:str,  \
    keywordArguments:dict=None \
    ):
        return self.createPrimitive("uvsphere", "{}".format(radius), keywordArguments)


    def verticies(self,
    landmarkName:str \
    ):
        print("verticies is not implemented") # implement 
        return self

    def loft(self,
    part1Name:str,  \
    part2Name:str \
    ):
        print("loft is not implemented") # implement 
        return self

    

    def mask(self,
    partName:str,  \
    landmarkName:str \
    ):
        print("mask is not implemented") # implement 
        return self
    

    def union(self,
    withPartName:str \
    ):
        BlenderActions.applyBooleanModifier(
                        self.name,
                        BlenderDefinitions.BlenderBooleanTypes.UNION,
                        withPartName
                    )

        return self

    def subtract(self,
    withPartName:str \
    ):
        BlenderActions.applyBooleanModifier(
                    self.name,
                    BlenderDefinitions.BlenderBooleanTypes.DIFFERENCE,
                    withPartName
                )

        return self

    def intersect(self,
    withPartName:str \
    ):
        BlenderActions.applyBooleanModifier(
                        self.name,
                        BlenderDefinitions.BlenderBooleanTypes.INTERSECT,
                        withPartName
                    )

        return self

    def bevel(self,
    landmarkName:str,  \
    angle:float,  \
    roundedness:int \
    ):
        print("bevel is not implemented") # implement 
        return self

    def hollow(self,
    wallThickness:float \
    ):
        print("hollow is not implemented") # implement 
        return self

# alias for Part
Shape = Part

class Sketch(Entity):
    
    name = None
    curveType = None
    description = None

    def __init__(self,
    name:str, \
    curveType:Utilities.CurveTypes=None, \
    description:str=None \
    ):
        self.name = name
        self.curveType = curveType
        self.description = description


    def extrude(self,
    length:str \
    ):

        [length] = Utilities.getDimensionsFromString(length) or [Utilities.Dimension(0)]

        
        BlenderActions.extrude(self.name, length)

        return self

    def sweep(self,
        profileCurveName,
        fillCap = False
        ):
        
        BlenderActions.addBevelObjectToCurve(self.name, profileCurveName, fillCap)

        return self
        
    def profile(self,
        profileCurveName
        ):

        BlenderActions.applyCurveModifier(self.name, profileCurveName)

        return self

    def createText(self,
        text,
        size = "1m",
        bold = False,
        italic = False,
        underlined = False,
        characterSpacing = 1,
        wordSpacing = 1,
        lineSpacing = 1,
        fontFilePath = None
        ):

        size = Utilities.Dimension(size)

        BlenderActions.createText(self.name, text, size, bold, italic, underlined, characterSpacing, wordSpacing, lineSpacing, fontFilePath)

        return self

    def createFromVerticies(self,
        coordinates, \
        interpolation = 64 \
        ):

        BlenderActions.createCurve(self.name, BlenderDefinitions.BlenderCurveTypes.fromCurveTypes(self.curveType) if self.curveType != None else BlenderDefinitions.BlenderCurveTypes.BEZIER, coordinates, interpolation)

        return self


    def createPrimitiveDecorator(curvePrimitiveType:Utilities.CurvePrimitiveTypes):
        def decorator(primitiveFunction):
            def wrapper(*args, **kwargs):

                self = args[0]

                blenderCurvePrimitiveType = BlenderDefinitions.BlenderCurvePrimitiveTypes.fromCurvePrimitiveTypes(curvePrimitiveType)

                blenderPrimitiveFunction = BlenderActions.getBlenderCurvePrimitiveFunction(blenderCurvePrimitiveType)

                blenderPrimitiveFunction(
                        *args[1:],
                        dict(
                                {"curveType": BlenderDefinitions.BlenderCurveTypes.fromCurveTypes(self.curveType) if self.curveType != None else None}
                                , **kwargs
                            )
                        )

                
                # Since we're using Blender's bpy.ops API, we cannot provide a name for the newly created object,
                # therefore, we'll use the object's "expected" name and rename it to what it should be
                # note: this will fail if the "expected" name is incorrect
                Part(blenderCurvePrimitiveType.name).rename(self.name)

                return primitiveFunction(*args, **kwargs)
            return wrapper
        return decorator

    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Point)
    def createPoint(self, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.LineTo)
    def createLineTo(self, endLocation, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Line)
    def createLine(self, length, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Angle)
    def createAngle(self, length, angle, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Circle)
    def createCircle(self, radius, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Ellipse)
    def createEllipse(self, radius_x, radius_y, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Arc)
    def createArc(self, radius, angle, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Sector)
    def createSector(self, radius, angle, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Segment)
    def createSegment(self, outter_radius, inner_radius, angle, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Rectangle)        
    def createRectangle(self, length, width, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Rhomb)
    def createRhomb(self, length, width, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Polygon)
    def createPolygon(self, numberOfSides, radius, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Polygon_ab)
    def createPolygon_ab(self, numberOfSides, radius_x, radius_y, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Trapezoid)
    def createTrapezoid(self, length_upper, length_lower, height, keywordArguments = {}):
        return self

# alias for Sketch
Curve = Sketch

class Landmark: 
    # Text to 3D Modeling Automation Capabilities.

    localToEntityWithName = None
    landmarkName = None
    entityName = None

    def __init__(self,
    landmarkName:str,
    localToEntityWithName:str=None \
    ):
        self.localToEntityWithName = localToEntityWithName
        
        self.landmarkName = landmarkName
        
        if localToEntityWithName:
            self.entityName = f"{localToEntityWithName}_{landmarkName}"
        else:
            self.entityName = landmarkName


class Joint: 
    # Text to 3D Modeling Automation Capabilities.

    part1Name = None
    part2Name = None
    part1Landmark:Landmark = None
    part2Landmark:Landmark = None

    def __init__(self,
    part1Name:str, \
    part2Name:str, \
    part1LandmarkName:str = None, \
    part2LandmarkName:str = None
    ):
        self.part1Name = part1Name
        self.part2Name = part2Name
        self.part1Landmark = Landmark(part1LandmarkName, part1Name) if part1LandmarkName else None
        self.part2Landmark = Landmark(part2LandmarkName, part2Name) if part2LandmarkName else None

        
    def transformLandmarkOntoAnother(self):
        
        BlenderActions.transformLandmarkOntoAnother(self.part1Name, self.part2Name, self.part1Landmark.entityName, self.part2Landmark.entityName)

        return self

    @staticmethod
    def _getLimitLocationDimensions(dimension:str):
        dimensionsArray = None

        if dimension != None:
            dimensionsArray:list[Utilities.Dimension] = Utilities.getDimensionsFromString(dimension) or []
            
            dimensionsArray = BlenderDefinitions.BlenderLength.convertDimensionsToBlenderUnit(dimensionsArray)

            assert len(dimensionsArray) > 0,\
                f"Limit Location joint must contain at least one value"
            
            if len(dimensionsArray) == 1:
                dimensionsArray.append(Utilities.Dimension(dimensionsArray[0].value, dimensionsArray[0].unit))

        return dimensionsArray

    @staticmethod
    def _limitLocationOffsetFromLandmark(objectName, objectLandmarkName, relativeToLandmarkName, xDimensions, yDimensions, zDimensions, keywordArguments):

        BlenderActions.updateViewLayer()

        [x,y,z] = BlenderActions.getObjectWorldLocation(objectName) - BlenderActions.getObjectWorldLocation(objectLandmarkName)
        

        if xDimensions:
            for index in range(0,len(xDimensions)):
                xDimensions[index].value = xDimensions[index].value + x
        if yDimensions:
            for index in range(0,len(yDimensions)):
                yDimensions[index].value = yDimensions[index].value + y
        if zDimensions:
            for index in range(0,len(zDimensions)):
                zDimensions[index].value = zDimensions[index].value + z

        BlenderActions.applyLimitLocationConstraint(objectName, xDimensions, yDimensions, zDimensions, relativeToLandmarkName, keywordArguments)

    def limitLocation(
        self,
        x:str = None,
        y:str = None,
        z:str = None,
        keywordArguments = {}
        ):
        
        xDimensions = Joint._getLimitLocationDimensions(x)
        yDimensions = Joint._getLimitLocationDimensions(y)
        zDimensions = Joint._getLimitLocationDimensions(z)

        
        Joint._limitLocationOffsetFromLandmark(self.part2Name, self.part2Landmark.entityName, self.part1Landmark.entityName, xDimensions, yDimensions, zDimensions, keywordArguments)

        return self
        

    @staticmethod
    def _getLimitRotationAngles(angles:str):
        angleList = None

        if angles != None:
            
            angleList:list[Utilities.Angle] = Utilities.getAnglesFromString(angles) or []

            assert len(angleList) > 0,\
                f"Limit Rotation joint angle must contain at least one value"
            
            if len(angleList) == 1:

                angleList.append(Utilities.Angle(angleList[0].value, angleList[0].unit))

        return angleList

    def limitRotation(
        self,
        x:str = None,
        y:str = None,
        z:str = None,
        keywordArguments = {}
        ):

        xAngles = Joint._getLimitRotationAngles(x)
        yAngles = Joint._getLimitRotationAngles(y)
        zAngles = Joint._getLimitRotationAngles(z)
        
        BlenderActions.applyLimitRotationConstraint(self.part2Name, xAngles, yAngles, zAngles, self.part1Landmark.entityName, keywordArguments)

        return self
        
    def pivot(
        self,
        keywordArguments = {}
        ):

        BlenderActions.applyPivotConstraint(self.part2Name, self.part1Landmark.entityName, keywordArguments)

        return self

class Material: 
    # Text to 3D Modeling Automation Capabilities.


    def __init__(self
    ):
        pass


class Scene: 
    # Text to 3D Modeling Automation Capabilities.

    name = None
    description = None

    # Names a scene
    def __init__(self,
    name:str = "Scene", # Uses Blender's default Scene
    description:str=None \
    ):
        self.name = name
        self.description = description

    def create(self):
        print("create is not implemented") # implement 
        return self

    def delete(self):
        print("delete is not implemented") # implement 
        return self

    def export(self
    ):
        print("export is not implemented") # implement 
        return self

    def setDefaultUnit(self,
    unit:Utilities.LengthUnit \
    ):

        if type(unit) == str:
            unit = Utilities.LengthUnit.fromString(unit)
            
        unit = BlenderDefinitions.BlenderLength.fromLengthUnit(unit)

        BlenderActions.setDefaultUnit(unit, self.name)

        return self

    def createGroup(self,
    name:str \
    ):
        BlenderActions.createCollection(name, self.name)

        return self

    def deleteGroup(self,
    name:str,  \
    removeChildren:bool \
    ):
        BlenderActions.removeCollection(name, removeChildren)

        return self
        
    def removeFromGroup(self,
    entityName:str, \
    groupName:str \
    ):
        BlenderActions.removeObjectFromCollection(entityName, groupName)

        return self

        
    def assignToGroup(self,
    entityName:str, \
    groupName:str, \
    removeFromOtherGroups:bool = True \
    ):
        BlenderActions.assignObjectToCollection(entityName, groupName, self.name, removeFromOtherGroups)

        return self
        

    def setVisible(self,
    entityName:str, \
    isVisible:bool \
    ):
        BlenderActions.setObjectVisibility(entityName, isVisible)

        return self

class Analytics: 
    # Text to 3D Modeling Automation Capabilities.

    def execute(self, callback: LambdaType, description = ""):
        
        blenderEvents.addToBlenderOperationsQueue(
            "Running analytics execute. {}".format(description),
            callback,
            None
        )

    def measureLandmarks(self,
    landmark1Name:str,  \
    landmark2Name:str=None \
    ):
        print("measure is not implemented") # implement 
        return None

    def getWorldPose(self,
    partName:str \
    ):
        return BlenderActions.getObjectWorldPose(partName)

    def getBoundingBox(self,
    partName:str \
    ):
        return BlenderActions.getBoundingBox(partName)

    def getDimensions(self,
    partName:str \
    ):
        
        dimensions = BlenderActions.getObject(partName).dimensions
        return [
            Utilities.Dimension(
                dimension,
                BlenderDefinitions.BlenderLength.DEFAULT_BLENDER_UNIT.value
            ) 
            for dimension in dimensions
            ]
