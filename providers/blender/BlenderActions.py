# Actions wrap Blender's API to perform a single action.
# An implementation of an action should avoid performing any logic
# An implementation of an action is allowed to perform unit conversions or perform read operations for pre-checks.

from typing import Optional
from uuid import uuid4
import bpy
from core.CodeToCADInterface import AngleOrItsFloatOrStringValue, DimensionOrItsFloatOrStringValue
import core.utilities as Utilities
import BlenderDefinitions
from pathlib import Path
import mathutils
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree

# MARK: Modifiers


def applyModifier(
    entityName: str,
    modifier: BlenderDefinitions.BlenderModifiers,
    keywordArguments: dict = {}
):

    blenderObject = getObject(entityName)

    # references https://docs.blender.org/api/current/bpy.types.BooleanModifier.html?highlight=boolean#bpy.types.BooleanModifier and https://docs.blender.org/api/current/bpy.types.ObjectModifiers.html#bpy.types.ObjectModifiers and https://docs.blender.org/api/current/bpy.types.Modifier.html#bpy.types.Modifier
    modifier = blenderObject.modifiers.new(
        type=modifier.name,
        name=modifier.name
    )

    # Apply every parameter passed in for modifier:
    for key, value in keywordArguments.items():
        setattr(modifier, key, value)


def applyBevelModifier(
    entityName,
    radius: Utilities.Dimension,
    vertexGroupName=None,
    useEdges=True,
    useWidth=False,
    chamfer=False,
    keywordArguments: Optional[dict] = None
):
    applyModifier(
        entityName,
        BlenderDefinitions.BlenderModifiers.BEVEL,
        dict({
            "affect": "EDGES" if useEdges else "VERTICES",
            "offset_type": "WIDTH" if useWidth else "OFFSET",
            "width": radius.value,
            "segments": 1 if chamfer else 24,
            "limit_method": "VGROUP" if vertexGroupName else "ANGLE",
            "vertex_group": vertexGroupName or ""
        },
            **(keywordArguments or {})
        )
    )


def applyLinearPattern(
    entityName,
    instanceCount,
    direction: Utilities.Axis,
    offset: float,
    keywordArguments: dict = {}
):

    offsetArray = [0.0, 0.0, 0.0]

    offsetArray[direction.value] = offset

    applyModifier(
        entityName,
        BlenderDefinitions.BlenderModifiers.ARRAY,
        dict(
            {
                "count": instanceCount,
                "use_relative_offset": False,
                "use_constant_offset": True,
                "constant_offset_displace": offsetArray
            },
            **keywordArguments
        )
    )


def applyCircularPattern(
    entityName,
    instanceCount,
    aroundObjectName,
    keywordArguments: dict = {}
):

    blenderObject = getObject(aroundObjectName)

    applyModifier(
        entityName,
        BlenderDefinitions.BlenderModifiers.ARRAY,
        dict(
            {
                "count": instanceCount,
                "use_relative_offset": False,
                "use_object_offset": True,
                "offset_object": blenderObject
            },
            **keywordArguments
        )
    )


def applySolidifyModifier(
    entityName,
    thickness: Utilities.Dimension,
    keywordArguments: dict = {}
):

    applyModifier(
        entityName,
        BlenderDefinitions.BlenderModifiers.SOLIDIFY,
        dict(
            {
                "thickness": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(thickness).value
            },
            **keywordArguments
        )
    )


def applyCurveModifier(
    entityName,
    curveObjectName,
    keywordArguments: dict = {}
):

    curveObject = getObject(curveObjectName)

    applyModifier(
        entityName,
        BlenderDefinitions.BlenderModifiers.CURVE,
        dict(
            {
                "object": curveObject
            },
            **keywordArguments
        )
    )


def applyBooleanModifier(
    meshObjectName,
    blenderBooleanType: BlenderDefinitions.BlenderBooleanTypes,
    withMeshObjectName,
    keywordArguments: Optional[dict] = None
):
    blenderObject = getObject(meshObjectName)
    blenderBooleanObject = getObject(withMeshObjectName)

    assert type(blenderObject.data) == BlenderDefinitions.BlenderTypes.MESH.value, \
        f"Object {meshObjectName} is not an Object. Cannot use the Boolean modifier with {type(blenderObject.data)} type."
    assert type(blenderBooleanObject.data) == BlenderDefinitions.BlenderTypes.MESH.value, \
        f"Object {withMeshObjectName} is not an Object. Cannot use the Boolean modifier with {type(blenderBooleanObject.data)} type."

    applyModifier(
        meshObjectName,
        BlenderDefinitions.BlenderModifiers.BOOLEAN,
        dict(
            {
                "operation": blenderBooleanType.name,
                "object": blenderBooleanObject,
                # "use_self": True,
                # "use_hole_tolerant": True,
                # "solver": "EXACT",
                # "double_threshold": 1e-6
            },
            **(keywordArguments or {})
        )
    )


def applyMirrorModifier(
    entityName,
    mirrorAcrossEntityName,
    axis: Utilities.Axis,
    keywordArguments: dict = {}
):

    axisList = [False, False, False]
    axisList[axis.value] = True

    blenderMirrorAcrossObject = getObject(mirrorAcrossEntityName)

    applyModifier(
        entityName,
        BlenderDefinitions.BlenderModifiers.MIRROR,
        dict(
            {
                "mirror_object": blenderMirrorAcrossObject,
                "use_axis": axisList,
                "use_mirror_merge": False
            },
            **keywordArguments
        )
    )


def applyScrewModifier(
    entityName,
    angle: Utilities.Angle,
    axis: Utilities.Axis,
    screwPitch: Utilities.Dimension = Utilities.Dimension(0),
    iterations=1,
    entityNameToDetermineAxis=None,
    keywordArguments: dict = {}
):

    # https://docs.blender.org/api/current/bpy.types.ScrewModifier.html
    properties = {
        "axis": axis.name,
        "angle": angle.value,
        "screw_offset": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(screwPitch).value,
        "steps": 64,
        "render_steps": 64,
        "use_merge_vertices": True,
        "iterations": iterations
    }

    if entityNameToDetermineAxis:

        blenderMirrorAcrossObject = getObject(entityNameToDetermineAxis)

        properties["object"] = blenderMirrorAcrossObject

    applyModifier(
        entityName,
        BlenderDefinitions.BlenderModifiers.SCREW,
        dict(
            properties,
            **keywordArguments
        )
    )


# MARK: CRUD of Objects (aka Parts)

def blenderPrimitiveFunction(
    primitive: BlenderDefinitions.BlenderObjectPrimitiveTypes,
    dimensions,
    keywordArguments={}
):

    if primitive == BlenderDefinitions.BlenderObjectPrimitiveTypes.cube:
        return bpy.ops.mesh.primitive_cube_add(size=1, scale=[dimension.value for dimension in dimensions[:3]], **keywordArguments)

    if primitive == BlenderDefinitions.BlenderObjectPrimitiveTypes.cone:
        return bpy.ops.mesh.primitive_cone_add(radius1=dimensions[0].value, radius2=dimensions[1].value, depth=dimensions[2].value, **keywordArguments)

    if primitive == BlenderDefinitions.BlenderObjectPrimitiveTypes.cylinder:
        return bpy.ops.mesh.primitive_cylinder_add(radius=dimensions[0].value, depth=dimensions[1].value, **keywordArguments)

    if primitive == BlenderDefinitions.BlenderObjectPrimitiveTypes.torus:
        return bpy.ops.mesh.primitive_torus_add(mode='EXT_INT', abso_minor_rad=dimensions[0].value, abso_major_rad=dimensions[1].value, **keywordArguments)

    if primitive == BlenderDefinitions.BlenderObjectPrimitiveTypes.sphere:
        return bpy.ops.mesh.primitive_ico_sphere_add(radius=dimensions[0].value, **keywordArguments)

    if primitive == BlenderDefinitions.BlenderObjectPrimitiveTypes.uvsphere:
        return bpy.ops.mesh.primitive_uv_sphere_add(radius=dimensions[0].value, **keywordArguments)

    if primitive == BlenderDefinitions.BlenderObjectPrimitiveTypes.circle:
        return bpy.ops.mesh.primitive_circle_add(radius=dimensions[0].value, **keywordArguments)

    if primitive == BlenderDefinitions.BlenderObjectPrimitiveTypes.grid:
        return bpy.ops.mesh.primitive_grid_add(size=dimensions[0].value, **keywordArguments)

    if primitive == BlenderDefinitions.BlenderObjectPrimitiveTypes.monkey:
        return bpy.ops.mesh.primitive_monkey_add(size=dimensions[0].value, **keywordArguments)

    if primitive == BlenderDefinitions.BlenderObjectPrimitiveTypes.empty:
        return bpy.ops.object.empty_add(radius=dimensions[0].value, **keywordArguments)

    if primitive == BlenderDefinitions.BlenderObjectPrimitiveTypes.plane:
        return bpy.ops.mesh.primitive_plane_add(**keywordArguments)

    raise Exception(
        f"Primitive with name {primitive.name} is not implemented.")


# Extracts dimensions from a string, then passes them as arguments to the blenderPrimitiveFunction
def addPrimitive(
    primitiveType: BlenderDefinitions.BlenderObjectPrimitiveTypes,
    dimensions: str,
    keywordArguments: Optional[dict]
):

    assert primitiveType != None, f"Primitive type is required."

    primitiveName = primitiveType.defaultNameInBlender()

    # Make sure an object or mesh with the same name don't already exist:
    blenderObject = bpy.data.objects.get(primitiveName)
    blenderMesh = bpy.data.meshes.get(primitiveName)

    assert blenderObject == None, f"An object with name {primitiveName} already exists."
    assert blenderMesh == None, f"A mesh with name {primitiveName} already exists."

    # Convert the dimensions:
    dimensionsList: list[Utilities.Dimension] = Utilities.getDimensionListFromStringList(
        dimensions) or []

    dimensionsList = BlenderDefinitions.BlenderLength.convertDimensionsToBlenderUnit(
        dimensionsList)

    # Add the object:
    blenderPrimitiveFunction(
        primitiveType,
        dimensionsList,
        keywordArguments or {}
    )


def createGear(
    objectName: str,
    outerRadius: DimensionOrItsFloatOrStringValue, addendum: DimensionOrItsFloatOrStringValue, innerRadius: DimensionOrItsFloatOrStringValue, dedendum: DimensionOrItsFloatOrStringValue, height: DimensionOrItsFloatOrStringValue, pressureAngle: AngleOrItsFloatOrStringValue = "20d", numberOfTeeth: 'int' = 12, skewAngle: AngleOrItsFloatOrStringValue = 0, conicalAngle: AngleOrItsFloatOrStringValue = 0, crownAngle: AngleOrItsFloatOrStringValue = 0
):
    addonName = "add_mesh_extra_objects"

    # check if the addon is enabled, enable it if it is not.
    addon = bpy.context.preferences.addons.get(addonName)
    if addon == None:
        addonSetEnabled(addonName, True)
        addon = bpy.context.preferences.addons.get(addonName)

    assert \
        addon != None, \
        f"Could not enable the {addonName} addon to create extra objects"

    outerRadiusDimension = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
        Utilities.Dimension.fromString(outerRadius)).value
    innerRadiusDimension = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
        Utilities.Dimension.fromString(innerRadius)).value
    addendumDimension = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
        Utilities.Dimension.fromString(addendum)).value
    dedendumDimension = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
        Utilities.Dimension.fromString(dedendum)).value
    heightDimension = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
        Utilities.Dimension.fromString(height)).value

    if addendumDimension > outerRadiusDimension/2:
        addendumDimension = outerRadiusDimension/2
    if innerRadiusDimension > outerRadiusDimension:
        innerRadiusDimension = outerRadiusDimension
    if dedendumDimension + innerRadiusDimension > outerRadiusDimension:
        dedendumDimension = outerRadiusDimension - innerRadiusDimension

    pressureAngleValue = Utilities.Angle.fromString(
        pressureAngle).toRadians().value
    skewAngleValue = Utilities.Angle.fromString(skewAngle).toRadians().value
    conicalAngleValue = Utilities.Angle.fromString(
        conicalAngle).toRadians().value
    crownAngleValue = Utilities.Angle.fromString(crownAngle).toRadians().value

    return bpy.ops.mesh.primitive_gear(  # type: ignore
        name=objectName,
        number_of_teeth=numberOfTeeth,
        radius=outerRadiusDimension,
        addendum=addendumDimension,
        dedendum=dedendumDimension,
        angle=pressureAngleValue,
        base=innerRadiusDimension,
        width=heightDimension,
        skew=skewAngleValue,
        conangle=conicalAngleValue,
        crown=crownAngleValue
    )


fileImportFunctions = {
    "stl": lambda filePath: bpy.ops.import_mesh.stl(filepath=filePath),
    "ply": lambda filePath: bpy.ops.import_mesh.ply(filepath=filePath),
    "svg": lambda filePath: bpy.ops.import_curve.svg(filepath=filePath),
    "png": lambda filePath: bpy.ops.image.open(filepath=filePath),
    "fbx": lambda filePath: bpy.ops.import_scene.fbx(filepath=filePath),
    "gltf": lambda filePath: bpy.ops.import_scene.gltf(filepath=filePath),
    "obj": lambda filePath: bpy.ops.import_scene.obj(filepath=filePath, use_split_objects=False),
    "x3d": lambda filePath: bpy.ops.import_scene.x3d(filepath=filePath)
}


def importFile(
    filePath: str,
    fileType: Optional[str] = None
):

    path = Path(filePath).resolve()

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
    fileType = fileType or path.suffix.replace(".", "")

    assert \
        fileType in fileImportFunctions, \
        f"File type {fileType} is not supported"

    # Import the file:
    isSuccess = fileImportFunctions[fileType](filePath) == {'FINISHED'}

    assert isSuccess == True, \
        f"Could not import {filePath}"

# MARK: Transformations

# Apply the object's transformations (under Object Properties tab)
# This is different from applyDependencyGraph()
# references https://blender.stackexchange.com/a/159540/138679


def applyObjectTransformations(objectName):

    blenderObject = getObject(objectName)

    assert blenderObject.data != None, \
        f"Object {objectName} does not have data to transform."

    finalPose = blenderObject.matrix_basis

    blenderObject.data.transform(finalPose)

    for child in blenderObject.children:
        child.matrix_local = finalPose @ child.matrix_local
        child.matrix_basis.identity()

    # Reset the object's transformations (resets everything in side menu to 0's)
    blenderObject.matrix_basis.identity()


def applyObjectRotationAndScale(objectName):
    blenderObject = getObject(objectName)

    assert blenderObject.data != None, \
        f"Object {objectName} does not have data to transform."

    translation, rotation, scale = blenderObject.matrix_basis.decompose()

    translation = mathutils.Matrix.Translation(translation)
    rotation = rotation.to_matrix().to_4x4()
    scale = mathutils.Matrix.Diagonal(scale).to_4x4()

    transformation = rotation @ scale

    blenderObject.data.transform(transformation)

    # Set the object to its world translation
    blenderObject.matrix_basis = translation

    for child in blenderObject.children:
        child.matrix_basis = transformation @ child.matrix_basis
        child.matrix_basis = mathutils.Matrix.Translation(
            child.matrix_basis.translation)


def rotateObject(
    objectName,
    rotationAngles: list[Optional[Utilities.Angle]],
    rotationType: BlenderDefinitions.BlenderRotationTypes
):

    blenderObject = getObject(objectName)

    currentRotation = getattr(blenderObject, rotationType.value)

    outputRotation = []

    for index in range(len(currentRotation)):
        angle = currentRotation[index]
        newAngle = rotationAngles[index]
        if newAngle != None:
            angle = newAngle.toRadians().value
        outputRotation.append(angle)

    setattr(blenderObject, rotationType.value, outputRotation)


def translateObject(
    objectName,
    translationDimensions: list[Optional[Utilities.Dimension]],
    translationType: BlenderDefinitions.BlenderTranslationTypes
):

    blenderObject = getObject(objectName)

    assert \
        len(translationDimensions) == 3, \
        "translationDimensions must be length 3"

    currentLocation = blenderObject.location

    outputLocation = []

    for index in range(3):
        location = currentLocation[index]
        newLocation = translationDimensions[index]
        if newLocation != None:
            location = newLocation.value
        outputLocation.append(location)

    setattr(blenderObject, translationType.value, outputLocation)


def setObjectLocation(
    objectName,
    locationDimensions: list[Optional[Utilities.Dimension]]
):

    blenderObject = getObject(objectName)

    assert \
        len(locationDimensions) == 3, \
        "locationDimensions must be length 3"

    currentLocation = blenderObject.location

    outputLocation = []

    for index in range(3):
        location = currentLocation[index]
        newLocation = locationDimensions[index]
        if newLocation != None:
            location = newLocation.value
        outputLocation.append(location)

    blenderObject.location = outputLocation


def scaleObject(
    objectName: str,
    xScaleFactor: Optional[float],
    yScaleFactor: Optional[float],
    zScaleFactor: Optional[float]
):

    blenderObject = getObject(objectName)

    currentScale = blenderObject.scale

    blenderObject.scale = (xScaleFactor or currentScale.x,
                           yScaleFactor or currentScale.y, zScaleFactor or currentScale.z)


# MARK: collections and groups:

def createCollection(
    name,
    sceneName="Scene"
):

    assert \
        name not in bpy.data.collections, \
        f"Collection {name} already exists"

    assert \
        sceneName in bpy.data.scenes, f"Scene {sceneName} does not exist"  # type: ignore

    collection = bpy.data.collections.new(name)

    bpy.data.scenes[sceneName].collection.children.link(collection)


def removeCollection(
    name,
    removeChildren
):

    assert \
        name in bpy.data.collections, \
        f"Collection {name} does not exist"

    if removeChildren:
        for obj in bpy.data.collections[name].objects:
            try:
                removeObject(obj.name, True)
            except Exception as e:
                pass

    bpy.data.collections.remove(bpy.data.collections[name])


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
    collectionName="Scene Collection",
    sceneName="Scene",
    removeFromOtherGroups=True,
    moveChildren=True
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
            assignObjectToCollection(
                child.name, collectionName, sceneName, True, True)


# MARK: Joints
def getConstraint(objectName, constraintName):
    blenderObject = getObject(objectName)
    return blenderObject.constraints.get(constraintName)


def applyConstraint(
    objectName,
    constraintType: BlenderDefinitions.BlenderConstraintTypes,
    keywordArguments={}
):

    blenderObject = getObject(objectName)

    constraintName = keywordArguments.get(
        "name") or constraintType.getDefaultBlenderName()

    constraint = blenderObject.constraints.get(constraintName)

    # If it doesn't exist, create it:
    if constraint is None:
        constraint = blenderObject.constraints.new(constraintType.name)

    # Apply every parameter passed in for modifier:
    for key, value in keywordArguments.items():
        setattr(constraint, key, value)


def applyLimitLocationConstraint(
    objectName,
    x: Optional[list[Optional[Utilities.Dimension]]],
    y: Optional[list[Optional[Utilities.Dimension]]],
    z: Optional[list[Optional[Utilities.Dimension]]],
    relativeToObjectName,
    keywordArguments={}
):

    relativeToObject = getObject(
        relativeToObjectName) if relativeToObjectName else None

    [minX, maxX] = x or [None, None]
    [minY, maxY] = y or [None, None]
    [minZ, maxZ] = z or [None, None]

    keywordArguments = keywordArguments or {}

    keywordArguments["name"] = f"loc_{objectName}_{relativeToObjectName}"

    keywordArguments["owner_space"] = "CUSTOM" if relativeToObject else "WORLD"

    keywordArguments["space_object"] = relativeToObject

    if minX:
        keywordArguments["use_min_x"] = True
        keywordArguments["min_x"] = minX.value
    if minY:
        keywordArguments["use_min_y"] = True
        keywordArguments["min_y"] = minY.value
    if minZ:
        keywordArguments["use_min_z"] = True
        keywordArguments["min_z"] = minZ.value
    if maxX:
        keywordArguments["use_max_x"] = True
        keywordArguments["max_x"] = maxX.value
    if maxY:
        keywordArguments["use_max_y"] = True
        keywordArguments["max_y"] = maxY.value
    if maxZ:
        keywordArguments["use_max_z"] = True
        keywordArguments["max_z"] = maxZ.value

    applyConstraint(
        objectName,
        BlenderDefinitions.BlenderConstraintTypes.LIMIT_LOCATION,
        keywordArguments
    )


def applyLimitRotationConstraint(
    objectName,
    x: Optional[list[Optional[Utilities.Angle]]],
    y:  Optional[list[Optional[Utilities.Angle]]],
    z:  Optional[list[Optional[Utilities.Angle]]],
    relativeToObjectName,
    keywordArguments={}
):

    relativeToObject = getObject(
        relativeToObjectName) if relativeToObjectName else None

    [minX, maxX] = x or [None, None]
    [minY, maxY] = y or [None, None]
    [minZ, maxZ] = z or [None, None]

    keywordArguments = keywordArguments or {}

    keywordArguments["name"] = f"rot_{objectName}_{relativeToObjectName}"

    keywordArguments["owner_space"] = "CUSTOM" if relativeToObject else "WORLD"

    keywordArguments["space_object"] = relativeToObject

    if minX:
        keywordArguments["use_limit_x"] = True
        keywordArguments["min_x"] = minX.toRadians().value
    if minY:
        keywordArguments["use_limit_y"] = True
        keywordArguments["min_y"] = minY.toRadians().value
    if minZ:
        keywordArguments["use_limit_z"] = True
        keywordArguments["min_z"] = minZ.toRadians().value
    if maxX:
        keywordArguments["use_limit_x"] = True
        keywordArguments["max_x"] = maxX.toRadians().value
    if maxY:
        keywordArguments["use_limit_y"] = True
        keywordArguments["max_y"] = maxY.toRadians().value
    if maxZ:
        keywordArguments["use_limit_z"] = True
        keywordArguments["max_z"] = maxZ.toRadians().value

    applyConstraint(
        objectName,
        BlenderDefinitions.BlenderConstraintTypes.LIMIT_ROTATION,
        keywordArguments
    )


def applyPivotConstraint(
    objectName,
    pivotObjectName,
    keywordArguments={}
):

    pivotObject = getObject(pivotObjectName)

    applyConstraint(
        objectName,
        BlenderDefinitions.BlenderConstraintTypes.PIVOT,
        dict(
            {
                "name": f"pivot_{objectName}_{pivotObjectName}",
                "target": pivotObject,
                "rotation_range": "ALWAYS_ACTIVE"
            },
            **keywordArguments
        )
    )


def applyGearConstraint(
    objectName,
    gearObjectName,
    ratio: float = 1,
    keywordArguments={}
):

    for axis in Utilities.Axis:
        # e.g. constraints["Limit Location"].min_x
        driver = createDriver(objectName, "rotation_euler", axis.value)
        setDriver(driver, "SCRIPTED", f"{-1*ratio} * gearRotation")
        setDriverVariableSingleProp(
            driver, "gearRotation", gearObjectName, f"rotation_euler[{axis.value}]")

# MARK: Drivers / Computed variables


def createDriver(
    objectName,
    path,
    index=-1
):

    blenderObject = getObject(objectName)

    return blenderObject.driver_add(path, index).driver


def removeDriver(
    objectName,
    path,
    index=-1
):

    blenderObject = getObject(objectName)

    blenderObject.driver_remove(path, index)


def getDriver(
    objectName,
    path
):
    blenderObject = getObject(objectName)

    # this returns an FCurve object
    # https://docs.blender.org/api/current/bpy.types.FCurve.html
    fcurve = blenderObject.animation_data.drivers.find(path)

    assert fcurve != None, f"Could not find driver {path} for object {objectName}."

    return fcurve.driver


def setDriver(
    driver,
    driverType,  # : BlenderDefinitions.BlenderDriverTypes,
    expression=""
):

    driver.type = driverType

    driver.expression = expression if expression else ""


def setDriverVariableSingleProp(
    driver,
    variableName,
    targetObjectName,
    targetDataPath
):

    variable = driver.variables.get(variableName)

    if variable is None:
        variable = driver.variables.new()
        driver.variables[-1].name = variableName

    variable.type = "SINGLE_PROP"

    targetObject = getObject(targetObjectName)

    variable.targets[0].id = targetObject

    variable.targets[0].data_path = targetDataPath


def setDriverVariableTransforms(
    driver,
    variableName,
    targetObjectName,
    transform_type,  # : BlenderDefinitions.BlenderDriverVariableTransformTypes,
    transform_space,  # : BlenderDefinitions.BlenderDriverVariableTransformSpaces
):

    variable = driver.variables.get(variableName)

    if variable is None:
        variable = driver.variables.new()
        driver.variables[-1].name = variableName

    variable.type = "‘TRANSFORMS’"

    targetObject = getObject(targetObjectName)

    variable.targets[0].id = targetObject

    variable.targets[0].transform_type = transform_type

    variable.targets[0].transform_space = transform_space


def setDriverVariableLocationDifference(
    driver,
    variableName,
    target1ObjectName,
    target2ObjectName
):

    variable = driver.variables.get(variableName)

    if variable is None:
        variable = driver.variables.new()
        driver.variables[-1].name = variableName

    variable.type = "‘LOC_DIFF’"

    target1Object = getObject(target1ObjectName)

    variable.targets[0].id = target1Object

    target2Object = getObject(target2ObjectName)

    variable.targets[1].id = target2Object


def setDriverVariableRotationDifference(
    driver,
    variableName,
    target1ObjectName,
    target2ObjectName
):

    variable = driver.variables.get(variableName)

    if variable is None:
        variable = driver.variables.new()
        driver.variables[-1].name = variableName

    variable.type = "‘ROTATION_DIFF’"

    target1Object = getObject(target1ObjectName)

    variable.targets[0].id = target1Object

    target2Object = getObject(target2ObjectName)

    variable.targets[1].id = target2Object


# MARK: Landmarks

def translateLandmarkOntoAnother(
    objectToTranslateName,
    object1LandmarkName,
    object2LandmarkName
):

    updateViewLayer()
    object1LandmarkLocation = getObjectWorldLocation(object1LandmarkName)
    object2LandmarkLocation = getObjectWorldLocation(object2LandmarkName)

    translation = (object1LandmarkLocation)-(object2LandmarkLocation)

    blenderDefaultUnit = BlenderDefinitions.BlenderLength.DEFAULT_BLENDER_UNIT.value

    translateObject(
        objectToTranslateName,
        [
            Utilities.Dimension(translation.x, blenderDefaultUnit),
            Utilities.Dimension(translation.y, blenderDefaultUnit),
            Utilities.Dimension(translation.z, blenderDefaultUnit)
        ],
        BlenderDefinitions.BlenderTranslationTypes.ABSOLUTE
    )

# MARK: creating and manipulating objects


def makeParent(
    name,
    parentName
):

    blenderObject = getObject(name)
    blenderParentObject = getObject(parentName)

    blenderObject.parent = blenderParentObject


def updateObjectName(
    oldName,
    newName
):

    blenderObject = getObject(oldName)

    blenderObject.name = newName


def getObjectCollectionName(objectName) -> str:

    blenderObject = getObject(objectName)

    # Assumes the first collection is the main collection
    [currentCollection] = blenderObject.users_collection

    return currentCollection.name


def updateObjectDataName(
    parentObjectName,
    newName
):

    blenderObject = getObject(parentObjectName)

    assert blenderObject.data != None, f"Object {parentObjectName} does not have data to name."

    blenderObject.data.name = newName


# This assumes that landmarks are named with format: `{parentPartName}_{landmarkName}`
def updateObjectLandmarkNames(
    parentObjectName,
    oldNamePrefix,
    newNamePrefix
):

    blenderObject = getObject(parentObjectName)

    for child in blenderObject.children:
        if f"{oldNamePrefix}_" in child.name and child.type == "EMPTY":
            updateObjectName(child.name, child.name.replace(
                f"{oldNamePrefix}_", f"{newNamePrefix}_"))


def removeObject(
    existingObjectName,
    removeChildren=False
):

    blenderObject = getObject(existingObjectName)

    if removeChildren:
        for child in blenderObject.children:
            try:
                removeObject(child.name, True)
            except:
                pass

    # Not all objects have data, but if they do, then deleting the data
    # deletes the object
    if blenderObject.data and type(blenderObject.data) == bpy.types.Mesh:
        bpy.data.meshes.remove(blenderObject.data)
    elif blenderObject.data and type(blenderObject.data) == bpy.types.Curve:
        bpy.data.curves.remove(blenderObject.data)
    elif blenderObject.data and type(blenderObject.data) == bpy.types.TextCurve:
        bpy.data.curves.remove(blenderObject.data)
    else:
        bpy.data.objects.remove(blenderObject)


def createObject(
    name,
    data=None
):

    blenderObject = bpy.data.objects.get(name)

    assert \
        blenderObject == None, \
        f"Object {name} already exists"

    return bpy.data.objects.new(name, data)


def createObjectVertexGroup(objectName, vertexGroupName):
    blenderObject = getObject(objectName)
    return blenderObject.vertex_groups.new(name=vertexGroupName)


def getObjectVertexGroup(objectName, vertexGroupName):
    blenderObject = getObject(objectName)
    return blenderObject.vertex_groups.get(vertexGroupName)


def addVerticiesToVertexGroup(vertexGroupObject, vertexIndecies: list[int]):
    vertexGroupObject.add(vertexIndecies, 1.0, 'ADD')


def createMeshFromCurve(
    existingCurveObjectName,
    newObjectName=None
):

    existingCurveObject = getObject(existingCurveObjectName)

    if newObjectName is None:
        updateObjectName(existingCurveObjectName, str(uuid4()))
        newObjectName = existingCurveObjectName

    dependencyGraph = bpy.context.evaluated_depsgraph_get()
    mesh = bpy.data.meshes.new_from_object(
        existingCurveObject.evaluated_get(dependencyGraph), depsgraph=dependencyGraph)

    blenderObject = createObject(newObjectName, mesh)

    blenderObject.matrix_world = existingCurveObject.matrix_world

    assignObjectToCollection(newObjectName)

    for child in existingCurveObject.children:
        if type(child) == BlenderDefinitions.BlenderTypes.OBJECT.value and child.type == 'EMPTY':
            child.parent = blenderObject

    # twisted logic here, but if we renamed this above, we want to nuke it because we're done with it.
    if existingCurveObject.name != existingCurveObjectName:
        removeObject(existingCurveObject.name, removeChildren=True)


def getObjectVisibility(
    existingObjectName
) -> bool:

    blenderObject = getObject(existingObjectName)

    return blenderObject.visible_get()


def setObjectVisibility(
    existingObjectName,
    isVisible
):

    blenderObject = getObject(existingObjectName)

    # blenderObject.hide_viewport = not isVisible
    # blenderObject.hide_render = not isVisible
    blenderObject.hide_set(not isVisible)


def transferLandmarks(
    fromObjectName,
    toObjectName
):

    updateViewLayer()

    fromBlenderObject = getObject(fromObjectName)
    toBlenderObject = getObject(toObjectName)

    translation = getObjectWorldLocation(
        fromObjectName) - getObjectWorldLocation(toObjectName)

    defaultCollection = getObjectCollectionName(toObjectName)

    for child in fromBlenderObject.children:
        if type(child) == BlenderDefinitions.BlenderTypes.OBJECT.value and child.type == 'EMPTY':
            child.name = f"{toObjectName}_{child.name}"
            isAlreadyExists = bpy.data.objects.get(child.name) == None
            if isAlreadyExists:
                print(f"{child.name} already exists. Skipping landmark transfer.")
                continue
            child.parent = toBlenderObject
            child.location = child.location + translation
            assignObjectToCollection(child.name, defaultCollection)


def duplicateObject(
    existingObjectName,
    newObjectName,
    copyLandmarks: bool = True
):

    clonedObject = bpy.data.objects.get(newObjectName)

    assert clonedObject == None, \
        f"Object with name {newObjectName} already exists."

    blenderObject = getObject(existingObjectName)

    clonedObject = blenderObject.copy()
    clonedObject.name = newObjectName
    clonedObject.data = blenderObject.data.copy()
    clonedObject.data.name = newObjectName

    # Link clonedObject to the original object's collection.
    defaultCollection = getObjectCollectionName(existingObjectName)

    assignObjectToCollection(newObjectName, defaultCollection)

    if copyLandmarks:
        for child in blenderObject.children:
            if type(child) == BlenderDefinitions.BlenderTypes.OBJECT.value and child.type == 'EMPTY':
                newChild = child.copy()
                newChild.name = child.name.replace(
                    existingObjectName, newObjectName)
                newChild.parent = clonedObject
                assignObjectToCollection(newChild.name, defaultCollection)


def updateViewLayer():
    bpy.context.view_layer.update()


def getObjectLocalLocation(objectName):

    blenderObject = getObject(objectName)

    return blenderObject.location


def getObjectWorldLocation(objectName):

    blenderObject = getObject(objectName)

    return blenderObject.matrix_world.translation


def getObjectWorldPose(objectName):

    blenderObject = getObject(objectName)

    return blenderObject.matrix_world


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


# Applies the dependency graph to the object and persists its data using .copy()
# This allows us to apply modifiers, UV data, etc.. to the mesh.
# This is different from applyObjectTransformations()
def applyDependencyGraph(
    existingObjectName
):

    blenderObject = getObject(existingObjectName)

    blenderObject.data = blenderObject.evaluated_get(
        bpy.context.evaluated_depsgraph_get()
    ).data.copy()


def clearModifiers(objectName):

    blenderObject = getObject(objectName)

    blenderObject.modifiers.clear()


def removeMesh(mesh):

    # if a (str) name is passed in, fetch the mesh object reference
    if type(mesh) == str:
        mesh = getMesh(mesh)

    bpy.data.meshes.remove(mesh)


def setEdgesMeanCrease(meshName, meanCreaseValue):

    blenderMesh = getMesh(meshName)

    for edge in blenderMesh.edges:
        edge.crease = meanCreaseValue


# Note: transformations have to be applied for this to be reliable.
def isCollisionBetweenTwoObjects(object1Name, object2Name):
    blenderObject1 = getObject(object1Name)
    blenderObject2 = getObject(object2Name)

    dependencyGraph = bpy.context.evaluated_depsgraph_get()

    bvhTreeObject1 = BVHTree.FromObject(blenderObject1, dependencyGraph)
    bvhTreeObject2 = BVHTree.FromObject(blenderObject2, dependencyGraph)

    uniqueIndecies = bvhTreeObject1.overlap(bvhTreeObject2)  # type: ignore

    return len(uniqueIndecies) > 0


# References https://docs.blender.org/api/current/mathutils.kdtree.html
def createKdTreeForObject(objectName):
    blenderObject = getObject(objectName)
    mesh = blenderObject.data
    size = len(mesh.vertices)
    kd = KDTree(size)

    for i, v in enumerate(mesh.vertices):
        kd.insert(v.co, i)

    kd.balance()
    return kd


# uses object.closest_point_on_mesh https://docs.blender.org/api/current/bpy.types.Object.html#bpy.types.Object.closest_point_on_mesh
def getClosestFaceToVertex(objectName, vertex):

    blenderObject = getObject(objectName)

    assert \
        len(vertex) == 3, \
        "Vertex is not length 3. Please provide a proper vertex (x,y,z)"

    matrixWorld = blenderObject.matrix_world
    invertedMatrixWorld = matrixWorld.inverted()

    # vertex in object space:
    vertexInverted = invertedMatrixWorld @ mathutils.Vector(vertex)

    # polygonIndex references an index at blenderObject.data.polygons[polygonIndex], in other words, the face or edge data
    [isFound, closestPoint, normal,
        polygonIndex] = blenderObject.closest_point_on_mesh(vertexInverted)

    assert \
        isFound, \
        f"Could not find a point close to {vertex} on {objectName}"

    assert \
        polygonIndex != None and polygonIndex != -1, \
        f"Could not find a face near {vertex} on {objectName}"

    blenderPolygon = blenderObject.data.polygons[polygonIndex]

    return blenderPolygon


# Returns a list of (co, index, dist)
def getClosestPointsToVertex(objectName, vertex, numberOfPoints=2, objectKdTree=None):

    blenderObject = getObject(objectName)

    kdTree = objectKdTree or createKdTreeForObject(objectName)

    assert \
        len(vertex) == 3, \
        "Vertex is not length 3. Please provide a proper vertex (x,y,z)"

    matrixWorld = blenderObject.matrix_world
    invertedMatrixWorld = matrixWorld.inverted()

    vertexInverted = invertedMatrixWorld @ mathutils.Vector(vertex)

    return kdTree.find_n(vertexInverted, numberOfPoints)


# References https://blender.stackexchange.com/a/32288/138679
def getBoundingBox(objectName):

    updateViewLayer()

    blenderObject = getObject(objectName)

    local_coords = blenderObject.bound_box[:]

    # om = blenderObject.matrix_world
    om = blenderObject.matrix_basis

    # matrix multiple world transform by all the vertices in the boundary
    coords = [(om @ mathutils.
               Vector(p[:])).to_tuple() for p in local_coords]
    coords = coords[::-1]
    # Coords should be a 1x8 array containing 1x3 vertices, example:
    # [(1.0, 1.0, -1.0), (1.0, 1.0, 1.0), (1.0, -1.0, 1.0), (1.0, -1.0, -1.0), (-1.0, 1.0, -1.0), (-1.0, 1.0, 1.0), (-1.0, -1.0, 1.0), (-1.0, -1.0, -1.0)]

    # After zipping we should get
    # x (1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0, -1.0)
    # y (1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0, -1.0)
    # z (-1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0)
    zipped = zip('xyz', zip(*coords))

    boundingBox = Utilities.BoundaryBox(None, None, None)

    for (axis, _list) in zipped:

        minVal = min(_list)
        maxVal = max(_list)

        setattr(
            boundingBox,
            axis,
            Utilities.BoundaryAxis(
                minVal,
                maxVal,
                "m"
            )
        )

    return boundingBox


# MARK: ADDONS

def addonSetEnabled(addonName, isEnabled):
    preferences = bpy.ops.preferences

    command = preferences.addon_enable if isEnabled else preferences.addon_disable

    command(module=addonName)


# MARK: Curves and Sketches

def extrude(
    curveObjectName,
    length: Utilities.Dimension
):

    blenderObject = getObject(curveObjectName)

    length = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
        length)

    assert type(blenderObject.data) == BlenderDefinitions.BlenderTypes.CURVE.value or type(blenderObject.data) == BlenderDefinitions.BlenderTypes.TEXT.value,\
        f"Object {curveObjectName} is not a curve or text object type."

    blenderObject.data.extrude = length.value


def createText(curveName, text,
               size=Utilities.Dimension(1),
               bold=False,
               italic=False,
               underlined=False,
               characterSpacing=1,
               wordSpacing=1,
               lineSpacing=1,
               fontFilePath=None):

    curveData = bpy.data.curves.new(type="FONT", name=curveName)
    setattr(curveData, "body", text)
    setattr(curveData, "size", BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
        size).value)
    setattr(curveData, "space_character", characterSpacing)
    setattr(curveData, "space_word", wordSpacing)
    setattr(curveData, "space_line", lineSpacing)

    if fontFilePath:
        fontData = bpy.data.fonts.load(fontFilePath.replace("\\", "/"))
        setattr(curveData, "font", fontData)

    if bold or italic or underlined:
        curveDataBodyFormat = curveData.body_format  # type: ignore
        for index in range(len(text)):
            curveDataBodyFormat[index].use_underline = underlined
            curveDataBodyFormat[index].use_bold = bold
            curveDataBodyFormat[index].use_bold = italic

        setattr(curveData, "body_format", curveDataBodyFormat)

    createObject(curveName, curveData)

    assignObjectToCollection(curveName)


def create3DCurve(
    curveName,
    curveType: BlenderDefinitions.BlenderCurveTypes,
    coordinates,
    interpolation=64
):

    curveData = bpy.data.curves.new(curveName, type='CURVE')
    curveData.dimensions = '3D'
    curveData.resolution_u = interpolation
    curveData.use_path = False

    createSpline(curveData, curveType, coordinates)

    createObject(curveName, curveData)

    assignObjectToCollection(curveName)


# Creates a new Splines instance in the bpy.types.curves object passed in as blenderCurve
# then assigns the coordinates to them.
# references https://blender.stackexchange.com/a/6751/138679
def createSpline(
    blenderCurve,
    curveType: BlenderDefinitions.BlenderCurveTypes,
        coordinates
):

    coordinates = [
        BlenderDefinitions.BlenderLength.convertDimensionsToBlenderUnit(
            Utilities.getDimensionListFromStringList(coordinate) or []
        ) for coordinate in coordinates
    ]
    coordinates = [[dimension.value for dimension in coordinate]
                   for coordinate in coordinates]

    spline = blenderCurve.splines.new(curveType.name)
    spline.order_u = 2

    # subtract 1 so the end and origin points are not connected
    numberOfPoints = len(coordinates)-1

    if curveType == BlenderDefinitions.BlenderCurveTypes.BEZIER:

        # subtract 1 so the end and origin points are not connected
        spline.bezier_points.add(numberOfPoints)
        for i, coord in enumerate(coordinates):
            x, y, z = coord
            spline.bezier_points[i].co = (x, y, z)
            spline.bezier_points[i].handle_left = (x, y, z)
            spline.bezier_points[i].handle_right = (x, y, z)

    else:

        # subtract 1 so the end and origin points are not connected
        spline.points.add(numberOfPoints)

        for i, coord in enumerate(coordinates):
            x, y, z = coord
            spline.points[i].co = (x, y, z, 1)


def addBevelObjectToCurve(
    pathCurveObjectName,
    profileCurveObjectName,
    fillCap=False
):

    pathCurveObject = getObject(pathCurveObjectName)

    profileCurveObject = getObject(profileCurveObjectName)

    assert \
        type(profileCurveObject.data) == bpy.types.Curve, \
        f"Profile Object {profileCurveObjectName} is not a Curve object. Please use a Curve object."

    pathCurveObject.data.bevel_mode = "OBJECT"
    pathCurveObject.data.bevel_object = profileCurveObject
    pathCurveObject.data.use_fill_caps = fillCap


def getBlenderCurvePrimitiveFunction(curvePrimitive: BlenderDefinitions.BlenderCurvePrimitiveTypes):
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

    raise TypeError("Unknown primitive")


class BlenderCurvePrimitives():
    @ staticmethod
    def createPoint(curveType=BlenderDefinitions.BlenderCurveTypes.NURBS, keywordArguments={}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Point,
            dict(
                {
                    "use_cyclic_u": False
                },
                **keywordArguments
            )
        )

    @ staticmethod
    def createLineTo(endLocation, keywordArguments={}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.LineTo,
            dict(
                {
                    "Simple_endlocation": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension.fromString(endLocation)).value,
                    "use_cyclic_u": False
                },
                **keywordArguments
            )
        )

    @ staticmethod
    def createLine(length, keywordArguments={}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Distance,
            dict(
                {
                    "Simple_length": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension.fromString(length)).value,
                    "Simple_center": True,
                    "use_cyclic_u": False
                },
                **keywordArguments
            )
        )

    @ staticmethod
    def createAngle(length, angle, keywordArguments={}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Angle,
            dict(
                {
                    "Simple_length": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension.fromString(length)).value,
                    "Simple_angle": Utilities.Angle.fromString(angle).toDegrees().value,
                    "use_cyclic_u": False
                },
                **keywordArguments
            )
        )

    @ staticmethod
    def createCircle(radius, keywordArguments={}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Circle,
            dict(
                {
                    "Simple_radius": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension.fromString(radius)).value,
                    "Simple_sides": 64
                },
                **keywordArguments
            )
        )

    @ staticmethod
    def createEllipse(radius_x, radius_y, keywordArguments={}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Ellipse,
            dict(
                {
                    "Simple_a": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension.fromString(radius_x)).value,
                    "Simple_b": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension.fromString(radius_y)).value
                },
                **keywordArguments
            )
        )

    @ staticmethod
    def createArc(radius, angle, keywordArguments={}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Arc,
            dict(
                {
                    "Simple_sides": 64,
                    "Simple_radius": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension.fromString(radius)).value,
                    "Simple_startangle": 0,
                    "Simple_endangle": Utilities.Angle.fromString(angle).toDegrees().value,
                    "use_cyclic_u": False
                },
                **keywordArguments
            )
        )

    @ staticmethod
    def createSector(radius, angle, keywordArguments={}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Sector,
            dict(
                {
                    "Simple_sides": 64,
                    "Simple_radius": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension.fromString(radius)).value,
                    "Simple_startangle": 0,
                    "Simple_endangle": Utilities.Angle.fromString(angle).toDegrees().value
                },
                **keywordArguments
            )
        )

    @ staticmethod
    def createSegment(outter_radius, inner_radius, angle, keywordArguments={}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Segment,
            dict(
                {
                    "Simple_sides": 64,
                    "Simple_a": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension.fromString(outter_radius)).value,
                    "Simple_b": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension.fromString(inner_radius)).value,
                    "Simple_startangle": 0,
                    "Simple_endangle": Utilities.Angle.fromString(angle).toDegrees().value
                },
                **keywordArguments
            )
        )

    @ staticmethod
    def createRectangle(length, width, keywordArguments={}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Rectangle,
            dict(
                {
                    "Simple_length": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension.fromString(length)).value,
                    "Simple_width": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension.fromString(width)).value,
                    "Simple_rounded": 0
                },
                **keywordArguments
            )
        )

    @ staticmethod
    def createRhomb(length, width, keywordArguments={}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Rhomb,
            dict(
                {
                    "Simple_length": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension.fromString(length)).value,
                    "Simple_width": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension.fromString(width)).value,
                    "Simple_center": True
                },
                **keywordArguments
            )
        )

    @ staticmethod
    def createPolygon(numberOfSides, radius, keywordArguments={}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Polygon,
            dict(
                {
                    "Simple_sides": numberOfSides,
                    "Simple_radius": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension.fromString(radius)).value
                },
                **keywordArguments
            )
        )

    @ staticmethod
    def createPolygon_ab(numberOfSides, radius_x, radius_y, keywordArguments={}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Polygon_ab,
            dict(
                {
                    "Simple_sides": numberOfSides,
                    "Simple_a": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension.fromString(radius_x)).value,
                    "Simple_b": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension.fromString(radius_y)).value
                },
                **keywordArguments
            )
        )

    @ staticmethod
    def createTrapezoid(length_upper, length_lower, height, keywordArguments={}):
        createSimpleCurve(
            BlenderDefinitions.BlenderCurvePrimitiveTypes.Trapezoid,
            dict(
                {
                    "Simple_a": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension.fromString(length_upper)).value,
                    "Simple_b": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension.fromString(length_lower)).value,
                    "Simple_h": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(Utilities.Dimension.fromString(height)).value
                },
                **keywordArguments
            )
        )


# assumes add_curve_extra_objects is enabled
# https://github.com/blender/blender-addons/blob/master/add_curve_extra_objects/add_curve_simple.py
def createSimpleCurve(curvePrimitiveType: BlenderDefinitions.BlenderCurvePrimitiveTypes, keywordArguments={}):

    curveType: BlenderDefinitions.BlenderCurveTypes = keywordArguments[
        "curveType"] if "curveType" in keywordArguments and keywordArguments["curveType"] else curvePrimitiveType.getDefaultCurveType()

    keywordArguments.pop("curveType", None)  # remove curveType from kwargs

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
    bpy.ops.curve.simple(Simple_Type=curvePrimitiveType.name, outputType=curveType.name,  # type: ignore
                         order_u=2, shape='2D',  edit_mode=False, **keywordArguments)


# MARK: manipulating the Scene

# locks the scene interface
def sceneLockInterface(isLocked):
    bpy.context.scene.render.use_lock_interface = isLocked


def setDefaultUnit(
    blenderUnit: BlenderDefinitions.BlenderLength,
    sceneName="Scene"
):

    blenderScene = bpy.data.scenes.get(sceneName)

    assert \
        blenderScene != None, \
        f"Scene {sceneName} does not exist"

    blenderScene.unit_settings.system = blenderUnit.getSystem()
    blenderScene.unit_settings.length_unit = blenderUnit.name


def selectObject(objectName: str):
    blenderObject = getObject(objectName)

    blenderObject.select_set(True)


def zoomToSelectedObjects():
    # References https://blender.stackexchange.com/a/7419/138679
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    override = {'area': area, 'region': region,
                                'edit_object': bpy.context.edit_object}
                    bpy.ops.view3d.view_all(override)


def addDependencyGraphUpdateListener(callback):
    bpy.app.handlers.depsgraph_update_post.append(callback)  # type: ignore


def addTimer(callback):
    bpy.app.timers.register(callback)


def getMaterial(materialName):
    blenderMaterial = bpy.data.materials.get(materialName)

    assert \
        blenderMaterial != None, \
        f"Material {materialName} does not exist."

    return blenderMaterial


def createMaterial(newMaterialName):
    material = bpy.data.materials.get(newMaterialName)

    assert \
        material == None, \
        f"Material with name {material} already exists."

    material = bpy.data.materials.new(name=newMaterialName)

    return material


def setMaterialColor(materialName, rValue, gValue, bValue, aValue=1.0):
    if type(rValue) == int:
        rValue /= 255.0

    if type(gValue) == int:
        gValue /= 255.0

    if type(bValue) == int:
        bValue /= 255.0

    if type(aValue) == int:
        aValue /= 255.0

    material = getMaterial(materialName)

    material.diffuse_color = (rValue, gValue, bValue, aValue)

    return material


def setMaterialToObject(materialName, objectName):

    material = getMaterial(materialName)

    object = getObject(objectName)

    objectMaterial = object.data.materials

    if len(objectMaterial) == 0:
        objectMaterial.append(material)
    else:
        objectMaterial[0] = material

    return material


def getBlenderVersion() -> tuple:
    return bpy.app.version  # type: ignore


fileExportFunctions = {
    "stl": lambda filePath, scale: bpy.ops.export_mesh.stl(
        filepath=filePath,
        use_selection=True,
        global_scale=scale
    ),
    "obj": lambda filePath, scale:
    bpy.ops.wm.obj_export(
        filepath=filePath,
        export_selected_objects=True,
        global_scale=scale
    )
        if getBlenderVersion() >= BlenderDefinitions.BlenderVersions.THREE_DOT_ONE.value else
    bpy.ops.export_scene.obj(
        filepath=filePath,
        use_selection=True,
        global_scale=scale
    ),

}


def exportObject(
    objectName,
    filePath,
    overwrite=True,
    scale=1.0
):

    path = Path(filePath).resolve()

    # Check if the file exists:
    if not overwrite:
        assert \
            not path.is_file(),\
            f"File {filePath} already exists"

    bpy.ops.object.select_all(action='DESELECT')

    blenderObject = getObject(objectName)

    blenderObject.select_set(True)

    # Check if this is a file-type we support:
    fileType = path.suffix.replace(".", "")

    assert \
        fileType in fileImportFunctions, \
        f"File type {fileType} is not supported"

    # export the file:
    isSuccess = fileExportFunctions[fileType](filePath, scale) == {'FINISHED'}

    assert isSuccess == True, \
        f"Could not export {filePath}"


# TODO: bind this to BlenderProvider
def separateObject(
        objectName):
    bpy.ops.object.select_all(action='DESELECT')

    blenderObject = getObject(objectName)

    blenderObject.select_set(True)

    isSuccess = bpy.ops.mesh.separate(type='LOOSE') == {'FINISHED'}

    assert isSuccess == True, \
        f"Could not separate object"

# MARK: Animation


def addKeyframeToObject(objectName: str, frameNumber: int, dataPath: str):
    blenderObject = getObject(objectName)

    # Acts on https://docs.blender.org/api/current/bpy.types.Keyframe.html
    blenderObject.keyframe_insert(data_path=dataPath, frame=frameNumber)


# def getTexture(textureName):
# 	blenderTexture = bpy.data.textures.get(textureName)

# 	assert \
# 		blenderTexture != None, \
# 			f"Texture {textureName} does not exist."

# 	return blenderTexture


# def createImageTexture(textureName, imageFilePath, repeatMode:BlenderDefinitions.RepeatMode):
#   image = bpy.data.images.load(imageFilePath)
#   blenderTexture = bpy.data.textures.new(name=textureName, type="IMAGE")
#   blenderTexture.image = image
#   blenderTexture.extension = repeatMode.getBlenderName

# ref https://blender.stackexchange.com/questions/118646/add-a-texture-to-an-object-using-python-and-blender-2-8/129014#129014

def addTextureToMaterial(materialName, imageFilePath):
    material = getMaterial(materialName)
    material.use_nodes = True
    bsdf = material.node_tree.nodes["Principled BSDF"]
    texImage = material.node_tree.nodes.new('ShaderNodeTexImage')
    image = bpy.data.images.load(imageFilePath)
    texImage.image = image
    material.node_tree.links.new(
        bsdf.inputs['Base Color'], texImage.outputs['Color'])


def logMessage(message):
    bpy.ops.code_to_cad.log_message(message=message)  # type: ignore


def createLight(objName, energyLevel, type):
    light_data = bpy.data.lights.new(name=objName, type=type)
    setattr(light_data, "energy", energyLevel)
    createObject(objName, data=light_data)
    assignObjectToCollection(objName)


def getLight(lightName):
    blenderLight = bpy.data.lights.get(lightName)

    assert \
        blenderLight != None, \
        f"Light {lightName} does not exist."

    return blenderLight


def setLightColor(lightName, rValue, gValue, bValue):
    if type(rValue) == int:
        rValue /= 255.0

    if type(gValue) == int:
        gValue /= 255.0

    if type(bValue) == int:
        bValue /= 255.0

    light = getLight(lightName)

    light.color = (rValue, gValue, bValue)

    return light


def createCamera(objName, type):
    camera_data = bpy.data.cameras.new(name=objName)
    createObject(objName, data=camera_data)
    assignObjectToCollection(objName)


def getCamera(cameraName):
    blenderCamera = bpy.data.cameras.get(cameraName)

    assert \
        blenderCamera != None, \
        f"Camera {cameraName} does not exist."

    return blenderCamera


def setFocalLength(cameraName, length=50.0):
    camera = getCamera(cameraName)
    assert \
        length >= 1, \
        "Length needs to be greater than or equal to 1."

    camera.lens = length


def addHDRTexture(sceneName, imageFilePath):
    deleteNodes(sceneName)
    nodeBackground = createNodes(sceneName, 'ShaderNodeBackground')
    nodeEnvironment = createNodes(sceneName, 'ShaderNodeTexEnvironment')
    nodeEnvironment.image = bpy.data.images.load(imageFilePath)
    nodeEnvironment.location = 0, 0
    nodeOutput = createNodes(sceneName, 'ShaderNodeOutputWorld')
    nodeOutput.location = 0, 0
    links = getNodeTree(sceneName).links
    links.new(nodeEnvironment.outputs["Color"], nodeBackground.inputs["Color"])
    links.new(nodeBackground.outputs["Background"],
              nodeOutput.inputs["Surface"])


def getNodeTree(sceneName):
    scene = getScene(sceneName)
    nodeTree = scene.world.node_tree
    return nodeTree


def deleteNodes(sceneName):
    nodes = getNodeTree(sceneName).nodes
    nodes.clear()


def createNodes(sceneName, type):
    nodes = getNodeTree(sceneName).nodes.new(type=type)
    return nodes


def setBackgroundLocation(sceneName, x, y):
    getNodeTree(sceneName).nodes.get('Environment Texture').location = x, y


def getScene(sceneName):

    blenderScene = bpy.data.scenes.get(sceneName or "Scene")

    assert \
        blenderScene != None, \
        f"Scene{sceneName} does not exists"

    return blenderScene
