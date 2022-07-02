# Actions wrap Blender's API to perform a single action.
# An implementation of an action should avoid performing any logic
# An implementation of an action is allowed to perform unit conversions or perform read operations for pre-checks.

import bpy
import CodeToCAD.utilities as Utilities
import BlenderDefinitions

from pathlib import Path
from mathutils import Vector
from enum import Enum

# MARK: Modifiers

def addModifier(
        entityName:str,
        modifier:BlenderDefinitions.BlenderModifiers,
        keywordArguments:dict = {}
    ):

    blenderObject = getObject(entityName)

    # references https://docs.blender.org/api/current/bpy.types.BooleanModifier.html?highlight=boolean#bpy.types.BooleanModifier and https://docs.blender.org/api/current/bpy.types.ObjectModifiers.html#bpy.types.ObjectModifiers and https://docs.blender.org/api/current/bpy.types.Modifier.html#bpy.types.Modifier
    modifier = blenderObject.modifiers.new(type=modifier.name, name=modifier.name)

    for key,value in keywordArguments.items():
        setattr(modifier, key, value)


def applySolidifyModifier(
        entityName,
        thickness:Utilities.Dimension,
        keywordArguments:dict = {}
    ):

    addModifier(
        entityName, 
        BlenderDefinitions.BlenderModifiers.SOLIDIFY,
        {
            "thickness": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(thickness).value
        }
    )
    

def applyCurveModifier(
        entityName,
        curveObjectName,
        keywordArguments:dict = {}
    ):
    
    curveObject = getObject(curveObjectName)
        
    addModifier(
        entityName, 
        BlenderDefinitions.BlenderModifiers.CURVE,
        {
            "object": curveObject
        }
    )


def applyBooleanModifier(
        meshObjectName,
        blenderBooleanType:BlenderDefinitions.BlenderBooleanTypes,
        withMeshObjectName,
        keywordArguments:dict = {}
    ):
    blenderObject = getObject(meshObjectName)
    blenderBooleanObject = getObject(withMeshObjectName)

    assert type(blenderObject.data) == BlenderDefinitions.BlenderTypes.MESH.value, \
        f"Object {meshObjectName} is not an Object. Cannot use the Boolean modifier with {type(blenderObject.data)} type."
    assert type(blenderBooleanObject.data) == BlenderDefinitions.BlenderTypes.MESH.value, \
        f"Object {withMeshObjectName} is not an Object. Cannot use the Boolean modifier with {type(blenderBooleanObject.data)} type."

    addModifier(
        meshObjectName,
        BlenderDefinitions.BlenderModifiers.BOOLEAN,
        {
            "operation": blenderBooleanType.name,
            "object": blenderBooleanObject,
            # "use_self": True,
            # "use_hole_tolerant": True,
            # "solver": "EXACT",
            # "double_threshold": 1e-6
        }
    )


def applyMirrorModifier(
        entityName,
        mirrorAcrossEntityName,
        axis,
        keywordArguments:dict = {}
    ):
    
    blenderMirrorAcrossObject = getObject(mirrorAcrossEntityName)

    addModifier(
        entityName, 
        BlenderDefinitions.BlenderModifiers.MIRROR,
        {
            "mirror_object": blenderMirrorAcrossObject,
            "use_axis": axis,
            "use_mirror_merge": False
        }
    )

    
def applyScrewModifier(
        entityName,
        angle:Utilities.Angle,
        axis:Utilities.Axis,
        screwPitch:Utilities.Dimension = Utilities.Dimension(0),
        iterations = 1,
        entityNameToDetermineAxis = None,
        keywordArguments:dict = {}
    ):
    
    # https://docs.blender.org/api/current/bpy.types.ScrewModifier.html
    properties = {
        "axis": axis.name,
        "angle": angle.value,
        "screw_offset": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(screwPitch).value,
        "steps":64,
        "render_steps":64,
        "use_merge_vertices": True,
        "iterations": iterations
    }

    if entityNameToDetermineAxis:

        blenderMirrorAcrossObject = getObject(entityNameToDetermineAxis)
        
        properties["object"] = blenderMirrorAcrossObject


    addModifier(
        entityName,
        BlenderDefinitions.BlenderModifiers.SCREW,
        properties
    )


# MARK: CRUD of Objects (aka Parts)

def blenderPrimitiveFunction(
        primitive:BlenderDefinitions.BlenderPrimitives,
        dimensions,
        keywordArguments = {}
    ):
    
    if primitive == BlenderDefinitions.BlenderPrimitives.cube:
        return bpy.ops.mesh.primitive_cube_add(size=1, scale=[dimension.value for dimension in dimensions[:3]], **keywordArguments)
        
    if primitive == BlenderDefinitions.BlenderPrimitives.cone:
        return bpy.ops.mesh.primitive_cone_add(radius1=dimensions[0].value, radius2=dimensions[1].value, depth=dimensions[2].value, **keywordArguments)
        
    if primitive == BlenderDefinitions.BlenderPrimitives.cylinder:
        return bpy.ops.mesh.primitive_cylinder_add(radius=dimensions[0].value, depth=dimensions[1].value, **keywordArguments)
        
    if primitive == BlenderDefinitions.BlenderPrimitives.torus:
        return bpy.ops.mesh.primitive_torus_add(mode='EXT_INT', abso_minor_rad=dimensions[0].value, abso_major_rad=dimensions[1].value, **keywordArguments)
        
    if primitive == BlenderDefinitions.BlenderPrimitives.sphere:
        return bpy.ops.mesh.primitive_ico_sphere_add(radius=dimensions[0].value, **keywordArguments)
        
    if primitive == BlenderDefinitions.BlenderPrimitives.uvsphere:
       return bpy.ops.mesh.primitive_uv_sphere_add(radius=dimensions[0].value, **keywordArguments)
        
    if primitive == BlenderDefinitions.BlenderPrimitives.circle:
        return bpy.ops.mesh.primitive_circle_add(radius=dimensions[0].value, **keywordArguments)
        
    if primitive == BlenderDefinitions.BlenderPrimitives.grid:
       return bpy.ops.mesh.primitive_grid_add(size=dimensions[0].value, **keywordArguments)
        
    if primitive == BlenderDefinitions.BlenderPrimitives.monkey:
        return bpy.ops.mesh.primitive_monkey_add(size=dimensions[0].value, **keywordArguments)

    raise Exception(f"Primitive with name {primitive.name} is not implemented.")


# Extracts dimensions from a string, then passes them as arguments to the BlenderPrimitives class
def addPrimitive(
        primitiveName:str,  \
        dimensions:str,  \
        keywordArguments:dict
    ):

    # Make sure an object or mesh with the same name don't already exist:
    blenderObject = bpy.data.objects.get(primitiveName)
    blenderMesh = bpy.data.meshes.get(primitiveName)

    assert blenderObject == None, f"An object with name {primitiveName} already exists."
    assert blenderMesh == None, f"A mesh with name {primitiveName} already exists."

    # Convert the dimensions:
    dimensions:list[Utilities.Dimension] = Utilities.getDimensionsFromString(dimensions) or []

    dimensions = BlenderDefinitions.BlenderLength.convertDimensionsToBlenderUnit(dimensions)

    while len(dimensions) < 3:
        dimensions.append(Utilities.Dimension(1))
    
    # Add the object:
    blenderPrimitiveFunction(
        BlenderDefinitions.BlenderPrimitives[primitiveName],
        dimensions,
        keywordArguments or {}
    )

fileImportFunctions = {
    "stl": lambda filePath: bpy.ops.import_mesh.stl(filepath=filePath),
    "ply": lambda filePath: bpy.ops.import_mesh.ply(filepath=filePath),
    "svg": lambda filePath: bpy.ops.import_curve.svg(filepath=filePath),
    "png": lambda filePath: bpy.ops.image.open(filepath=filePath),
    "fbx": lambda filePath: bpy.ops.import_scene.fbx(filepath=filePath),
    "gltf": lambda filePath: bpy.ops.import_scene.gltf(filepath=filePath),
    "obj": lambda filePath: bpy.ops.import_scene.obj(filepath=filePath),
    "x3d": lambda filePath: bpy.ops.import_scene.x3d(filepath=filePath)
}

def importFile(
        filePath:str,
        fileType:str=None
    ):
    
    path = Path(filePath)

    # Check if the file exists:
    assert \
        path.is_file(),\
            f"File {filePath} does not exist"
            
    fileName = path.stem

    # Make sure an object or mesh with the same name don't already exist:
    blenderObject = bpy.data.objects.get(fileName)
    blenderMesh = bpy.data.meshes.get(fileName)

    assert blenderObject == None, f"An object with name {fileName} already exists."
    assert blenderMesh == None, f"A mesh with name {fileName} already exists."
    
    # Check if this is a file-type we support:
    fileType = fileType or path.suffix.replace(".","")

    assert \
        fileType in fileImportFunctions, \
            f"File type {fileType} is not supported"

    # Import the file:
    isSuccess = fileImportFunctions[fileType](filePath) == {'FINISHED'}

    assert isSuccess == True, \
            f"Could not import {filePath}"


def updateObjectName(
        oldName,
        newName
    ):

    blenderObject = getObject(oldName)    
    
    blenderObject.name = newName


def updateObjectDataName(
        parentObjectName,
        newName
    ):
    
    blenderObject = getObject(parentObjectName)

    blenderObject.data.name = newName


# locks the scene interface
def sceneLockInterface(isLocked):
    bpy.context.scene.render.use_lock_interface = isLocked


def removeObject(
        existingObjectName,
        removeChildren = False
    ):
    
    blenderObject = getObject(existingObjectName)

    if removeChildren:
        for child in blenderObject.children:
            try:
                removeObject(child.name, True)
            except:
                pass
    
    data = blenderObject.data
    bpy.data.objects.remove(blenderObject)
    bpy.data.meshes.remove(data)


def createCollection(
        name,
        sceneName = "Scene"
    ):

    assert \
        name not in bpy.data.collections, \
        f"Collection {name} already exists"

    assert \
        sceneName in bpy.data.scenes, \
        f"Scene {sceneName} does not exist"

    collection = bpy.data.collections.new(name)

    bpy.data.scenes[sceneName].collection.children.link(collection)


def removeCollection(
        name,
        removeNestedObjects
    ):
    
    assert \
        name in bpy.data.collections, \
        f"Collection {name} does not exist"

    if removeNestedObjects:
        for obj in bpy.data.collections[name].objects:
            try:
                removeObject(obj.name, True)
            except Exception as e:
                pass

    bpy.data.collections.remove(bpy.data.collections[name])


def setDefaultUnit(
        blenderUnit:BlenderDefinitions.BlenderLength,
        sceneName = "Scene"
    ):
    
    blenderScene = bpy.data.scenes.get(sceneName)
    
    assert \
        blenderScene != None, \
        f"Scene {sceneName} does not exist"

    blenderScene.unit_settings.system = blenderUnit.getSystem()
    blenderScene.unit_settings.length_unit = blenderUnit.name


# references https://blender.stackexchange.com/a/159540/138679
def applyObjectTransformations(objectName):

    blenderObject = getObject(objectName)
    
    final_pose = blenderObject.matrix_basis
    # final_pose = blenderObject.matrix_world

    blenderObject.data.transform(final_pose)
    
    for child in blenderObject.children:
        child.matrix_local = final_pose @ child.matrix_local
    
    # Reset the object's transformations (resets everything in side menu to 0's)
    blenderObject.matrix_basis.identity()


def rotateObject(
        objectName, 
        rotationAngles:list[Utilities.Angle],
        rotationType:BlenderDefinitions.BlenderRotationTypes
    ):

    blenderObject = getObject(objectName)
    
    assert \
        len(rotationAngles) == 3, \
        "rotationAngles must be length 3"

    rotationTuple = (rotationAngles[0].toRadians().value, rotationAngles[1].toRadians().value, rotationAngles[2].toRadians().value)

    setattr(blenderObject, rotationType.value, rotationTuple)
    
    applyObjectTransformations(objectName)


def translateObject(
        objectName,
        translationDimensions:list[Utilities.Dimension],
        translationType:BlenderDefinitions.BlenderTranslationTypes
    ):
    
    blenderObject = getObject(objectName)
    
    assert \
        len(translationDimensions) == 3, \
        "translationDimensions must be length 3"

    translationTuple = (translationDimensions[0].value, translationDimensions[1].value, translationDimensions[2].value)

    setattr(blenderObject, translationType.value, translationTuple)

    applyObjectTransformations(objectName)


def scaleObject(
        objectName:str,
        scalingDimensions:list[Utilities.Dimension]
    ):

    blenderObject = getObject(objectName)
    
    assert \
        len(scalingDimensions) == 3, \
        "scalingDimensions must be length 3"

    # by default we'll try to scale to the specific length passed in, or a scale factor if no unit is passed. If two of the passed in lengths are None, we will do a lockAspectRatio scaling
    scalingMethod = Utilities.ScalingMethods.toSpecificLength

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
        scalingMethod = Utilities.ScalingMethods.scaleFactor
    elif emptyValuesCount == 2:
        scalingMethod = Utilities.ScalingMethods.lockAspectRatio

    
    [x,y,z] = scalingDimensions
    sceneDimensions = blenderObject.dimensions

    if scalingMethod == Utilities.ScalingMethods.lockAspectRatio:
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

    elif scalingMethod == Utilities.ScalingMethods.toSpecificLength or scalingMethod == Utilities.ScalingMethods.scaleFactor:

        #calculate scale factors if a unit is passed into the dimension
        if sceneDimensions:
            x.value = x.value/sceneDimensions.x if x.unit != None else x.value
            y.value = y.value/sceneDimensions.y if y.unit != None else y.value
            z.value = z.value/sceneDimensions.z if z.unit != None else z.value
    
    blenderObject.scale = (x.value,y.value,z.value)

    applyObjectTransformations(objectName)


def duplicateObject(
        existingObjectName,
        newObjectName
    ):
    
    clonedObject = bpy.data.objects.get(newObjectName)

    assert clonedObject == None, \
        f"Object with name {newObjectName} already exists."

    blenderObject = getObject(existingObjectName)
    
    clonedObject = blenderObject.copy()
    clonedObject.name = newObjectName
    clonedObject.data = blenderObject.data.copy()
    clonedObject.data.name = newObjectName
    
    # Link clonedObject to a collection. Might want to make this optional.
    [currentCollection] = blenderObject.users_collection

    defaultCollection = None
    if currentCollection:
        defaultCollection = currentCollection.name

    assignObjectToCollection(newObjectName, defaultCollection)


def removeObjectFromCollection(
        existingObjectName,
        collectionName
    ):
    
    blenderObject = getObject(existingObjectName)

    collection = bpy.data.collections.get(collectionName)
    
    assert \
        collection != None, \
        f"Collection {collectionName} does not exist"
    
    assert \
        existingObjectName in collection.objects, \
        f"Object {existingObjectName} does not exist in collection {collectionName}"
        
    collection.objects.unlink(blenderObject)


def assignObjectToCollection(
        existingObjectName,
        collectionName = "Scene Collection",
        sceneName = "Scene",
        removeFromOtherGroups = True,
        moveChildren = True
    ):

    blenderObject = getObject(existingObjectName)
    
    currentCollections = blenderObject.users_collection

    assert \
        collectionName not in currentCollections, \
        f"Object {existingObjectName} is already in collection {collectionName}."

    
    collection = bpy.data.collections.get(collectionName)

    if collection == None and collectionName == "Scene Collection":
        scene = bpy.data.scenes.get(sceneName)

        assert \
            scene != None, \
            f"Scene {sceneName} does not exist"

        collection = scene.collection

    
    assert \
        collection != None, \
        f"Collection {collectionName} does not exist"

    if removeFromOtherGroups:
        for currentCollection in currentCollections:
            currentCollection.objects.unlink(blenderObject)
    
    
    collection.objects.link(blenderObject)

    if moveChildren:
        for child in blenderObject.children:
            assignObjectToCollection(child.name, collectionName, sceneName, True, True)

# TODO: createArmatures
def createArmatures(name):
    armature = bpy.data.armatures.new(name)
    object = bpy.data.objects.new(name, armature)


def addDependencyGraphUpdateListener(callback):
    bpy.app.handlers.depsgraph_update_post.append(callback)


def addTimer(callback):
    bpy.app.timers.register(callback)


def applyDependencyGraph(
        existingObjectName,
        removeModifiers = True
    ):
    
    blenderObject = getObject(existingObjectName)

    blenderObject.data = blenderObject.evaluated_get(bpy.context.evaluated_depsgraph_get()).data.copy()

    if removeModifiers:
        blenderObject.modifiers.clear()


def createMeshFromCurve(
        newObjectName,
        blenderCurveObject
    ):

    dependencyGraph = bpy.context.evaluated_depsgraph_get()
    mesh = bpy.data.meshes.new_from_object(blenderCurveObject.evaluated_get(dependencyGraph), depsgraph=dependencyGraph)
    
    blenderObject = createObject(newObjectName, mesh)

    blenderObject.matrix_world = blenderCurveObject.matrix_world
    
    assignObjectToCollection(newObjectName)


def setObjectVisibility(
        existingObjectName,
        isVisible
    ):
    
    blenderObject = getObject(existingObjectName)

    # blenderObject.hide_viewport = not isVisible
    # blenderObject.hide_render = not isVisible
    blenderObject.hide_set(not isVisible)


# TODO: addConstraint
def addConstraint(
        objectName,
        constraintType,
        keywordArguments = {}
    ):
    
    blenderObject = getObject(objectName)


# TODO: addJoint
def addJoint(
        object1Name,
        object2Name,
        object1Landmark,
        object2Landmark
    ):
    pass


def transformLandmarkOntoAnother(
        object1Name,
        object2Name,
        object1Landmark,
        object2Landmark
    ):

    blenderObject1 = getObject(object1Name)
    [blenderObject1Landmark] = filter(lambda child: child.name == object1Landmark, blenderObject1.children)
    blenderObject2 = getObject(object2Name)
    [blenderObject2Landmark] = filter(lambda child: child.name == object2Landmark, blenderObject2.children)

    # transform landmark1 onto landmark2
    # t1 = blenderObject2Landmark.matrix_world.inverted() @ blenderObject1Landmark.matrix_world
    # transform object onto landmark1
    # t2 = blenderObject2.matrix_world.inverted() @ blenderObject2Landmark.matrix_world

    # transform the object onto landmark1, the result onto landmark2, then restore the transform of the object onto the landmark to maintain their position 
    # transformation = blenderObject2.matrix_world.copy() @ t2 @ t1 @ t2.inverted()
    
    # rotation = transformation.to_euler()
    
    # rotateObject(object2Name, [Angle(rotation.x),Angle(rotation.y),Angle(rotation.z)], BlenderRotationTypes.EULER)

    # Use matrix_basis if transformations are applied.
    blenderObject1Translation = blenderObject1Landmark.matrix_basis.to_translation()
    blenderObject2Translation = blenderObject2Landmark.matrix_basis.to_translation()
    # blenderObject1Translation = blenderObject1Landmark.matrix_world.to_translation()
    # blenderObject2Translation = blenderObject2Landmark.matrix_world.to_translation()
    translation = (blenderObject1Translation)-(blenderObject2Translation)
    print("blenderObject1Translation: ",blenderObject1Translation, " blenderObject2Translation: ", blenderObject2Translation, " translation: ", translation)
    
    blenderDefaultUnit = BlenderDefinitions.BlenderLength.DEFAULT_BLENDER_UNIT.value
    
    translateObject(
        object2Name,
        [
            Utilities.Dimension(translation.x, blenderDefaultUnit),
            Utilities.Dimension(translation.y, blenderDefaultUnit),
            Utilities.Dimension(translation.z, blenderDefaultUnit)
        ],
        BlenderDefinitions.BlenderTranslationTypes.ABSOLUTE
    )


def blenderMakeParent(
        name,
        parentName
    ):

    blenderObject = getObject(name)
    blenderParentObject = getObject(parentName)

    blenderObject.parent = blenderParentObject


def createObject(
        name,
        data = None
    ):

    blenderObject = bpy.data.objects.get(name)

    assert \
        blenderObject == None, \
            f"Object {name} already exists"

    return bpy.data.objects.new( name , data )


def createLandmark(
        objectName,
        landmarkName,
        localPosition
    ):
    blenderObject = getObject(objectName)

    # Create an Empty object
    landmarkObject = createObject(landmarkName)
    landmarkObject.empty_display_size = 0

    # Assign landmark Empty object to the same collection as the object it's attaching to.
    # Assumes the first collection is the main collection
    [currentCollection] = blenderObject.users_collection

    defaultCollection = None
    if currentCollection:
        defaultCollection = currentCollection.name

    assignObjectToCollection(landmarkName, defaultCollection)


    # Parent the landmark to the object
    blenderMakeParent(landmarkName, objectName)
    

    # Figure out how far we want to translate 
    boundingBox = getBoundingBox(objectName)

    localPosition:list[Utilities.Dimension] = Utilities.getDimensionsFromString(localPosition, boundingBox) or []

    localPosition = BlenderDefinitions.BlenderLength.convertDimensionsToBlenderUnit(localPosition)

    while len(localPosition) < 3:
        localPosition.append(Utilities.Dimension(1))

    landmarkObject.location = [dimension.value for dimension in localPosition[:3]]


def getObjectWorldLocation(objectName):
    
    blenderObject = getObject(objectName)

    # return blenderObject.matrix_world.translation.to_tuple()
    return blenderObject.matrix_basis.translation.to_tuple()

    
def getObjectWorldPose(objectName):
    
    blenderObject = getObject(objectName)

    # return blenderObject.matrix_world
    return blenderObject.matrix_basis


def getObject(objectName):

    blenderObject = bpy.data.objects.get(objectName)

    assert \
        blenderObject != None, \
            f"Object {objectName} does not exists"

    return blenderObject
    

def getMesh(meshName):

    blenderMesh = bpy.data.meshes.get(meshName)

    assert \
        blenderMesh != None, \
            f"Mesh {meshName} does not exists"

    return blenderMesh

# uses object.closest_point_on_mesh https://docs.blender.org/api/current/bpy.types.Object.html#bpy.types.Object.closest_point_on_mesh
def getClosestPointsToVertex(objectName, vertex):
    
    blenderObject = getObject(objectName)
    
    assert \
        len(vertex) == 3, \
            "Vertex is not length 3. Please provide a proper vertex (x,y,z)"

    # polygonIndex references an index at blenderObject.data.polygons[polygonIndex], in other words, the face or edge data
    [isFound, closestPoint, normal, polygonIndex] = blenderObject.closest_point_on_mesh(vertex)

    assert \
        isFound, \
            f"Could not find a point close to {vertex} on {objectName}"

    blenderPolygon = None
    blenderVertices = None

    if polygonIndex and polygonIndex != -1:
        blenderPolygon = blenderObject.data.polygons[polygonIndex]
        blenderVertices = [blenderObject.data.vertices[vertexIndex] for vertexIndex in blenderObject.data.polygons[polygonIndex].vertices]

    return [closestPoint, normal, blenderPolygon, blenderVertices]


# References https://blender.stackexchange.com/a/32288/138679
def getBoundingBox(objectName):
    
    blenderObject = getObject(objectName)

    local_coords = blenderObject.bound_box[:]
    
    # om = blenderObject.matrix_world
    om = blenderObject.matrix_basis
    
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

    boundingBox = Utilities.BoundaryBox()

    for (axis, _list) in zipped:
    
        minVal = min(_list)
        maxVal = max(_list)
    
        setattr(
            boundingBox,
            axis,
            Utilities.BoundaryAxis(
                minVal,
                maxVal,
                (maxVal+minVal)/2,
                maxVal - minVal
            )
        )
    
    return boundingBox
## ADDONS ##

def addonSetEnabled(addonName, isEnabled):
    preferences = bpy.ops.preferences

    command = preferences.addon_enable if isEnabled else preferences.addon_disable

    command(module=addonName)

## CURVES ##

def createText(curveName, text,
        size = Utilities.Dimension(1),
        bold = False,
        italic = False,
        underlined = False,
        characterSpacing = 1,
        wordSpacing = 1,
        lineSpacing = 1,
        fontFilePath = None):
    
    curveData = bpy.data.curves.new(type="FONT", name=curveName)
    curveData.body = text
    curveData.size = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(size).value
    curveData.space_character = characterSpacing
    curveData.space_word = wordSpacing
    curveData.space_line = lineSpacing

    if fontFilePath:
        fontData = bpy.data.fonts.load(fontFilePath.replace("\\","/"))
        curveData.font = fontData

    if bold or italic or underlined:
        for index in range(len(text)):
            curveData.body_format[index].use_underline = underlined
            curveData.body_format[index].use_bold = bold
            curveData.body_format[index].use_bold = italic

    createObject(curveName, curveData)
    
    assignObjectToCollection(curveName)


def createCurve(
        curveName,
        curveType:BlenderDefinitions.BlenderCurveTypes,
        coordinates,
        interpolation = 64
    ):
    
    curveData = bpy.data.curves.new(curveName, type='CURVE')
    curveData.dimensions = '3D'
    curveData.resolution_u = interpolation
    
    createSpline(curveData, curveType, coordinates)

    createObject(curveName, curveData)
    
    assignObjectToCollection(curveName)


# references https://blender.stackexchange.com/a/6751/138679
def createSpline(
        blenderCurve,
        curveType:BlenderDefinitions.BlenderCurveTypes,
         coordinates
    ):

    coordinates = [
            BlenderDefinitions.BlenderLength.convertDimensionsToBlenderUnit(
                Utilities.getDimensionsFromString(coordinate) or []
            ) for coordinate in coordinates
        ]
    coordinates = [[dimension.value for dimension in coordinate] for coordinate in coordinates]
    
    spline = blenderCurve.splines.new(curveType.name)
    spline.order_u = 2

    numberOfPoints = len(coordinates)-1 # subtract 1 so the end and origin points are not connected
    
    if curveType == BlenderDefinitions.BlenderCurveTypes.BEZIER:

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


def addBevelObjectToCurve(
        pathCurveObjectName,
        profileCurveObjectName,
        fillCap = False
    ):
    
    pathCurveObject = getObject(pathCurveObjectName)
    
    profileCurveObject = getObject(profileCurveObjectName)

    assert \
        type(profileCurveObject.data) == bpy.types.Curve, \
        f"Profile Object {profileCurveObjectName} is not a Curve object. Please use a Curve object."


    pathCurveObject.data.bevel_mode = "OBJECT"
    pathCurveObject.data.bevel_object = profileCurveObject
    pathCurveObject.data.use_fill_caps = fillCap


def getBlenderCurvePrimitiveFunction(curvePrimitive:BlenderDefinitions.BlenderCurvePrimitiveTypes):
    if curvePrimitive == BlenderDefinitions.BlenderCurvePrimitiveTypes.Point:
        return BlenderCurvePrimitives.createPoint
    elif curvePrimitive == BlenderDefinitions.BlenderCurvePrimitiveTypes.LineTo:
        return BlenderCurvePrimitives.createLineTo
    elif curvePrimitive == BlenderDefinitions.BlenderCurvePrimitiveTypes.Distance:
        return BlenderCurvePrimitives.createLine
    elif curvePrimitive == BlenderDefinitions.BlenderCurvePrimitiveTypes.Angle:
        return BlenderCurvePrimitives.createAngle
    elif curvePrimitive == BlenderDefinitions.BlenderCurvePrimitiveTypes.Circle:
        return BlenderCurvePrimitives.createCircle
    elif curvePrimitive == BlenderDefinitions.BlenderCurvePrimitiveTypes.Ellipse:
        return BlenderCurvePrimitives.createEllipse
    elif curvePrimitive == BlenderDefinitions.BlenderCurvePrimitiveTypes.Sector:
        return BlenderCurvePrimitives.createSector
    elif curvePrimitive == BlenderDefinitions.BlenderCurvePrimitiveTypes.Segment:
        return BlenderCurvePrimitives.createSegment
    elif curvePrimitive == BlenderDefinitions.BlenderCurvePrimitiveTypes.Rectangle:
        return BlenderCurvePrimitives.createRectangle
    elif curvePrimitive == BlenderDefinitions.BlenderCurvePrimitiveTypes.Rhomb:
        return BlenderCurvePrimitives.createRhomb
    elif curvePrimitive == BlenderDefinitions.BlenderCurvePrimitiveTypes.Trapezoid:
        return BlenderCurvePrimitives.createTrapezoid
    elif curvePrimitive == BlenderDefinitions.BlenderCurvePrimitiveTypes.Polygon:
        return BlenderCurvePrimitives.createPolygon
    elif curvePrimitive == BlenderDefinitions.BlenderCurvePrimitiveTypes.Polygon_ab:
        return BlenderCurvePrimitives.createPolygon_ab
    elif curvePrimitive == BlenderDefinitions.BlenderCurvePrimitiveTypes.Arc:
        return BlenderCurvePrimitives.createArc
    
    raise "Unknown primitive"


class BlenderCurvePrimitives():
    def createPoint(curveType=BlenderDefinitions.BlenderCurveTypes.NURBS, keywordArguments = {}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Point,
            dict(
                {
                    "use_cyclic_u": False
                },
                **keywordArguments
            )
        )
    def createLineTo(endLocation, keywordArguments = {}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Line,
            dict(
                {
                    "Simple_endlocation": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension(endLocation)).value,
                    "use_cyclic_u": False
                },
                **keywordArguments
            )
        )
    def createLine(length, keywordArguments = {}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Distance,
            dict(
                {
                    "Simple_length": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension(length)).value,
                    "Simple_center": True,
                    "use_cyclic_u": False
                },
                **keywordArguments
            )
        )
    def createAngle(length, angle, keywordArguments = {}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Angle,
            dict(
                {
                    "Simple_length": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension(length)).value,
                    "Simple_angle": Utilities.Angle(angle).toDegrees().value,
                    "use_cyclic_u": False
                },
                **keywordArguments
            )
        )
    def createCircle(radius, keywordArguments = {}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Circle,
            dict(
                {
                    "Simple_radius": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension(radius)).value,
                    "Simple_sides": 64
                },
                **keywordArguments
            )
        )
    def createEllipse(radius_x, radius_y, keywordArguments = {}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Ellipse,
            dict(
                {
                    "Simple_a": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension(radius_x)).value,
                    "Simple_b": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension(radius_y)).value
                },
                **keywordArguments
            )
        )
    def createArc(radius, angle, keywordArguments = {}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Arc,
            dict(
                {
                    "Simple_sides": 64,
                    "Simple_radius": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension(radius)).value,
                    "Simple_startangle": 0,
                    "Simple_endangle": Utilities.Angle(angle).toDegrees().value,
                    "use_cyclic_u": False
                },
                **keywordArguments
            )
        )
    def createSector(radius, angle, keywordArguments = {}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Sector,
            dict(
                {
                    "Simple_sides": 64,
                    "Simple_radius": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension(radius)).value,
                    "Simple_startangle": 0,
                    "Simple_endangle": Utilities.Angle(angle).toDegrees().value
                },
                **keywordArguments
            )
        )
    def createSegment(outter_radius, inner_radius, angle, keywordArguments = {}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Segment,
            dict(
                {
                    "Simple_sides": 64,
                    "Simple_a": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension(outter_radius)).value,
                    "Simple_b": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension(inner_radius)).value,
                    "Simple_startangle": 0,
                    "Simple_endangle": Utilities.Angle(angle).toDegrees().value
                },
                **keywordArguments
            )
        )
        
    def createRectangle(length, width, keywordArguments = {}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Rectangle,
            dict(
                {
                    "Simple_length": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension(length)).value,
                    "Simple_width": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension(width)).value,
                    "Simple_rounded": 0
                },
                **keywordArguments
            )
        )
    def createRhomb(length, width, keywordArguments = {}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Rhomb,
            dict(
                {
                    "Simple_length": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension(length)).value,
                    "Simple_width": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension(width)).value,
                    "Simple_center": True
                },
                **keywordArguments
            )
        )
    def createPolygon(numberOfSides, radius, keywordArguments = {}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Polygon,
            dict(
                {
                    "Simple_sides": numberOfSides,
                    "Simple_radius": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension(radius)).value
                },
                **keywordArguments
            )
        )
    def createPolygon_ab(numberOfSides, radius_x, radius_y, keywordArguments = {}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Polygon_ab,
            dict(
                {
                    "Simple_sides": numberOfSides,
                    "Simple_a": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension(radius_x)).value,
                    "Simple_b": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension(radius_y)).value
                },
                **keywordArguments
            )
        )
    def createTrapezoid(length_upper, length_lower, height, keywordArguments = {}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Trapezoid,
            dict(
                {
                    "Simple_a": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension(length_upper)).value,
                    "Simple_b": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension(length_lower)).value,
                    "Simple_h": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension(height)).value
                },
                **keywordArguments
            )
        )


# assumes add_curve_extra_objects is enabled
# https://github.com/blender/blender-addons/blob/master/add_curve_extra_objects/add_curve_simple.py
def createSimpleCurve(curvePrimitiveType:BlenderDefinitions.BlenderCurvePrimitiveTypes, keywordArguments = {}):

    curveType:BlenderDefinitions.BlenderCurveTypes = keywordArguments["curveType"] if "curveType" in keywordArguments and keywordArguments["curveType"] else curvePrimitiveType.getDefaultCurveType()

    keywordArguments.pop("curveType", None) #remove curveType from kwargs
    
    addonName = "add_curve_extra_objects"

    # check if the addon is enabled, enable it if it is not.
    addon = bpy.context.preferences.addons.get(addonName)
    if addon == None:
        addonSetEnabled(addonName, True)
        addon = bpy.context.preferences.addons.get(addonName)

    assert \
        addon != None, \
            f"Could not enable the {addonName} addon to create simple curves"
    
    assert \
        type(curvePrimitiveType) == BlenderDefinitions.BlenderCurvePrimitiveTypes, \
            "{} is not a known curve primitive. Options: {}" \
                .format(
                    curvePrimitiveType,
                    [b.name for b in BlenderDefinitions.BlenderCurvePrimitiveTypes]
                )
            
    assert \
        type(curveType) == BlenderDefinitions.BlenderCurveTypes, \
            "{} is not a known simple curve type. Options: {}" \
                .format(
                    curveType,
                    [b.name for b in BlenderDefinitions.BlenderCurveTypes]
                )

    # Make sure an object or curve with the same name don't already exist:
    blenderObject = bpy.data.objects.get(curvePrimitiveType.name)
    blenderCurve = bpy.data.curves.get(curvePrimitiveType.name)

    assert blenderObject == None, f"An object with name {curvePrimitiveType.name} already exists."
    assert blenderCurve == None, f"A curve with name {curvePrimitiveType.name} already exists."
    
    # Default values:
    # bpy.ops.curve.simple(align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), Simple=True, Simple_Change=False, Simple_Delete="", Simple_Type='Point', Simple_endlocation=(2, 2, 2), Simple_a=2, Simple_b=1, Simple_h=1, Simple_angle=45, Simple_startangle=0, Simple_endangle=45, Simple_sides=3, Simple_radius=1, Simple_center=True, Simple_degrees_or_radians='Degrees', Simple_width=2, Simple_length=2, Simple_rounded=0, shape='2D', outputType='BEZIER', use_cyclic_u=True, endp_u=True, order_u=4, handleType='VECTOR', edit_mode=True)
    bpy.ops.curve.simple(Simple_Type=curvePrimitiveType.name, outputType=curveType.name, order_u=2, shape='2D',  edit_mode=False, **keywordArguments)