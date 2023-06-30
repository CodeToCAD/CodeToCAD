# Actions wrap Blender's API to perform a single action.
# An implementation of an action should avoid performing any logic
# An implementation of an action is allowed to perform unit conversions or perform read operations for pre-checks.

from typing import Any, Optional, Union
from uuid import uuid4
import bpy
from CodeToCAD import Dimension
from CodeToCAD.CodeToCADInterface import AngleOrItsFloatOrStringValue, DimensionOrItsFloatOrStringValue
import CodeToCAD.utilities as Utilities
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
    blenderModifier = blenderObject.modifiers.new(
        type=modifier.name,
        name=modifier.name
    )

    # Apply every parameter passed in for modifier:
    for key, value in keywordArguments.items():
        setattr(blenderModifier, key, value)


def applyBevelModifier(
    entityName: str,
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
    entityName: str,
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
    entityName: str,
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
    entityName: str,
    thickness: Utilities.Dimension,
    keywordArguments: dict = {}
):

    applyModifier(
        entityName,
        BlenderDefinitions.BlenderModifiers.SOLIDIFY,
        dict(
            {
                "thickness": BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(thickness).value,
                "offset": 0
            },
            **keywordArguments
        )
    )


def applyCurveModifier(
    entityName: str,
    curveObjectName: str,
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
    meshObjectName: str,
    blenderBooleanType: BlenderDefinitions.BlenderBooleanTypes,
    withMeshObjectName: str,
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
                "use_self": True,
                "use_hole_tolerant": True,
                # "solver": "EXACT",
                # "double_threshold": 1e-6
            },
            **(keywordArguments or {})
        )
    )


def applyMirrorModifier(
    entityName: str,
    mirrorAcrossEntityName: str,
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
    entityName: str,
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

    assert primitiveType is not None, f"Primitive type is required."

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
        addon is not None, \
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
) -> str:

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
    fileType = fileType or Utilities.getFileExtension(filePath)

    assert \
        fileType in fileImportFunctions, \
        f"File type {fileType} is not supported"

    # Import the file:
    isSuccess = fileImportFunctions[fileType](filePath) == {'FINISHED'}

    assert isSuccess == True, \
        f"Could not import {filePath}"

    # Assume the imported file is 1 part and it's the last added object. Lots of wrong assumptions here.
    return bpy.data.objects[-1].name


# MARK: Transformations

def applyObjectTransformations(objectName):
    # Apply the object's transformations (under Object Properties tab)
    # This is different from applyDependencyGraph()
    # references https://blender.stackexchange.com/a/159540/138679

    blenderObject = getObject(objectName)

    assert blenderObject.data is not None, \
        f"Object {objectName} does not have data to transform."

    finalPose = blenderObject.matrix_basis

    mesh: bpy.types.Mesh = blenderObject.data  # type: ignore
    mesh.transform(finalPose)

    blenderObjectChildren: list[bpy.types.Object] = \
        blenderObject.children  # type: ignore

    for child in blenderObjectChildren:
        child.matrix_local = finalPose @ child.matrix_local  # type: ignore

    # Reset the object's transformations (resets everything in side menu to 0's)
    blenderObject.matrix_basis.identity()  # type: ignore


def applyObjectRotationAndScale(objectName):
    # references https://blender.stackexchange.com/a/159540/138679
    blenderObject = getObject(objectName)

    assert blenderObject.data is not None, \
        f"Object {objectName} does not have data to transform."

    decomposedMatrix: list[Any] = \
        blenderObject.matrix_basis.decompose()  # type: ignore
    translationVector: mathutils.Vector = decomposedMatrix[0]
    rotationQuat: mathutils.Quaternion = decomposedMatrix[1]
    scaleVector: mathutils.Vector = decomposedMatrix[2]

    translation: mathutils.Matrix = mathutils.Matrix.Translation(
        translationVector)
    rotation: mathutils.Matrix = rotationQuat.to_matrix().to_4x4()
    scale: mathutils.Matrix = mathutils.Matrix.Diagonal(scaleVector).to_4x4()

    transformation: mathutils.Matrix = rotation @ scale  # type: ignore

    mesh: bpy.types.Mesh = blenderObject.data  # type: ignore
    mesh.transform(transformation)

    # Set the object to its world translation
    blenderObject.matrix_basis = translation

    for child in blenderObject.children:  # type: ignore
        child.matrix_basis = transformation @ child.matrix_basis
        child.matrix_basis = mathutils.Matrix.Translation(
            child.matrix_basis.translation)


def rotateObject(
    objectName: str,
    rotationAngles: list[Optional[Utilities.Angle]],
    rotationType: BlenderDefinitions.BlenderRotationTypes
):

    blenderObject = getObject(objectName)

    currentRotation = getattr(blenderObject, rotationType.value)

    outputRotation = []

    for index in range(len(currentRotation)):
        angle = currentRotation[index]
        newAngle = rotationAngles[index]
        if newAngle is not None:
            angle = newAngle.toRadians().value
        outputRotation.append(angle)

    setattr(blenderObject, rotationType.value, outputRotation)


def translateObject(
    objectName: str,
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
        if newLocation is not None:
            location = newLocation.value
        outputLocation.append(location)

    setattr(blenderObject, translationType.value, outputLocation)


def setObjectLocation(
    objectName: str,
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
        if newLocation is not None:
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

    currentScale: mathutils.Vector = blenderObject.scale  # type: ignore

    blenderObject.scale = (xScaleFactor or currentScale.x,
                           yScaleFactor or currentScale.y, zScaleFactor or currentScale.z)


# MARK: collections and groups:

def createCollection(
    name: str,
    sceneName="Scene"
):

    assert \
        bpy.data.collections.get(name) == None, \
        f"Collection {name} already exists"

    assert \
        sceneName in bpy.data.scenes, f"Scene {sceneName} does not exist"  # type: ignore

    collection = bpy.data.collections.new(name)

    bpy.data.scenes[sceneName].collection.children.link(collection)


def removeCollection(
    name: str,
    removeChildren
):

    assert \
        bpy.data.collections.get(name) == None, \
        f"Collection {name} does not exist"

    if removeChildren:
        for obj in bpy.data.collections[name].objects:
            try:
                removeObject(obj.name, True)
            except Exception as e:
                pass

    bpy.data.collections.remove(bpy.data.collections[name])


def removeObjectFromCollection(
    existingObjectName: str,
    collectionName: str
):

    blenderObject = getObject(existingObjectName)

    collection = bpy.data.collections.get(collectionName)

    assert \
        collection is not None, \
        f"Collection {collectionName} does not exist"

    assert \
        existingObjectName in collection.objects, \
        f"Object {existingObjectName} does not exist in collection {collectionName}"

    collection.objects.unlink(blenderObject)


def assignObjectToCollection(
    existingObjectName: str,
    collectionName="Scene Collection",
    sceneName="Scene",
    removeFromOtherGroups=True,
    moveChildren=True
):

    blenderObject = getObject(existingObjectName)

    collection = bpy.data.collections.get(collectionName)

    if collection == None and collectionName == "Scene Collection":
        scene = bpy.data.scenes.get(sceneName)

        assert \
            scene is not None, \
            f"Scene {sceneName} does not exist"

        collection = scene.collection

    assert \
        collection is not None, \
        f"Collection {collectionName} does not exist"

    if removeFromOtherGroups:
        currentCollections: list[bpy.types.Collection] = \
            blenderObject.users_collection  # type: ignore
        for currentCollection in currentCollections:
            currentCollection.objects.unlink(blenderObject)

    collection.objects.link(blenderObject)

    if moveChildren:
        for child in blenderObject.children:  # type: ignore
            assignObjectToCollection(
                child.name, collectionName, sceneName, True, True)


# MARK: Joints
def getConstraint(objectName: str, constraintName) -> Optional[bpy.types.Constraint]:
    blenderObject = getObject(objectName)
    return blenderObject.constraints.get(constraintName)


def applyConstraint(
    objectName: str,
    constraintType: BlenderDefinitions.BlenderConstraintTypes,
    keywordArguments={}
):

    blenderObject = getObject(objectName)

    constraintName = keywordArguments.get(
        "name") or constraintType.getDefaultBlenderName()

    constraint = getConstraint(objectName, constraintName)

    # If it doesn't exist, create it:
    if constraint is None:
        constraint = blenderObject.constraints.new(constraintType.name)

    # Apply every parameter passed in for modifier:
    for key, value in keywordArguments.items():
        setattr(constraint, key, value)


def applyLimitLocationConstraint(
    objectName: str,
    x: Optional[list[Optional[Utilities.Dimension]]],
    y: Optional[list[Optional[Utilities.Dimension]]],
    z: Optional[list[Optional[Utilities.Dimension]]],
    relativeToObjectName: Optional[str],
    keywordArguments={}
):

    relativeToObject = getObject(
        relativeToObjectName) if relativeToObjectName else None

    [minX, maxX] = x or [None, None]
    [minY, maxY] = y or [None, None]
    [minZ, maxZ] = z or [None, None]

    keywordArguments = keywordArguments or {}

    keywordArguments["name"] = BlenderDefinitions.BlenderConstraintTypes.LIMIT_LOCATION.formatConstraintName(
        objectName, relativeToObject)

    keywordArguments["owner_space"] = "CUSTOM" if relativeToObject else "WORLD"

    keywordArguments["space_object"] = relativeToObject

    keywordArguments["use_transform_limit"] = True

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
    objectName: str,
    x: Optional[list[Optional[Utilities.Angle]]],
    y:  Optional[list[Optional[Utilities.Angle]]],
    z:  Optional[list[Optional[Utilities.Angle]]],
    relativeToObjectName: Optional[str],
    keywordArguments={}
):

    relativeToObject = getObject(
        relativeToObjectName) if relativeToObjectName else None

    [minX, maxX] = x or [None, None]
    [minY, maxY] = y or [None, None]
    [minZ, maxZ] = z or [None, None]

    keywordArguments = keywordArguments or {}

    keywordArguments["name"] = BlenderDefinitions.BlenderConstraintTypes.LIMIT_ROTATION.formatConstraintName(
        objectName, relativeToObject)

    keywordArguments["owner_space"] = "CUSTOM" if relativeToObject else "WORLD"

    keywordArguments["space_object"] = relativeToObject

    keywordArguments["use_transform_limit"] = True

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


def applyCopyLocationConstraint(
    objectName: str,
    copiedObjectName: str,
    copyX: bool,
    copyY: bool,
    copyZ: bool,
    useOffset: bool,
    keywordArguments={}
):

    copiedObject = getObject(copiedObjectName)

    applyConstraint(
        objectName,
        BlenderDefinitions.BlenderConstraintTypes.COPY_LOCATION,
        dict(
            {
                "name": BlenderDefinitions.BlenderConstraintTypes.COPY_LOCATION.formatConstraintName(objectName, copiedObjectName),
                "target": copiedObject,
                "use_x": copyX,
                "use_y": copyY,
                "use_z": copyZ,
                "use_offset": useOffset
            },
            **keywordArguments
        )
    )


def applyCopyRotationConstraint(
    objectName: str,
    copiedObjectName: str,
    copyX: bool,
    copyY: bool,
    copyZ: bool,
    keywordArguments={}
):

    copiedObject = getObject(copiedObjectName)

    applyConstraint(
        objectName,
        BlenderDefinitions.BlenderConstraintTypes.COPY_ROTATION,
        dict(
            {
                "name": BlenderDefinitions.BlenderConstraintTypes.COPY_ROTATION.formatConstraintName(objectName, copiedObjectName),
                "target": copiedObject,
                "use_x": copyX,
                "use_y": copyY,
                "use_z": copyZ,
                "mix_mode": "BEFORE"
            },
            **keywordArguments
        )
    )


def applyPivotConstraint(
    objectName: str,
    pivotObjectName: str,
    keywordArguments={}
):

    pivotObject = getObject(pivotObjectName)

    applyConstraint(
        objectName,
        BlenderDefinitions.BlenderConstraintTypes.PIVOT,
        dict(
            {
                "name": BlenderDefinitions.BlenderConstraintTypes.PIVOT.formatConstraintName(objectName, pivotObjectName),
                "target": pivotObject,
                "rotation_range": "ALWAYS_ACTIVE"
            },
            **keywordArguments
        )
    )


def applyGearConstraint(
    objectName: str,
    gearObjectName: str,
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
    objectName: str,
    path: str,
    index=-1
):

    blenderObject = getObject(objectName)

    return blenderObject.driver_add(path, index).driver


def removeDriver(
    objectName: str,
    path: str,
    index=-1
):

    blenderObject = getObject(objectName)

    blenderObject.driver_remove(path, index)


def getDriver(
    objectName: str,
    path: str,
):
    blenderObject = getObject(objectName)

    # this returns an FCurve object
    # https://docs.blender.org/api/current/bpy.types.FCurve.html
    fcurve = blenderObject.animation_data.drivers.find(path)

    assert fcurve is not None, f"Could not find driver {path} for object {objectName}."

    return fcurve.driver


def setDriver(
    driver: bpy.types.Driver,
    driverType,  # : BlenderDefinitions.BlenderDriverTypes,
    expression=""
):

    driver.type = driverType

    driver.expression = expression if expression else ""


def setDriverVariableSingleProp(
    driver: bpy.types.Driver,
    variableName: str,
    targetObjectName: str,
    targetDataPath: str,
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
    driver: bpy.types.Driver,
    variableName: str,
    targetObjectName: str,
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
    driver: bpy.types.Driver,
    variableName: str,
    target1ObjectName: str,
    target2ObjectName: str,
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
    driver: bpy.types.Driver,
    variableName: str,
    target1ObjectName: str,
    target2ObjectName: str,
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
    objectToTranslateName: str,
    object1LandmarkName: str,
    object2LandmarkName: str,
):

    updateViewLayer()
    object1LandmarkLocation = getObjectWorldLocation(object1LandmarkName)
    object2LandmarkLocation = getObjectWorldLocation(object2LandmarkName)

    translation = (object1LandmarkLocation)-(object2LandmarkLocation)

    blenderDefaultUnit = BlenderDefinitions.BlenderLength.DEFAULT_BLENDER_UNIT.value

    translateObject(
        objectToTranslateName,
        [
            Utilities.Dimension(translation.x.value, blenderDefaultUnit),
            Utilities.Dimension(translation.y.value, blenderDefaultUnit),
            Utilities.Dimension(translation.z.value, blenderDefaultUnit)
        ],  # type: ignore
        BlenderDefinitions.BlenderTranslationTypes.ABSOLUTE
    )

# MARK: creating and manipulating objects


def makeParent(
    name: str,
    parentName: str,
):

    blenderObject = getObject(name)
    blenderParentObject = getObject(parentName)

    blenderObject.parent = blenderParentObject


def updateObjectName(
    oldName: str,
    newName: str,
):

    blenderObject = getObject(oldName)

    blenderObject.name = newName


def getObjectCollectionName(objectName: str,) -> str:

    blenderObject = getObject(objectName)

    # Assumes the first collection is the main collection
    [currentCollection] = \
        blenderObject.users_collection  # type: ignore

    return currentCollection.name


def updateObjectDataName(
    parentObjectName: str,
    newName: str,
):

    blenderObject = getObject(parentObjectName)

    assert blenderObject.data is not None, f"Object {parentObjectName} does not have data to name."

    blenderObject.data.name = newName


# This assumes that landmarks are named with format: `{parentPartName}_{landmarkName}`
def updateObjectLandmarkNames(
    parentObjectName: str,
    oldNamePrefix: str,
    newNamePrefix: str,
):

    blenderObject = getObject(parentObjectName)

    blenderObjectChildren: list[bpy.types.Object] = \
        blenderObject.children  # type: ignore

    for child in blenderObjectChildren:
        if f"{oldNamePrefix}_" in child.name and child.type == "EMPTY":
            updateObjectName(child.name, child.name.replace(
                f"{oldNamePrefix}_", f"{newNamePrefix}_"))


def removeObject(
    existingObjectName: str,
    removeChildren=False
):

    blenderObject = getObject(existingObjectName)

    if removeChildren:
        blenderObjectChildren: list[bpy.types.Object] = \
            blenderObject.children  # type: ignore
        for child in blenderObjectChildren:
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
    name: str,
    data: Optional[Any] = None
):

    blenderObject = bpy.data.objects.get(name)

    assert \
        blenderObject == None, \
        f"Object {name} already exists"

    return bpy.data.objects.new(name, data)


def createObjectVertexGroup(
        objectName: str,
        vertexGroupName: str,
):
    blenderObject = getObject(objectName)
    return blenderObject.vertex_groups.new(name=vertexGroupName)


def getObjectVertexGroup(
    objectName: str,
    vertexGroupName: str,
):
    blenderObject = getObject(objectName)
    return blenderObject.vertex_groups.get(vertexGroupName)


def addVerticiesToVertexGroup(
        vertexGroupObject,
        vertexIndecies: list[int]
):
    vertexGroupObject.add(vertexIndecies, 1.0, 'ADD')


def createMeshFromCurve(
    existingCurveObjectName: str,
    newObjectName: Optional[str] = None
):

    existingCurveObject = getObject(existingCurveObjectName)

    if newObjectName is None:
        updateObjectName(existingCurveObjectName, str(uuid4()))
        newObjectName = existingCurveObjectName

    dependencyGraph = bpy.context.evaluated_depsgraph_get()
    evaluatedObject: bpy.types.Object = existingCurveObject.evaluated_get(
        dependencyGraph)  # type: ignore
    mesh: bpy.types.Mesh = bpy.data.meshes.new_from_object(
        evaluatedObject,  depsgraph=dependencyGraph)

    blenderObject = createObject(newObjectName, mesh)

    blenderObject.matrix_world = existingCurveObject.matrix_world

    assignObjectToCollection(newObjectName)

    existingCurveObjectChildren: list[bpy.types.Object] = \
        existingCurveObject.children  # type: ignore
    for child in existingCurveObjectChildren:
        if type(child) == BlenderDefinitions.BlenderTypes.OBJECT.value and child.type == 'EMPTY':
            child.parent = blenderObject

    # twisted logic here, but if we renamed this above, we want to nuke it because we're done with it.
    if existingCurveObject.name != existingCurveObjectName:
        removeObject(existingCurveObject.name, removeChildren=True)


def getObjectVisibility(
    existingObjectName: str,
) -> bool:

    blenderObject = getObject(existingObjectName)

    return blenderObject.visible_get()


def setObjectVisibility(
    existingObjectName: str,
    isVisible: bool
):

    blenderObject = getObject(existingObjectName)

    # blenderObject.hide_viewport = not isVisible
    # blenderObject.hide_render = not isVisible
    blenderObject.hide_set(not isVisible)


def transferLandmarks(
    fromObjectName: str,
    toObjectName: str,
):

    updateViewLayer()

    fromBlenderObject = getObject(fromObjectName)
    toBlenderObject = getObject(toObjectName)

    translation = (getObjectWorldLocation(
        fromObjectName) - getObjectWorldLocation(toObjectName)).toList()

    translation = [
        axisValue.value for axisValue in BlenderDefinitions.BlenderLength.convertDimensionsToBlenderUnit(translation)]

    defaultCollection = getObjectCollectionName(toObjectName)

    fromBlenderObjectChildren: list[bpy.types.Object] = \
        fromBlenderObject.children  # type: ignore
    for child in fromBlenderObjectChildren:
        if type(child) == BlenderDefinitions.BlenderTypes.OBJECT.value and child.type == 'EMPTY':
            child.name = f"{toObjectName}_{child.name}"
            isAlreadyExists = bpy.data.objects.get(child.name) == None
            if isAlreadyExists:
                print(f"{child.name} already exists. Skipping landmark transfer.")
                continue
            child.parent = toBlenderObject
            child.location = child.location + \
                mathutils.Vector(translation)  # type: ignore
            assignObjectToCollection(child.name, defaultCollection)


def duplicateObject(
    existingObjectName: str,
    newObjectName: str,
    copyLandmarks: bool = True
):

    clonedObject = bpy.data.objects.get(newObjectName)  # type: ignore

    assert clonedObject == None, \
        f"Object with name {newObjectName} already exists."

    blenderObject = getObject(existingObjectName)

    clonedObject: bpy.types.Object = blenderObject.copy()  # type: ignore
    clonedObject.name = newObjectName
    clonedObject.data = blenderObject.data.copy()
    clonedObject.data.name = newObjectName

    # Link clonedObject to the original object's collection.
    defaultCollection = getObjectCollectionName(existingObjectName)

    assignObjectToCollection(newObjectName, defaultCollection)

    if copyLandmarks:
        blenderObjectChildren: list[bpy.types.Object] = \
            blenderObject.children  # type: ignore
        for child in blenderObjectChildren:
            if type(child) == BlenderDefinitions.BlenderTypes.OBJECT.value and child.type == 'EMPTY':
                newChild: bpy.types.Object = child.copy()  # type: ignore
                newChild.name = child.name.replace(
                    existingObjectName, newObjectName)
                newChild.parent = clonedObject
                assignObjectToCollection(newChild.name, defaultCollection)


def updateViewLayer():
    bpy.context.view_layer.update()


def getObjectLocalLocation(objectName: str,):

    blenderObject = getObject(objectName)

    return Utilities.Point.fromList([Utilities.Dimension(p,  BlenderDefinitions.BlenderLength.DEFAULT_BLENDER_UNIT.value) for p in blenderObject.location])


def getObjectWorldLocation(objectName: str,):

    blenderObject = getObject(objectName)

    return Utilities.Point.fromList(
        [
            Utilities.Dimension(
                p,  BlenderDefinitions.BlenderLength.DEFAULT_BLENDER_UNIT.value)
            for p in
            blenderObject.matrix_world.translation  # type: ignore
        ]
    )


def getObjectWorldPose(objectName: str,) -> list[float]:

    blenderObject = getObject(objectName)

    listOfTuples = [v.to_tuple() for v in list(
        blenderObject.matrix_world)]  # type: ignore

    return [value for values in listOfTuples for value in values]


def getObject(objectName: str,) -> bpy.types.Object:

    blenderObject = bpy.data.objects.get(objectName)

    assert \
        blenderObject is not None, \
        f"Object {objectName} does not exists"

    return blenderObject


def getMesh(meshName: str,) -> bpy.types.Mesh:

    blenderMesh = bpy.data.meshes.get(meshName)

    assert \
        blenderMesh is not None, \
        f"Mesh {meshName} does not exists"

    return blenderMesh


# Applies the dependency graph to the object and persists its data using .copy()
# This allows us to apply modifiers, UV data, etc.. to the mesh.
# This is different from applyObjectTransformations()
def applyDependencyGraph(
    existingObjectName: str,
):

    blenderObject = getObject(existingObjectName)
    blenderObjectEvaluated: bpy.types.Object = blenderObject.evaluated_get(
        bpy.context.evaluated_depsgraph_get()
    )  # type: ignore
    blenderObject.data = blenderObjectEvaluated.data.copy()


def clearModifiers(objectName: str,):

    blenderObject = getObject(objectName)

    blenderObject.modifiers.clear()


def removeMesh(meshNameOrInstance: Union[str, bpy.types.Mesh],):

    mesh: bpy.types.Mesh = meshNameOrInstance  # type: ignore
    # if a (str) name is passed in, fetch the mesh object reference
    if isinstance(meshNameOrInstance, str):
        mesh = getMesh(meshNameOrInstance)

    bpy.data.meshes.remove(mesh)


def setEdgesMeanCrease(meshName: str, meanCreaseValue: float):

    blenderMesh = getMesh(meshName)

    for edge in blenderMesh.edges:
        edge.crease = meanCreaseValue


# Note: transformations have to be applied for this to be reliable.
def isCollisionBetweenTwoObjects(
        object1Name: str,
        object2Name: str,
):
    blenderObject1 = getObject(object1Name)
    blenderObject2 = getObject(object2Name)

    dependencyGraph = bpy.context.evaluated_depsgraph_get()

    bvhTreeObject1 = BVHTree.FromObject(blenderObject1, dependencyGraph)
    bvhTreeObject2 = BVHTree.FromObject(blenderObject2, dependencyGraph)

    uniqueIndecies = bvhTreeObject1.overlap(bvhTreeObject2)  # type: ignore

    return len(uniqueIndecies) > 0


# References https://docs.blender.org/api/current/mathutils.kdtree.html
def createKdTreeForObject(objectName: str,):
    blenderObject = getObject(objectName)
    mesh: bpy.types.Mesh = blenderObject.data  # type: ignore
    size = len(mesh.vertices)
    kd = KDTree(size)

    for i, v in enumerate(mesh.vertices):
        kd.insert(v.co, i)

    kd.balance()
    return kd


# uses object.closest_point_on_mesh https://docs.blender.org/api/current/bpy.types.Object.html#bpy.types.Object.closest_point_on_mesh
def getClosestFaceToVertex(objectName: str, vertex) -> bpy.types.MeshPolygon:

    blenderObject = getObject(objectName)

    assert \
        len(vertex) == 3, \
        "Vertex is not length 3. Please provide a proper vertex (x,y,z)"

    matrixWorld: mathutils.Matrix = blenderObject.matrix_world  # type: ignore
    invertedMatrixWorld = matrixWorld.inverted()

    # vertex in object space:
    vertexInverted = invertedMatrixWorld @ mathutils.Vector(vertex)

    # polygonIndex references an index at blenderObject.data.polygons[polygonIndex], in other words, the face or edge data
    [isFound, closestPoint, normal,
        polygonIndex] = blenderObject.closest_point_on_mesh(vertexInverted)  # type: ignore

    assert \
        isFound, \
        f"Could not find a point close to {vertex} on {objectName}"

    assert \
        polygonIndex is not None and polygonIndex != -1, \
        f"Could not find a face near {vertex} on {objectName}"

    mesh: bpy.types.Mesh = blenderObject.data  # type: ignore
    blenderPolygon = mesh.polygons[polygonIndex]

    return blenderPolygon


# Returns a list of (co, index, dist)
def getClosestPointsToVertex(objectName: str, vertex, numberOfPoints=2, objectKdTree=None):

    blenderObject = getObject(objectName)

    kdTree = objectKdTree or createKdTreeForObject(objectName)

    assert \
        len(vertex) == 3, \
        "Vertex is not length 3. Please provide a proper vertex (x,y,z)"

    matrixWorld: mathutils.Matrix = blenderObject.matrix_world  # type: ignore
    invertedMatrixWorld = matrixWorld.inverted()

    vertexInverted: mathutils.Vector = \
        invertedMatrixWorld @ mathutils.Vector(vertex)  # type: ignore

    return kdTree.find_n(vertexInverted, numberOfPoints)


# References https://blender.stackexchange.com/a/32288/138679
def getBoundingBox(objectName: str,):

    updateViewLayer()

    blenderObject = getObject(objectName)

    local_coords = blenderObject.bound_box[:]

    # om = blenderObject.matrix_world
    om = blenderObject.matrix_basis

    # matrix multiple world transform by all the vertices in the boundary
    coords = [
        (
            om @ mathutils.
            Vector(p[:])  # type: ignore
        ).to_tuple()
        for p in local_coords
    ]
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

def addonSetEnabled(addonName: str, isEnabled: bool):
    preferences = bpy.ops.preferences

    command = preferences.addon_enable if isEnabled else preferences.addon_disable

    command(module=addonName)


# MARK: Curves and Sketches

def extrude(
    curveObjectName: str,
    length: Utilities.Dimension
):

    blenderObject = getObject(curveObjectName)

    length = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
        length)

    assert type(blenderObject.data) == BlenderDefinitions.BlenderTypes.CURVE.value or type(blenderObject.data) == BlenderDefinitions.BlenderTypes.TEXT.value,\
        f"Object {curveObjectName} is not a curve or text object type."

    blenderObject.data.extrude = length.value


def createText(curveName: str, text: str,
               size=Utilities.Dimension(1),
               bold=False,
               italic=False,
               underlined=False,
               characterSpacing=1,
               wordSpacing=1,
               lineSpacing=1,
               fontFilePath: Optional[str] = None):

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
            curveDataBodyFormat[index].use_italic = italic

        # setattr(curveData, "body_format", curveDataBodyFormat)

    createObject(curveName, curveData)

    assignObjectToCollection(curveName)


def create3DCurve(
    curveName: str,
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
    blenderCurve: bpy.types.Curve,
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
    pathCurveObjectName: str,
    profileCurveObjectName: str,
    fillCap=False
):

    pathCurveObject = getObject(pathCurveObjectName)

    profileCurveObject = getObject(profileCurveObjectName)

    assert \
        type(profileCurveObject.data) == bpy.types.Curve, \
        f"Profile Object {profileCurveObjectName} is not a Curve object. Please use a Curve object."

    curve: bpy.types.Curve = pathCurveObject.data  # type: ignore

    curve.bevel_mode = "OBJECT"
    curve.bevel_object = profileCurveObject
    curve.use_fill_caps = fillCap


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
    elif curvePrimitive == BlenderDefinitions.BlenderCurvePrimitiveTypes.Spiral:
        return BlenderCurvePrimitives.createSpiral

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

    @staticmethod
    def createSpiral(numberOfTurns: 'int', height: DimensionOrItsFloatOrStringValue, radius: DimensionOrItsFloatOrStringValue, isClockwise: bool = True, radiusEnd: Optional[DimensionOrItsFloatOrStringValue] = None, keywordArguments={}):
        enableCurveExtraObjectsAddon()

        heightMeters = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
            Dimension.fromString(height)).value

        radiusMeters = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
            Dimension.fromString(radius)).value

        radiusEndMeters = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
            Dimension.fromString(radiusEnd)) if radiusEnd else None

        radiusDiff = 0 if radiusEndMeters is None else (
            radiusEndMeters - radiusMeters).value

        curveType: BlenderDefinitions.BlenderCurveTypes = keywordArguments[
            "curveType"] if "curveType" in keywordArguments and keywordArguments["curveType"] else BlenderDefinitions.BlenderCurvePrimitiveTypes.Spiral.getDefaultCurveType()

        curveTypeName: str = curveType.name

        bpy.ops.curve.spirals(spiral_type='ARCH',  # type: ignore
                              turns=numberOfTurns, steps=24, edit_mode=False,
                              radius=radiusMeters,
                              dif_z=heightMeters/numberOfTurns, dif_radius=radiusDiff, curve_type=curveTypeName,
                              spiral_direction='CLOCKWISE' if isClockwise else 'COUNTER_CLOCKWISE'
                              )


def enableCurveExtraObjectsAddon():
    addonName = "add_curve_extra_objects"

    # check if the addon is enabled, enable it if it is not.
    addon = bpy.context.preferences.addons.get(addonName)
    if addon == None:
        addonSetEnabled(addonName, True)
        addon = bpy.context.preferences.addons.get(addonName)

    assert \
        addon is not None, \
        f"Could not enable the {addonName} addon to create simple curves"


# assumes add_curve_extra_objects is enabled
# https://github.com/blender/blender-addons/blob/master/add_curve_extra_objects/add_curve_simple.py
def createSimpleCurve(curvePrimitiveType: BlenderDefinitions.BlenderCurvePrimitiveTypes, keywordArguments={}):

    curveType: BlenderDefinitions.BlenderCurveTypes = keywordArguments[
        "curveType"] if "curveType" in keywordArguments and keywordArguments["curveType"] else curvePrimitiveType.getDefaultCurveType()

    keywordArguments.pop("curveType", None)  # remove curveType from kwargs

    enableCurveExtraObjectsAddon()

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


def setCurveUsePath(curveName: str, isUsePath: bool):
    curveObject = getObject(curveName)

    curve: bpy.types.Curve = curveObject.data  # type: ignore

    curve.use_path = isUsePath

# MARK: manipulating the Scene

# locks the scene interface


def sceneLockInterface(isLocked: bool):
    bpy.context.scene.render.use_lock_interface = isLocked


def setDefaultUnit(
    blenderUnit: BlenderDefinitions.BlenderLength,
    sceneName="Scene"
):

    blenderScene = bpy.data.scenes.get(sceneName)

    assert \
        blenderScene is not None, \
        f"Scene {sceneName} does not exist"

    blenderScene.unit_settings.system = blenderUnit.getSystem()
    blenderScene.unit_settings.length_unit = blenderUnit.name


def selectObject(objectName: str):
    blenderObject = getObject(objectName)

    blenderObject.select_set(True)


def getSelectedObjectName() -> str:

    selectedObjects = bpy.context.selected_objects

    assert len(selectedObjects) > 0, "There are no selected objects."

    return selectedObjects[0].name


def getContextView3D():
    window = bpy.context.window_manager.windows[0]
    for area in window.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    return bpy.context.temp_override(window=window, area=area, region=region)
    raise Exception("Could not find a VIEW_3D region.")


def zoomToSelectedObjects():
    bpy.context.view_layer.update()
    # References https://blender.stackexchange.com/a/7419/138679
    with getContextView3D():
        bpy.ops.view3d.view_selected(use_all_regions=True)
        return


def addDependencyGraphUpdateListener(callback):
    bpy.app.handlers.depsgraph_update_post.append(callback)  # type: ignore


def addTimer(callback):
    bpy.app.timers.register(callback)


def getMaterial(materialName: str,) -> bpy.types.Material:
    blenderMaterial = bpy.data.materials.get(materialName)

    assert \
        blenderMaterial is not None, \
        f"Material {materialName} does not exist."

    return blenderMaterial


def createMaterial(newMaterialName: str,):
    material = bpy.data.materials.get(newMaterialName)

    assert \
        material == None, \
        f"Material with name {material} already exists."

    material = bpy.data.materials.new(name=newMaterialName)

    return material


def setMaterialColor(materialName: str, rValue, gValue, bValue, aValue=1.0):
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


def setMaterialMetallicness(materialName: str, value: float):

    material = getMaterial(materialName)
    material.metallic = value


def setMaterialRoughness(materialName: str, value: float):

    material = getMaterial(materialName)
    material.roughness = value


def setMaterialSpecularness(materialName: str, value: float):

    material = getMaterial(materialName)
    material.specular_intensity = value


def setMaterialToObject(materialName: str, objectName: str,):

    material = getMaterial(materialName)

    object = getObject(objectName)

    mesh: bpy.types.Mesh = object.data  # type: ignore

    objectMaterial = mesh.materials

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
    objectName: str,
    filePath: str,
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


def setFrameStart(frameNumber: int, sceneName: Optional[str]):
    scene = getScene(sceneName)
    scene.frame_start = frameNumber


def setFrameEnd(frameNumber: int, sceneName: Optional[str]):
    scene = getScene(sceneName)
    scene.frame_end = frameNumber


def setFrameStep(step: int, sceneName: Optional[str]):
    scene = getScene(sceneName)
    scene.frame_step = step


def setFrameCurrent(frameNumber: int, sceneName: Optional[str]):
    scene = getScene(sceneName)
    scene.frame_set(frameNumber)


# def getTexture(textureName):
# 	blenderTexture = bpy.data.textures.get(textureName)

# 	assert \
# 		blenderTexture is not None, \
# 			f"Texture {textureName} does not exist."

# 	return blenderTexture


# def createImageTexture(textureName, imageFilePath, repeatMode:BlenderDefinitions.RepeatMode):
#   image = bpy.data.images.load(imageFilePath)
#   blenderTexture = bpy.data.textures.new(name=textureName, type="IMAGE")
#   blenderTexture.image = image
#   blenderTexture.extension = repeatMode.getBlenderName

# ref https://blender.stackexchange.com/questions/118646/add-a-texture-to-an-object-using-python-and-blender-2-8/129014#129014

def addTextureToMaterial(materialName: str, imageFilePath: str,):
    material = getMaterial(materialName)
    material.use_nodes = True
    bsdf = material.node_tree.nodes["Principled BSDF"]
    texImage: bpy.types.ShaderNodeTexImage = material.node_tree.nodes.new(
        'ShaderNodeTexImage')  # type: ignore
    image = bpy.data.images.load(imageFilePath)
    texImage.image = image
    material.node_tree.links.new(
        bsdf.inputs['Base Color'], texImage.outputs['Color'])


def logMessage(message: str,):
    bpy.ops.code_to_cad.log_message(message=message)  # type: ignore


def createLight(objName: str, energyLevel, type):
    light_data = bpy.data.lights.new(name=objName, type=type)
    setattr(light_data, "energy", energyLevel)
    createObject(objName, data=light_data)
    assignObjectToCollection(objName)


def getLight(lightName: str,):
    blenderLight = bpy.data.lights.get(lightName)

    assert \
        blenderLight is not None, \
        f"Light {lightName} does not exist."

    return blenderLight


def setLightColor(lightName: str, rValue, gValue, bValue):
    if type(rValue) == int:
        rValue /= 255.0

    if type(gValue) == int:
        gValue /= 255.0

    if type(bValue) == int:
        bValue /= 255.0

    light = getLight(lightName)

    light.color = (rValue, gValue, bValue)

    return light


def createCamera(objName: str, type):
    camera_data = bpy.data.cameras.new(name=objName)
    createObject(objName, data=camera_data)
    assignObjectToCollection(objName)


def getCamera(cameraName: str,):
    blenderCamera = bpy.data.cameras.get(cameraName)

    assert \
        blenderCamera is not None, \
        f"Camera {cameraName} does not exist."

    return blenderCamera


def setSceneCamera(cameraName: str, sceneName: Optional[str] = None):
    blenderCamera = getObject(cameraName)
    scene = getScene(sceneName)

    scene.camera = blenderCamera


def setFocalLength(cameraName: str, length=50.0):
    camera = getCamera(cameraName)
    assert \
        length >= 1, \
        "Length needs to be greater than or equal to 1."

    camera.lens = length


def addHDRTexture(sceneName: str, imageFilePath: str,):
    deleteNodes(sceneName)
    nodeBackground = createNodes(sceneName, 'ShaderNodeBackground')
    nodeEnvironment: bpy.types.ShaderNodeTexEnvironment = createNodes(
        sceneName, 'ShaderNodeTexEnvironment')  # type: ignore
    nodeEnvironment.image = bpy.data.images.load(imageFilePath)
    nodeEnvironment.location = 0, 0
    nodeOutput = createNodes(sceneName, 'ShaderNodeOutputWorld')
    nodeOutput.location = 0, 0
    links = getNodeTree(sceneName).links
    links.new(nodeEnvironment.outputs["Color"], nodeBackground.inputs["Color"])
    links.new(nodeBackground.outputs["Background"],
              nodeOutput.inputs["Surface"])


def getNodeTree(sceneName: str,) -> bpy.types.NodeTree:
    scene = getScene(sceneName)
    nodeTree = scene.world.node_tree
    return nodeTree


def deleteNodes(sceneName: str,):
    nodes = getNodeTree(sceneName).nodes
    nodes.clear()


def createNodes(sceneName: str, type) -> bpy.types.Node:
    nodes = getNodeTree(sceneName).nodes.new(type=type)
    return nodes


def setBackgroundLocation(sceneName: str, x, y):
    envTexture: bpy.types.ShaderNodeTexEnvironment = getNodeTree(
        sceneName).nodes.get('Environment Texture')  # type: ignore
    envTexture.location = x, y


def getScene(sceneName: Optional[str] = "Scene") -> bpy.types.Scene:

    blenderScene = bpy.data.scenes.get(sceneName or "Scene")

    assert \
        blenderScene is not None, \
        f"Scene{sceneName} does not exists"

    return blenderScene


def renderImage(outputFilepath: str, overwrite: bool):
    bpy.context.scene.render.use_overwrite = overwrite
    bpy.context.scene.render.filepath = outputFilepath
    bpy.ops.render.render(write_still=True)


def renderAnimation(outputFilepath: str, overwrite: bool):
    bpy.context.scene.render.use_overwrite = overwrite
    bpy.context.scene.render.filepath = outputFilepath
    bpy.ops.render.render(animation=True)


def setRenderFrameRate(rate: int):
    bpy.context.scene.render.fps = rate


def setRenderQuality(percentage: int):
    bpy.context.scene.render.image_settings.quality = percentage


def setRenderFileFormat(format: BlenderDefinitions.FileFormat):
    bpy.context.scene.render.image_settings.file_format = format.name


def setRenderEngine(engine: BlenderDefinitions.RenderEngines):
    bpy.context.scene.render.engine = engine.name


def setRenderResolution(x: int, y: int):
    bpy.context.scene.render.resolution_x = x
    bpy.context.scene.render.resolution_y = y
