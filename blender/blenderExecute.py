from pathlib import Path
from mathutils import Vector
from enum import Enum
import bpy
from utilities import *

class BlenderLength(Units):
    #metric
    KILOMETERS = LengthUnit.kilometer
    METERS = LengthUnit.meter
    CENTIMETERS = LengthUnit.centimeter
    MILLIMETERS = LengthUnit.millimeter
    MICROMETERS = LengthUnit.micrometer
    #imperial
    MILES = LengthUnit.mile
    FEET = LengthUnit.foot
    INCHES = LengthUnit.inch
    THOU = LengthUnit.thousandthInch

    def getSystem(self):
        if self == self.KILOMETERS or self == self.METERS or self == self.CENTIMETERS or self == self.MILLIMETERS or self == self.MICROMETERS:
            return'METRIC'
        else:
            return'IMPERIAL'

# Use this value to scale any number operations done throughout this implementation
defaultBlenderUnit = BlenderLength.METERS

# Takes in a list of Dimension and converts them to the `defaultBlenderUnit`, which is the unit blender deals with, no matter what we set the document unit to. 
def convertDimensionsToBlenderUnit(dimensions:list):
    return [
        Dimension(
            float(
                convertToLengthUnit(
                    defaultBlenderUnit.value, dimension.value,
                    dimension.unit or defaultBlenderUnit.value
                )
            ),
            defaultBlenderUnit.value
        )
        
            if (dimension.value != None and dimension.unit != None and dimension.unit != defaultBlenderUnit.value)

            else dimension

                for dimension in dimensions 
    ]



# an enum of Blender modifiers and an instance method to add that modifier to an object in Blender.
class BlenderModifiers(Enum):
    EDGE_SPLIT = 0
    SUBSURF = 1
    BOOLEAN = 2
    MIRROR = 3 # https://docs.blender.org/api/current/bpy.types.MirrorModifier.html

    def blenderAddModifier(self, shapeName:str, keywordArguments:dict):

        blenderObject = bpy.data.objects.get(shapeName)
        
        assert \
            blenderObject != None, \
            "Object {} does not exist".format(shapeName)

        # references https://docs.blender.org/api/current/bpy.types.BooleanModifier.html?highlight=boolean#bpy.types.BooleanModifier and https://docs.blender.org/api/current/bpy.types.ObjectModifiers.html#bpy.types.ObjectModifiers and https://docs.blender.org/api/current/bpy.types.Modifier.html#bpy.types.Modifier
        modifier = blenderObject.modifiers.new(type=self.name, name=self.name)

        for key,value in keywordArguments.items():
            setattr(modifier, key, value)

class BlenderBooleanTypes(Enum):
    UNION = 0
    DIFFERENCE = 1
    INTERSECT = 2

def blenderApplyBooleanModifier(shapeName, type:BlenderBooleanTypes, withShapeName):

    blenderObject = bpy.data.objects.get(shapeName)
        
    blenderBooleanObject = bpy.data.objects.get(withShapeName)
    
    assert \
        blenderObject != None, \
        "Object {} does not exist".format(shapeName)

    assert \
        blenderBooleanObject != None, \
        "Object {} does not exist".format(withShapeName)

    BlenderModifiers.BOOLEAN.blenderAddModifier(
        shapeName, 
        {
            "operation": type.name,
            "object": blenderBooleanObject,
            # "use_self": True,
            # "use_hole_tolerant": True,
            # "solver": "EXACT",
            # "double_threshold": 1e-6
        }
    )

def blenderApplyMirrorModifier(shapeName, mirrorAcrossShapeName, axis):
    
    blenderMirrorAcrossObject = bpy.data.objects.get(mirrorAcrossShapeName)
    
    assert \
        blenderMirrorAcrossObject != None, \
        "Object {} does not exist".format(mirrorAcrossShapeName)

    properties = {
        "mirror_object": blenderMirrorAcrossObject,
        "use_axis": axis,
        "use_mirror_merge": False
    }

    BlenderModifiers.MIRROR.blenderAddModifier(shapeName, properties)

# An enum of Blender Primitives, and an instance method to add the primitive to Blender.
class BlenderPrimitives(Enum):
    cube = 0
    cone = 1
    cylinder = 2
    torus = 3
    sphere = 4
    uvsphere = 5
    circle = 6
    grid = 7
    monkey = 8

    def blenderAddPrimitive(self, dimensions, keywordArguments):
        switch = {
            "cube": lambda:bpy.ops.mesh.primitive_cube_add(size=1, scale=[dimension.value for dimension in dimensions[:3]], **keywordArguments),
            "cone": lambda:bpy.ops.mesh.primitive_cone_add(radius1=dimensions[0].value, radius2=dimensions[1].value, depth=dimensions[2].value, **keywordArguments),
            "cylinder": lambda:bpy.ops.mesh.primitive_cylinder_add(radius=dimensions[0].value, depth=dimensions[1].value, **keywordArguments),
            "torus": lambda:bpy.ops.mesh.primitive_torus_add(mode='EXT_INT', abso_minor_rad=dimensions[0].value, abso_major_rad=dimensions[1].value, **keywordArguments),
            "sphere": lambda:bpy.ops.mesh.primitive_ico_sphere_add(radius=dimensions[0].value, **keywordArguments),
            "uvsphere": lambda:bpy.ops.mesh.primitive_uv_sphere_add(radius=dimensions[0].value, **keywordArguments),
            "circle": lambda:bpy.ops.mesh.primitive_circle_add(radius=dimensions[0].value, **keywordArguments),
            "grid": lambda:bpy.ops.mesh.primitive_grid_add(size=dimensions[0].value, **keywordArguments),
            "monkey": lambda:bpy.ops.mesh.primitive_monkey_add(size=dimensions[0].value, **keywordArguments),
        }
        return switch[self.name]()

# Extracts dimensions from a string, then passes them as arguments to the BlenderPrimitives class
# TODO: if object already exists, merge objects
def blenderAddPrimitive(
    primitiveName:str,  \
    dimensions:str,  \
    keywordArguments:dict=None
    ):

    dimensions:list[Dimension] = getDimensionsFromString(dimensions) or []

    dimensions = convertDimensionsToBlenderUnit(dimensions)

    while len(dimensions) < 3:
        dimensions.append(Dimension(1))
    
    BlenderPrimitives[primitiveName].blenderAddPrimitive(dimensions, keywordArguments or {})

blenderFileImportTypes = {
    "stl": lambda filePath: bpy.ops.import_mesh.stl(filepath=filePath),
    "ply": lambda filePath: bpy.ops.import_mesh.ply(filepath=filePath),
    "svg": lambda filePath: bpy.ops.import_curve.svg(filepath=filePath),
    "png": lambda filePath: bpy.ops.image.open(filepath=filePath),
    "fbx": lambda filePath: bpy.ops.import_scene.fbx(filepath=filePath),
    "gltf": lambda filePath: bpy.ops.import_scene.gltf(filepath=filePath),
    "obj": lambda filePath: bpy.ops.import_scene.obj(filepath=filePath),
    "x3d": lambda filePath: bpy.ops.import_scene.x3d(filepath=filePath)
}

def blenderImportFile(filePath:str, fileType:str=None):
    
    path = Path(filePath)

    assert \
        path.is_file(),\
            "File {} does not exist".format(filePath)
    
    fileType = fileType or path.suffix.replace(".","")

    assert \
        fileType in blenderFileImportTypes, \
            "File type {} is not supported".format(fileType)

    assert blenderFileImportTypes[fileType](filePath) == {'FINISHED'}, \
            "Could not import {}".format(filePath)
    


def blenderUpdateObjectName(oldName, newName):

    blenderObject = bpy.data.objects.get(oldName)
    
    assert \
        blenderObject != None, \
        "Object {} does not exist".format(oldName)
    
    
    blenderObject.name = newName


def blenderUpdateObjectMeshName(parentObjectName, newName):
    
    blenderObject = bpy.data.objects.get(parentObjectName)
    
    assert \
        blenderObject != None, \
        "Object {} does not exist".format(parentObjectName)

    meshName = blenderObject.data.name

    blenderMesh = bpy.data.meshes.get(meshName)

    assert \
        blenderMesh != None, \
        "Mesh {} does not exist".format(meshName)

    blenderMesh.name = newName


# locks the scene interface
def blenderSceneLockInterface(isLocked):
    bpy.context.scene.render.use_lock_interface = isLocked

def blenderRemoveObject(existingObjectName, removeChildren = False):
    
    blenderObject = bpy.data.objects.get(existingObjectName)
    
    assert \
        blenderObject != None, \
        "Object {} does not exist".format(existingObjectName)

    if removeChildren:
        for child in blenderObject.children:
            try:
                blenderRemoveObject(child.name, True)
            except:
                pass
    
    data = blenderObject.data
    bpy.data.objects.remove(blenderObject)
    bpy.data.meshes.remove(data)

def blenderCreateCollection(name, sceneName = "Scene"):

    assert \
        name not in bpy.data.collections, \
        "Collection {} already exists".format(name)

    assert \
        sceneName in bpy.data.scenes, \
        "Scene {} does not exist".format(sceneName)

    collection = bpy.data.collections.new(name)

    bpy.data.scenes[sceneName].collection.children.link(collection)

def blenderRemoveCollection(name, removeNestedObjects):
    
    assert \
        name in bpy.data.collections, \
        "Collection {} does not exist".format({name})

    if removeNestedObjects:
        for obj in bpy.data.collections[name].objects:
            try:
                blenderRemoveObject(obj.name, True)
            except Exception as e:
                pass

    bpy.data.collections.remove(bpy.data.collections[name])

def blenderSetDefaultUnit(unitSystem, unitName, sceneName = "Scene"):

    
    blenderScene = bpy.data.scenes.get(sceneName)
    
    assert \
        blenderScene != None, \
        "Scene {} does not exist".format(sceneName)

    blenderScene.unit_settings.system = unitSystem
    blenderScene.unit_settings.length_unit = unitName

# references https://blender.stackexchange.com/a/159540/138679
def blenderApplyObjectTransformations(shapeName):

    blenderObject = bpy.data.objects.get(shapeName)
    
    assert \
        blenderObject != None, \
        "Object {} does not exist".format(shapeName)

    mb = blenderObject.matrix_basis
    if hasattr(blenderObject.data, "transform"):
        blenderObject.data.transform(mb)
    for c in blenderObject.children:
        c.matrix_local = mb @ c.matrix_local
        
    blenderObject.matrix_basis.identity()


class BlenderRotationTypes(Enum):
    EULER = "rotation_euler"
    DELTA_EULER = "delta_rotation_euler"
    QUATERNION = "rotation_quaternion"
    DELTA_QUATERNION = "delta_rotation_quaternion"

def blenderRotateObject(shapeName, 
rotationAngles:list[Angle],
rotationType:BlenderRotationTypes):

    blenderObject = bpy.data.objects.get(shapeName)
    
    assert \
        blenderObject != None, \
        "Object {} does not exist".format(shapeName)
        
    
    assert \
        len(rotationAngles) == 3, \
        "rotationAngles must be length 3"

    rotationTuple = (rotationAngles[0].value, rotationAngles[1].value, rotationAngles[2].value)

    setattr(blenderObject, rotationType.value, rotationTuple)
    
    blenderApplyObjectTransformations(shapeName)


class BlenderTranslationTypes(Enum):
    ABSOLUTE = "location"
    RELATIVE = "delta_location"

def blenderTranslationObject(shapeName, translationDimensions:list[Dimension], translationType:BlenderTranslationTypes):
    
    blenderObject = bpy.data.objects.get(shapeName)
    
    assert \
        blenderObject != None, \
        "Object {} does not exist".format(shapeName)
    
    assert \
        len(translationDimensions) == 3, \
        "translationDimensions must be length 3"

    translationTuple = (translationDimensions[0].value, translationDimensions[1].value, translationDimensions[2].value)

    setattr(blenderObject, translationType.value, translationTuple)

    blenderApplyObjectTransformations(shapeName)


class ScalingMethods(Enum):
    toSpecificLength=0
    scaleFactor=1
    lockAspectRatio=2 # scale one dimension, the others scale with it

def blenderScaleObject(
    shapeName:str,
    scalingDimensions:list[Dimension] \
):
    blenderObject = bpy.data.objects.get(shapeName)
    
    assert \
        blenderObject != None, \
        "Object {} does not exist".format(shapeName)
    
    assert \
        len(scalingDimensions) == 3, \
        "scalingDimensions must be length 3"

    # by default we'll try to scale to the specific length passed in, or a scale factor if no unit is passed. If two of the passed in lengths are None, we will do a lockAspectRatio scaling
    scalingMethod = ScalingMethods.toSpecificLength

    # this might be confusing, but if [None,1m,None] is passed in
    # we would want to scale y to 1m and adjust x and z by the same scale factor
    # this also means that two values need to be None, and only 1 should have a value
    emptyValuesCount = len( list( filter(lambda dimension: dimension.value == None, scalingDimensions) ) )

    assert \
        emptyValuesCount != 1, \
            "One of the scaling dimensions is None. At least two should be empty for lockAspectRatio calculations."

    assert \
        emptyValuesCount != 3, \
            "All of the scaling dimensions are None. There are no values to scale by."

    if emptyValuesCount == 0:
        scalingMethod = ScalingMethods.scaleFactor
    elif emptyValuesCount == 2:
        scalingMethod = ScalingMethods.lockAspectRatio

    
    [x,y,z] = scalingDimensions
    sceneDimensions = blenderObject.dimensions

    if scalingMethod == ScalingMethods.lockAspectRatio:
        nonEmptyIndex = next((index for index,dimension in enumerate(scalingDimensions) if dimension.value != None), None)

        assert \
            nonEmptyIndex != None, \
                "Could not find the value to compute lockAspectRatio scaling"

        # assert \
        #     sceneDimensions != None, \
        #         "Could not get sceneDimensions to compute lockAspectRatio value"

        lockAspectRatio = scalingDimensions[nonEmptyIndex].value
        if sceneDimensions and scalingDimensions[nonEmptyIndex].unit != None:
            lockAspectRatio = scalingDimensions[nonEmptyIndex].value/sceneDimensions[nonEmptyIndex]
        
        x.value = lockAspectRatio
        y.value = lockAspectRatio
        z.value = lockAspectRatio

    elif scalingMethod == ScalingMethods.toSpecificLength or scalingMethod == ScalingMethods.scaleFactor:

        #calculate scale factors if a unit is passed into the dimension
        if sceneDimensions:
            x.value = x.value/sceneDimensions.x if x.unit != None else x.value
            y.value = y.value/sceneDimensions.y if y.unit != None else y.value
            z.value = z.value/sceneDimensions.z if z.unit != None else z.value
    
    blenderObject.scale = (x.value,y.value,z.value)

    blenderApplyObjectTransformations(shapeName)


# TODO: if object already exists, merge objects
def blenderDuplicateObject(existingObjectName, newObjectName):

    blenderObject = bpy.data.objects.get(existingObjectName)
    
    assert \
        blenderObject != None, \
        "Object {} does not exist".format(existingObjectName)
    
    clonedObject = blenderObject.copy()
    clonedObject.name = newObjectName
    clonedObject.data = blenderObject.data.copy()
    clonedObject.data.name = newObjectName
    
    # Link clonedObject to a collection. Might want to make this optional.
    [currentCollection] = blenderObject.users_collection

    defaultCollection = None
    if currentCollection:
        defaultCollection = currentCollection.name

    blenderAssignObjectToCollection(newObjectName, defaultCollection)


def blenderRemoveObjectFromCollection(existingObjectName, collectionName):
    
    blenderObject = bpy.data.objects.get(existingObjectName)
    
    assert \
        blenderObject != None, \
        "Object {} does not exist".format(existingObjectName)

    collection = bpy.data.collections.get(collectionName)
    
    
    assert \
        collection != None, \
        "Collection {} does not exist".format(collectionName)
    
    assert \
        existingObjectName in collection.objects, \
        "Object {} does not exist in collection {}".format(existingObjectName, collectionName)
        
    collection.objects.unlink(blenderObject)

def blenderAssignObjectToCollection(existingObjectName, collectionName = "Scene Collection", sceneName = "Scene", removeFromOtherGroups = True, moveChildren = True):

    blenderObject = bpy.data.objects.get(existingObjectName)
    
    assert \
        blenderObject != None, \
        "Object {} does not exist".format(existingObjectName)
        
    currentCollections = blenderObject.users_collection

    assert \
        collectionName not in currentCollections, \
        "Object {} is already in collection {}.".format(existingObjectName, collectionName)

    
    collection = bpy.data.collections.get(collectionName)

    if collection == None and collectionName == "Scene Collection":
        scene = bpy.data.scenes.get(sceneName)

        assert \
            scene != None, \
            "Scene {} does not exist".format(sceneName)

        collection = scene.collection

    
    assert \
        collection != None, \
        "Collection {} does not exist".format(collectionName)

    if removeFromOtherGroups:
        for currentCollection in currentCollections:
            currentCollection.objects.unlink(blenderObject)
    
    
    collection.objects.link(blenderObject)

    if moveChildren:
        for child in blenderObject.children:
            blenderAssignObjectToCollection(child.name, collectionName, sceneName, True, True)


def blenderCreateArmatures(name):
    armature = bpy.data.armatures.new(name)
    object = bpy.data.objects.new(name, armature)
    


def blenderApplyDependencyGraph(existingObjectName, removeModifiers = True):
    
    blenderObject = bpy.data.objects.get(existingObjectName)
    
    assert \
        blenderObject != None, \
        "Object {} does not exist".format(existingObjectName)

    blenderObject.data = blenderObject.evaluated_get(bpy.context.evaluated_depsgraph_get()).data.copy()

    if removeModifiers:
        blenderObject.modifiers.clear()


def blenderSetObjectVisibility(existingObjectName, isVisible):
    
    blenderObject = bpy.data.objects.get(existingObjectName)
    
    assert \
        blenderObject != None, \
        "Object {} does not exist".format(existingObjectName)
    
    blenderObject.hide_set(not isVisible)

def blenderAddConstraint(shapeName, constraintType, keywordArguments):
    
    blenderObject = bpy.data.objects.get(shapeName)

    assert \
        blenderObject != None, \
            "Object {} does not exists".format(shapeName)

    # TODO

def blenderAddJoint(shape1Name, shape2Name, shape1Landmark, shape2Landmark):
    pass

def blenderTransformLandmarkOntoAnother(shape1Name, shape2Name, shape1Landmark, shape2Landmark):

    blenderObject1 = bpy.data.objects.get(shape1Name)
    [blenderObject1Landmark] = filter(lambda child: child.name == shape1Landmark, blenderObject1.children)
    blenderObject2 = bpy.data.objects.get(shape2Name)
    [blenderObject2Landmark] = filter(lambda child: child.name == shape2Landmark, blenderObject2.children)

    # transform landmark1 onto landmark2
    t1 = blenderObject2Landmark.matrix_world.inverted() @ blenderObject1Landmark.matrix_world
    # transform object onto landmark1
    t2 = blenderObject2.matrix_world.inverted() @ blenderObject2Landmark.matrix_world

    # transform the object onto landmark1, the result onto landmark2, then restore the transform of the object onto the landmark to maintain their position 
    blenderObject2.matrix_world = blenderObject2.matrix_world.copy() @ t2 @ t1 @ t2.inverted()


def blenderMakeParent(name, parentName):
    blenderObject = bpy.data.objects.get(name)
    blenderParentObject = bpy.data.objects.get(parentName)

    assert \
        blenderObject != None, \
            "Object {} does not exists".format(name)
    assert \
        blenderParentObject != None, \
            "Object {} does not exists".format(name)

    blenderObject.parent = blenderParentObject

def blenderCreateObject(name, data = None):
    blenderObject = bpy.data.objects.get(name)

    assert \
        blenderObject == None, \
            "Object {} already exists".format(name)

    return bpy.data.objects.new( name , data )

def blenderCreateLandmark(objectName, landmarkName, localPosition):
    blenderObject = bpy.data.objects.get(objectName)

    assert \
        blenderObject != None, \
            "Object {} does not exists".format(objectName)

    # Create an Empty object
    landmarkObject = blenderCreateObject(landmarkName)


    # Assign landmark Empty object to the same collection as the object it's attaching to.
    # Assumes the first collection is the main collection
    [currentCollection] = blenderObject.users_collection

    defaultCollection = None
    if currentCollection:
        defaultCollection = currentCollection.name

    blenderAssignObjectToCollection(landmarkName, defaultCollection)


    # Parent the landmark to the object
    blenderMakeParent(landmarkName, objectName)
    

    # Figure out how far we want to translate 
    boundingBox = blenderGetBoundingBox(blenderObject)

    localPosition:list[Dimension] = getDimensionsFromString(localPosition, boundingBox) or []

    localPosition = convertDimensionsToBlenderUnit(localPosition)

    while len(localPosition) < 3:
        localPosition.append(Dimension(1))

    landmarkObject.location = [dimension.value for dimension in localPosition[:3]]


# uses object.closest_point_on_mesh https://docs.blender.org/api/current/bpy.types.Object.html#bpy.types.Object.closest_point_on_mesh
def blenderGetClosestPointsToVertex(objectName, vertex):
    
    blenderObject = bpy.data.objects.get(objectName)

    assert \
        blenderObject != None, \
            "Object {} does not exists".format(objectName)

            
    assert \
        len(vertex) == 3, \
            "Vertex is not length 3. Please provide a proper vertex (x,y,z)"

    # polygonIndex references an index at blenderObject.data.polygons[polygonIndex], in other words, the face or edge data
    [isFound, closestPoint, normal, polygonIndex] = blenderObject.closest_point_on_mesh(vertex)

    assert \
        isFound, \
            "Could not find a point close to {} on {}".format(vertex, objectName)

    blenderPolygon, blenderVertices = None

    if polygonIndex and polygonIndex != -1:
        blenderPolygon = blenderObject.data.polygons[polygonIndex]
        blenderVertices = [blenderObject.data.vertices[vertexIndex] for vertexIndex in blenderObject.data.polygons[polygonIndex].vertices]

    return [closestPoint, normal, blenderPolygon, blenderVertices]


# References https://blender.stackexchange.com/a/32288/138679
def blenderGetBoundingBox(objectName):
    
    blenderObject = bpy.data.objects.get(objectName)

    assert \
        blenderObject != None, \
            "Object {} does not exists".format(objectName)

    local_coords = blenderObject.bound_box[:]
    om = blenderObject.matrix_world
    # matrix multiple world transform by all the vertices in the boundary
    coords = [(om @ Vector(p[:])).to_tuple() for p in local_coords]
    coords = coords[::-1]
    # Coords should be a 1x8 array containing 1x3 vertices, example:
    # [(1.0, 1.0, -1.0), (1.0, 1.0, 1.0), (1.0, -1.0, 1.0), (1.0, -1.0, -1.0), (-1.0, 1.0, -1.0), (-1.0, 1.0, 1.0), (-1.0, -1.0, 1.0), (-1.0, -1.0, -1.0)]
    
    # After zipping we should get
    # x (1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0, -1.0)
    # y (1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0, -1.0)
    # z (-1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0)
    zipped = zip('xyz', zip(*coords))

    boundingBox = BoundaryBox()

    for (axis, _list) in zipped:
    
        minVal = min(_list)
        maxVal = max(_list)
    
        setattr(
            boundingBox,
            axis,
            BoundaryAxis(
                minVal,
                maxVal,
                (maxVal+minVal)/2,
                maxVal - minVal
            )
        )
    
    return boundingBox
## ADDONS ##

def blenderAddonSetEnabled(addonName, isEnabled):
    preferences = bpy.ops.preferences

    command = preferences.addon_enable if isEnabled else preferences.addon_disable

    command(module=addonName)

## CURVES ##

class BlenderCurveTypes(EquittableEnum):
    POLY = CurveTypes.POLY
    NURBS = CurveTypes.NURBS
    BEZIER = CurveTypes.BEZIER
    
    # Convert a utilities CurveTypes to BlenderCurveTypes
    @staticmethod
    def fromCurveTypes(curveType:CurveTypes):

        [result] = list(filter(lambda b: b.value == curveType, [b for b in BlenderCurveTypes]))

        return result

def blenderCreateCurve(curveName, curveType:BlenderCurveTypes, coordinates, interpolation = 64):
    
    curveData = bpy.data.curves.new(curveName, type='CURVE')
    curveData.dimensions = '3D'
    curveData.resolution_u = interpolation
    
    blenderCreateSpline(curveData, curveType, coordinates)

    blenderCreateObject(curveName, curveData)
    
    blenderAssignObjectToCollection(curveName)

# references https://blender.stackexchange.com/a/6751/138679
def blenderCreateSpline(blenderCurve, curveType:BlenderCurveTypes, coordinates):
    
    spline = blenderCurve.splines.new(curveType.name)
    spline.order_u = 2

    numberOfPoints = len(coordinates)-1 # subtract 1 so the end and origin points are not connected
    
    if curveType == BlenderCurveTypes.BEZIER:

        spline.bezier_points.add(numberOfPoints) # subtract 1 so the end and origin points are not connected
        for i, coord in enumerate(coordinates):
            x,y,z = coord
            spline.bezier_points[i].co = (x, y, z)
            spline.bezier_points[i].handle_left = (x, y, z)
            spline.bezier_points[i].handle_right = (x, y, z)

    else:

        spline.points.add(numberOfPoints) # subtract 1 so the end and origin points are not connected
        for i, coord in enumerate(coordinates):
            x,y,z = coord
            spline.points[i].co = (x, y, z, 1)

def blenderAddBevelObjectToCurve(pathCurveObjectName, profileCurveObjectName, fillCap = False):
    
    pathCurveObject = bpy.data.objects.get(pathCurveObjectName)
    
    assert \
        pathCurveObject != None, \
        "Curve Object {} does not exist".format(pathCurveObjectName)
    

    profileCurveObject = bpy.data.objects.get(profileCurveObjectName)

    assert \
        profileCurveObject != None, \
        "Curve Object {} does not exist".format(profileCurveObjectName)


    pathCurveObject.bevel_mode = "OBJECT"
    pathCurveObject.bevel_object = profileCurveObject
    pathCurveObject.use_fill_caps = fillCap

def blenderCreateMeshFromCurve(newObjectName, blenderCurveObject):
    dependencyGraph = bpy.context.evaluated_depsgraph_get()
    mesh = bpy.data.meshes.new_from_object(blenderCurveObject.evaluated_get(dependencyGraph), depsgraph=dependencyGraph)
    
    blenderObject = blenderCreateObject(newObjectName, mesh)

    blenderObject.matrix_world = blenderCurveObject.matrix_world
    
    blenderAssignObjectToCollection(newObjectName)


# assumes add_curve_extra_objects is enabled
# https://github.com/blender/blender-addons/blob/master/add_curve_extra_objects/add_curve_simple.py
class BlenderCurvePrimitiveTypes(EquittableEnum):
    # These names should match the names in Blender
    Point = CurvePrimitiveTypes.Point
    LineTo = CurvePrimitiveTypes.LineTo
    Distance = CurvePrimitiveTypes.Line
    Angle = CurvePrimitiveTypes.Angle
    Circle = CurvePrimitiveTypes.Circle
    Ellipse = CurvePrimitiveTypes.Ellipse
    Sector = CurvePrimitiveTypes.Sector
    Segment = CurvePrimitiveTypes.Segment
    Rectangle = CurvePrimitiveTypes.Rectangle
    Rhomb = CurvePrimitiveTypes.Rhomb
    Trapezoid = CurvePrimitiveTypes.Trapezoid
    Polygon = CurvePrimitiveTypes.Polygon
    Polygon_ab = CurvePrimitiveTypes.Polygon_ab
    Arc = CurvePrimitiveTypes.Arc

    # Convert a utilities CurvePrimitiveTypes to BlenderCurvePrimitiveTypes
    @staticmethod
    def fromCurvePrimitiveTypes(curvePrimitiveType:CurvePrimitiveTypes):

        [result] = list(filter(lambda b: b.value == curvePrimitiveType, [b for b in BlenderCurvePrimitiveTypes]))

        return result

    def getBlenderCurvePrimitiveFunction(self):
        if self == BlenderCurvePrimitiveTypes.Point:
            return BlenderCurvePrimitives.createPoint
        elif self == BlenderCurvePrimitiveTypes.LineTo:
            return BlenderCurvePrimitives.createLineTo
        elif self == BlenderCurvePrimitiveTypes.Distance:
            return BlenderCurvePrimitives.createLine
        elif self == BlenderCurvePrimitiveTypes.Angle:
            return BlenderCurvePrimitives.createAngle
        elif self == BlenderCurvePrimitiveTypes.Circle:
            return BlenderCurvePrimitives.createCircle
        elif self == BlenderCurvePrimitiveTypes.Ellipse:
            return BlenderCurvePrimitives.createEllipse
        elif self == BlenderCurvePrimitiveTypes.Sector:
            return BlenderCurvePrimitives.createSector
        elif self == BlenderCurvePrimitiveTypes.Segment:
            return BlenderCurvePrimitives.createSegment
        elif self == BlenderCurvePrimitiveTypes.Rectangle:
            return BlenderCurvePrimitives.createRectangle
        elif self == BlenderCurvePrimitiveTypes.Rhomb:
            return BlenderCurvePrimitives.createRhomb
        elif self == BlenderCurvePrimitiveTypes.Trapezoid:
            return BlenderCurvePrimitives.createTrapezoid
        elif self == BlenderCurvePrimitiveTypes.Polygon:
            return BlenderCurvePrimitives.createPolygon
        elif self == BlenderCurvePrimitiveTypes.Polygon_ab:
            return BlenderCurvePrimitives.createPolygon_ab
        elif self == BlenderCurvePrimitiveTypes.Arc:
            return BlenderCurvePrimitives.createArc
        else:
            raise "Unknown primitive"

            
    def getDefaultCurveType(self):
        if self == BlenderCurvePrimitiveTypes.Point:
            return BlenderCurveTypes.NURBS
        elif self == BlenderCurvePrimitiveTypes.LineTo:
            return BlenderCurveTypes.NURBS
        elif self == BlenderCurvePrimitiveTypes.Distance:
            return BlenderCurveTypes.NURBS
        elif self == BlenderCurvePrimitiveTypes.Angle:
            return BlenderCurveTypes.BEZIER
        elif self == BlenderCurvePrimitiveTypes.Circle:
            return BlenderCurveTypes.BEZIER
        elif self == BlenderCurvePrimitiveTypes.Ellipse:
            return BlenderCurveTypes.BEZIER
        elif self == BlenderCurvePrimitiveTypes.Sector:
            return BlenderCurveTypes.BEZIER
        elif self == BlenderCurvePrimitiveTypes.Segment:
            return BlenderCurveTypes.BEZIER
        elif self == BlenderCurvePrimitiveTypes.Rectangle:
            return BlenderCurveTypes.NURBS
        elif self == BlenderCurvePrimitiveTypes.Rhomb:
            return BlenderCurveTypes.NURBS
        elif self == BlenderCurvePrimitiveTypes.Trapezoid:
            return BlenderCurveTypes.NURBS
        elif self == BlenderCurvePrimitiveTypes.Polygon:
            return BlenderCurveTypes.NURBS
        elif self == BlenderCurvePrimitiveTypes.Polygon_ab:
            return BlenderCurveTypes.NURBS
        elif self == BlenderCurvePrimitiveTypes.Arc:
            return BlenderCurveTypes.NURBS
        else:
            raise "Unknown primitive"


class BlenderCurvePrimitives():
    def createPoint(curveType=BlenderCurveTypes.NURBS, keywordArguments = {}):
        blenderCreateSimpleCurve(
            BlenderCurvePrimitiveTypes.Point,
            keywordArguments
        )
    def createLineTo(endLocation, keywordArguments = {}):
        blenderCreateSimpleCurve(
            BlenderCurvePrimitiveTypes.Line,
            dict(
                {
                    "Simple_endlocation": endLocation
                },
                **keywordArguments
            )
        )
    def createLine(length, keywordArguments = {}):
        blenderCreateSimpleCurve(
            BlenderCurvePrimitiveTypes.Distance,
            dict(
                {
                    "Simple_length": length,
                    "Simple_center": True
                },
                **keywordArguments
            )
        )
    def createAngle(length, angle, keywordArguments = {}):
        blenderCreateSimpleCurve(
            BlenderCurvePrimitiveTypes.Angle,
            dict(
                {
                    "Simple_length": length,
                    "Simple_angle": angle
                },
                **keywordArguments
            )
        )
    def createCircle(radius, keywordArguments = {}):
        blenderCreateSimpleCurve(
            BlenderCurvePrimitiveTypes.Circle,
            dict(
                {
                    "Simple_radius": radius,
                    "Simple_sides": 64,
                    "use_cyclic_u": True
                },
                **keywordArguments
            )
        )
    def createEllipse(radius_x, radius_y, keywordArguments = {}):
        blenderCreateSimpleCurve(
            BlenderCurvePrimitiveTypes.Ellipse,
            dict(
                {
                    "Simple_a": radius_x,
                    "Simple_b": radius_y
                },
                **keywordArguments
            )
        )
    def createArc(radius, angle, keywordArguments = {}):
        blenderCreateSimpleCurve(
            BlenderCurvePrimitiveTypes.Arc,
            dict(
                {
                    "Simple_sides": 64,
                    "Simple_radius": radius,
                    "Simple_startangle": 0,
                    "Simple_endangle": angle
                },
                **keywordArguments
            )
        )
    def createSector(radius, angle, keywordArguments = {}):
        blenderCreateSimpleCurve(
            BlenderCurvePrimitiveTypes.Sector,
            dict(
                {
                    "Simple_sides": 64,
                    "Simple_radius": radius,
                    "Simple_startangle": 0,
                    "Simple_endangle": angle
                },
                **keywordArguments
            )
        )
    def createSegment(outter_radius, inner_radius, angle, keywordArguments = {}):
        blenderCreateSimpleCurve(
            BlenderCurvePrimitiveTypes.Segment,
            dict(
                {
                    "Simple_sides": 64,
                    "Simple_a": outter_radius,
                    "Simple_b": inner_radius,
                    "Simple_startangle": 0,
                    "Simple_endangle": angle
                },
                **keywordArguments
            )
        )
        
    def createRectangle(length, width, keywordArguments = {}):
        blenderCreateSimpleCurve(
            BlenderCurvePrimitiveTypes.Rectangle,
            dict(
                {
                    "Simple_length": length,
                    "Simple_width": width,
                    "Simple_rounded": 0
                },
                **keywordArguments
            )
        )
    def createRhomb(length, width, keywordArguments = {}):
        blenderCreateSimpleCurve(
            BlenderCurvePrimitiveTypes.Rhomb,
            dict(
                {
                    "Simple_length": length,
                    "Simple_width": width,
                    "Simple_center": True
                },
                **keywordArguments
            )
        )
    def createPolygon(numberOfSides, radius, keywordArguments = {}):
        blenderCreateSimpleCurve(
            BlenderCurvePrimitiveTypes.Polygon,
            dict(
                {
                    "Simple_sides": numberOfSides,
                    "Simple_radius": radius
                },
                **keywordArguments
            )
        )
    def createPolygon_ab(numberOfSides, radius_x, radius_y, keywordArguments = {}):
        blenderCreateSimpleCurve(
            BlenderCurvePrimitiveTypes.Polygon_ab,
            dict(
                {
                    "Simple_sides": numberOfSides,
                    "Simple_a": radius_x,
                    "Simple_b": radius_y
                },
                **keywordArguments
            )
        )
    def createTrapezoid(length_upper, length_lower, height, keywordArguments = {}):
        blenderCreateSimpleCurve(
            BlenderCurvePrimitiveTypes.Trapezoid,
            dict(
                {
                    "Simple_a": length_upper,
                    "Simple_b": length_lower,
                    "Simple_h": height
                },
                **keywordArguments
            )
        )

def blenderCreateSimpleCurve(curvePrimitiveType:BlenderCurvePrimitiveTypes, keywordArguments = {}):

    curveType:BlenderCurveTypes = keywordArguments["curveType"] if "curveType" in keywordArguments and keywordArguments["curveType"] else curvePrimitiveType.getDefaultCurveType()

    keywordArguments.pop("curveType", None) #remove curveType from kwargs

    
    addonName = "add_curve_extra_objects"

    # check if the addon is enabled, enable it if it is not.
    addon = bpy.context.preferences.addons.get(addonName)
    if addon == None:
        blenderAddonSetEnabled(addonName, True)
        addon = bpy.context.preferences.addons.get(addonName)

    assert \
        addon != None, \
            "Could not enable the {} addon to create simple curves".format(addonName)
    
    assert \
        type(curvePrimitiveType) == BlenderCurvePrimitiveTypes, \
            "{} is not a known curve primitive. Options: {}".format(curvePrimitiveType, [b.name for b in BlenderCurvePrimitiveTypes])
            
    assert \
        type(curveType) == BlenderCurveTypes, \
            "{} is not a known simple curve type. Options: {}".format(curveType, [b.name for b in BlenderCurveTypes])
    
    # Default values:
    # bpy.ops.curve.simple(align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), Simple=True, Simple_Change=False, Simple_Delete="", Simple_Type='Point', Simple_endlocation=(2, 2, 2), Simple_a=2, Simple_b=1, Simple_h=1, Simple_angle=45, Simple_startangle=0, Simple_endangle=45, Simple_sides=3, Simple_radius=1, Simple_center=True, Simple_degrees_or_radians='Degrees', Simple_width=2, Simple_length=2, Simple_rounded=0, shape='2D', outputType='BEZIER', use_cyclic_u=True, endp_u=True, order_u=4, handleType='VECTOR', edit_mode=True)
    bpy.ops.curve.simple(Simple_Type=curvePrimitiveType.name, outputType=curveType.name, order_u=2, edit_mode=False, **keywordArguments)