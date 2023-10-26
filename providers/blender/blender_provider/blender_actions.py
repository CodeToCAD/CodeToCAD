# Actions wrap Blender's API to perform a single action.
# An implementation of an action should avoid performing any logic
# An implementation of an action is allowed to perform unit conversions or perform read operations for pre-checks.

from typing import Any, Optional, Union
from uuid import uuid4
import bpy
import bmesh
from codetocad.codetocad_types import (
    AngleOrItsFloatOrStringValue,
    DimensionOrItsFloatOrStringValue,
)
from codetocad.core.angle import Angle
from codetocad.core.boundary_axis import BoundaryAxis
from codetocad.core.boundary_box import BoundaryBox
from codetocad.core.dimension import Dimension
from codetocad.core.point import Point
from codetocad.enums.axis import Axis
from codetocad.utilities import get_dimension_list_from_string_list, get_file_extension
from . import blender_definitions
from pathlib import Path
import mathutils
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree

# MARK: Modifiers


def apply_modifier(
    entity_name: str, modifier: blender_definitions.BlenderModifiers, **kwargs
):
    blenderObject = get_object(entity_name)

    # references https://docs.blender.org/api/current/bpy.types.BooleanModifier.html?highlight=boolean#bpy.types.BooleanModifier and https://docs.blender.org/api/current/bpy.types.ObjectModifiers.html#bpy.types.ObjectModifiers and https://docs.blender.org/api/current/bpy.types.Modifier.html#bpy.types.Modifier
    blenderModifier = blenderObject.modifiers.new(
        type=modifier.name, name=modifier.name
    )

    # blenderModifier.show_viewport = False

    # Apply every parameter passed in for modifier:
    for key, value in kwargs.items():
        setattr(blenderModifier, key, value)


def apply_decimate_modifier(entity_name: str, amount: int):
    apply_modifier(
        entity_name,
        blender_definitions.BlenderModifiers.DECIMATE,
        decimate_type="UNSUBDIV",
        iterations=amount,
    )


def apply_bevel_modifier(
    entity_name: str,
    radius: Dimension,
    vertex_group_name=None,
    use_edges=True,
    use_width=False,
    chamfer=False,
    **kwargs,
):
    apply_modifier(
        entity_name,
        blender_definitions.BlenderModifiers.BEVEL,
        affect="EDGES" if use_edges else "VERTICES",
        offset_type="WIDTH" if use_width else "OFFSET",
        width=radius.value,
        segments=1 if chamfer else 24,
        limit_method="VGROUP" if vertex_group_name else "ANGLE",
        vertex_group=vertex_group_name or "",
        **kwargs,
    )


def apply_linear_pattern(
    entity_name: str, instance_count, direction: Axis, offset: float, **kwargs
):
    offsetArray = [0.0, 0.0, 0.0]

    offsetArray[direction.value] = offset

    apply_modifier(
        entity_name,
        blender_definitions.BlenderModifiers.ARRAY,
        use_relative_offset=False,
        count=instance_count,
        use_constant_offset=True,
        constant_offset_displace=offsetArray,
        **kwargs,
    )


def apply_circular_pattern(
    entity_name: str, instance_count, around_object_name, **kwargs
):
    blenderObject = get_object(around_object_name)

    apply_modifier(
        entity_name,
        blender_definitions.BlenderModifiers.ARRAY,
        count=instance_count,
        use_relative_offset=False,
        use_object_offset=True,
        offset_object=blenderObject,
        **kwargs,
    )


def apply_solidify_modifier(entity_name: str, thickness: Dimension, **kwargs):
    apply_modifier(
        entity_name,
        blender_definitions.BlenderModifiers.SOLIDIFY,
        thickness=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
            thickness
        ).value,
        offset=0,
        **kwargs,
    )


def apply_curve_modifier(entity_name: str, curve_object_name: str, **kwargs):
    curveObject = get_object(curve_object_name)

    apply_modifier(
        entity_name,
        blender_definitions.BlenderModifiers.CURVE,
        object=curveObject,
        **kwargs,
    )


def apply_boolean_modifier(
    mesh_object_name: str,
    blender_boolean_type: blender_definitions.BlenderBooleanTypes,
    with_mesh_object_name: str,
    **kwargs,
):
    blenderObject = get_object(mesh_object_name)
    blenderBooleanObject = get_object(with_mesh_object_name)

    assert isinstance(
        blenderObject.data, blender_definitions.BlenderTypes.MESH.value
    ), f"Object {mesh_object_name} is not an Object. Cannot use the Boolean modifier with {type(blenderObject.data)} type."
    assert isinstance(
        blenderBooleanObject.data, blender_definitions.BlenderTypes.MESH.value
    ), f"Object {with_mesh_object_name} is not an Object. Cannot use the Boolean modifier with {type(blenderBooleanObject.data)} type."

    apply_modifier(
        mesh_object_name,
        blender_definitions.BlenderModifiers.BOOLEAN,
        operation=blender_boolean_type.name,
        object=blenderBooleanObject,
        use_self=True,
        use_hole_tolerant=True,
        # "solver= "EXACT",
        # "double_threshold= 1e-6,
        **kwargs,
    )


def apply_mirror_modifier(
    entity_name: str, mirror_across_entity_name: str, axis: Axis, **kwargs
):
    axisList = [False, False, False]
    axisList[axis.value] = True

    blenderMirrorAcrossObject = get_object(mirror_across_entity_name)

    apply_modifier(
        entity_name,
        blender_definitions.BlenderModifiers.MIRROR,
        mirror_object=blenderMirrorAcrossObject,
        use_axis=axisList,
        use_mirror_merge=False,
        **kwargs,
    )


def apply_screw_modifier(
    entity_name: str,
    angle: Angle,
    axis: Axis,
    screw_pitch: Dimension = Dimension(0),
    iterations=1,
    entity_nameToDetermineAxis=None,
    **kwargs,
):
    # https://docs.blender.org/api/current/bpy.types.ScrewModifier.html
    properties = {
        "axis": axis.name,
        "angle": angle.value,
        "screw_offset": blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
            screw_pitch
        ).value,
        "steps": 64,
        "render_steps": 64,
        "use_merge_vertices": True,
        "iterations": iterations,
    }

    if entity_nameToDetermineAxis:
        blenderMirrorAcrossObject = get_object(entity_nameToDetermineAxis)

        properties["object"] = blenderMirrorAcrossObject

    apply_modifier(
        entity_name, blender_definitions.BlenderModifiers.SCREW, **properties, **kwargs
    )


# MARK: CRUD of Objects (aka Parts)


def blender_primitive_function(
    primitive: blender_definitions.BlenderObjectPrimitiveTypes, dimensions, **kwargs
):
    primitiveName = primitive.default_name_in_blender()

    # Make sure an object or mesh with the same name don't already exist.
    blenderObject = bpy.data.objects.get(primitiveName)
    blenderMesh = bpy.data.meshes.get(primitiveName)

    assert blenderObject is None, f"An object with name {primitiveName} already exists."

    orphanMeshMessage = ""
    if blenderMesh is not None and blenderMesh.users == 0:
        orphanMeshMessage += " Your mesh is an orphan, please delete it."

        # issue-182, add a warning for the Default Cube:
        if primitiveName == "Cube":
            orphanMeshMessage += "If you are starting with the Default Cube, please remove both the object and the mesh using Delete Hierarchy (not just Delete), then try again."

    assert (
        blenderMesh is None
    ), f"A mesh with name {primitiveName} already exists. {orphanMeshMessage}"

    if primitive == blender_definitions.BlenderObjectPrimitiveTypes.cube:
        return bpy.ops.mesh.primitive_cube_add(
            size=1, scale=[dimension.value for dimension in dimensions[:3]], **kwargs
        )

    if primitive == blender_definitions.BlenderObjectPrimitiveTypes.cone:
        return bpy.ops.mesh.primitive_cone_add(
            radius1=dimensions[0].value,
            radius2=dimensions[1].value,
            depth=dimensions[2].value,
            **kwargs,
        )

    if primitive == blender_definitions.BlenderObjectPrimitiveTypes.cylinder:
        return bpy.ops.mesh.primitive_cylinder_add(
            radius=dimensions[0].value, depth=dimensions[1].value, **kwargs
        )

    if primitive == blender_definitions.BlenderObjectPrimitiveTypes.torus:
        return bpy.ops.mesh.primitive_torus_add(
            mode="EXT_INT",
            abso_minor_rad=dimensions[0].value,
            abso_major_rad=dimensions[1].value,
            **kwargs,
        )

    if primitive == blender_definitions.BlenderObjectPrimitiveTypes.sphere:
        return bpy.ops.mesh.primitive_ico_sphere_add(
            radius=dimensions[0].value, **kwargs
        )

    if primitive == blender_definitions.BlenderObjectPrimitiveTypes.uvsphere:
        return bpy.ops.mesh.primitive_uv_sphere_add(
            radius=dimensions[0].value, **kwargs
        )

    if primitive == blender_definitions.BlenderObjectPrimitiveTypes.circle:
        return bpy.ops.mesh.primitive_circle_add(radius=dimensions[0].value, **kwargs)

    if primitive == blender_definitions.BlenderObjectPrimitiveTypes.grid:
        return bpy.ops.mesh.primitive_grid_add(size=dimensions[0].value, **kwargs)

    if primitive == blender_definitions.BlenderObjectPrimitiveTypes.monkey:
        return bpy.ops.mesh.primitive_monkey_add(size=dimensions[0].value, **kwargs)

    if primitive == blender_definitions.BlenderObjectPrimitiveTypes.empty:
        return bpy.ops.object.empty_add(radius=dimensions[0].value, **kwargs)

    if primitive == blender_definitions.BlenderObjectPrimitiveTypes.plane:
        return bpy.ops.mesh.primitive_plane_add(**kwargs)

    raise Exception(f"Primitive with name {primitive.name} is not implemented.")


# Extracts dimensions from a string, then passes them as arguments to the blender_primitive_function
def add_primitive(
    primitive_type: blender_definitions.BlenderObjectPrimitiveTypes,
    dimensions: str,
    **kwargs,
):
    assert primitive_type is not None, "Primitive type is required."

    # Convert the dimensions:
    dimensionsList: list[Dimension] = (
        get_dimension_list_from_string_list(dimensions) or []
    )

    dimensionsList = (
        blender_definitions.BlenderLength.convert_dimensions_to_blender_unit(
            dimensionsList
        )
    )

    # Add the object:
    blender_primitive_function(primitive_type, dimensionsList, **kwargs)


def create_gear(
    object_name: str,
    outer_radius: DimensionOrItsFloatOrStringValue,
    addendum: DimensionOrItsFloatOrStringValue,
    inner_radius: DimensionOrItsFloatOrStringValue,
    dedendum: DimensionOrItsFloatOrStringValue,
    height: DimensionOrItsFloatOrStringValue,
    pressure_angle: AngleOrItsFloatOrStringValue = "20d",
    number_of_teeth: "int" = 12,
    skew_angle: AngleOrItsFloatOrStringValue = 0,
    conical_angle: AngleOrItsFloatOrStringValue = 0,
    crown_angle: AngleOrItsFloatOrStringValue = 0,
):
    addon_name = "add_mesh_extra_objects"

    # check if the addon is enabled, enable it if it is not.
    addon = bpy.context.preferences.addons.get(addon_name)
    if addon is None:
        addon_set_enabled(addon_name, True)
        addon = bpy.context.preferences.addons.get(addon_name)

    assert (
        addon is not None
    ), f"Could not enable the {addon_name} addon to create extra objects"

    outer_radiusDimension = (
        blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
            Dimension.from_string(outer_radius)
        ).value
    )
    inner_radiusDimension = (
        blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
            Dimension.from_string(inner_radius)
        ).value
    )
    addendumDimension = (
        blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
            Dimension.from_string(addendum)
        ).value
    )
    dedendumDimension = (
        blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
            Dimension.from_string(dedendum)
        ).value
    )
    heightDimension = (
        blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
            Dimension.from_string(height)
        ).value
    )

    if addendumDimension > outer_radiusDimension / 2:
        addendumDimension = outer_radiusDimension / 2
    if inner_radiusDimension > outer_radiusDimension:
        inner_radiusDimension = outer_radiusDimension
    if dedendumDimension + inner_radiusDimension > outer_radiusDimension:
        dedendumDimension = outer_radiusDimension - inner_radiusDimension

    pressure_angleValue = Angle.from_string(pressure_angle).to_radians().value
    skew_angleValue = Angle.from_string(skew_angle).to_radians().value
    conical_angleValue = Angle.from_string(conical_angle).to_radians().value
    crown_angleValue = Angle.from_string(crown_angle).to_radians().value

    return bpy.ops.mesh.primitive_gear(  # type: ignore
        name=object_name,
        number_of_teeth=number_of_teeth,
        radius=outer_radiusDimension,
        addendum=addendumDimension,
        dedendum=dedendumDimension,
        angle=pressure_angleValue,
        base=inner_radiusDimension,
        width=heightDimension,
        skew=skew_angleValue,
        conangle=conical_angleValue,
        crown=crown_angleValue,
    )


fileImportFunctions = {
    "stl": lambda file_path: bpy.ops.import_mesh.stl(filepath=file_path),
    "ply": lambda file_path: bpy.ops.import_mesh.ply(filepath=file_path),
    "svg": lambda file_path: bpy.ops.import_curve.svg(filepath=file_path),
    "png": lambda file_path: bpy.ops.image.open(filepath=file_path),
    "fbx": lambda file_path: bpy.ops.import_scene.fbx(filepath=file_path),
    "gltf": lambda file_path: bpy.ops.import_scene.gltf(filepath=file_path),
    "obj": lambda file_path: bpy.ops.import_scene.obj(
        filepath=file_path, use_split_objects=False
    ),
    "x3d": lambda file_path: bpy.ops.import_scene.x3d(filepath=file_path),
}


def import_file(file_path: str, file_type: Optional[str] = None) -> str:
    path = Path(file_path).resolve()

    # Check if the file exists:
    assert path.is_file(), f"File {file_path} does not exist"

    fileName = path.stem

    # Make sure an object or mesh with the same name don't already exist:
    blenderObject = bpy.data.objects.get(fileName)
    blenderMesh = bpy.data.meshes.get(fileName)

    assert blenderObject is None, f"An object with name {fileName} already exists."
    assert blenderMesh is None, f"A mesh with name {fileName} already exists."

    # Check if this is a file-type we support:
    file_type = file_type or get_file_extension(file_path)

    assert file_type in fileImportFunctions, f"File type {file_type} is not supported"

    # Import the file:
    old_objs = set(bpy.context.scene.objects)

    isSuccess = fileImportFunctions[file_type](file_path) == {"FINISHED"}

    assert isSuccess is True, f"Could not import {file_path}"

    imported_objs = list(set(bpy.context.scene.objects) - old_objs)
    active_object = imported_objs[0]

    # if imported file has multiple parts, collapse them. We really can't handle unknown objects being thrown in at the moment. References https://blender.stackexchange.com/a/108112 and https://blender.stackexchange.com/a/43357
    with get_context_view_3d(
        active_object=active_object, selected_objects=imported_objs
    ):
        for o in imported_objs:
            o.select_set(True)
        bpy.context.view_layer.objects.active = active_object
        update_view_layer()
        bpy.ops.object.join()

    # return the imported objects, assumed to be selected at import
    return active_object.name


# MARK: Transformations


def apply_object_transformations(
    object_name: str,
    apply_rotation: bool,
    apply_scale: bool,
    apply_location: bool,
):
    # Apply the object's transformations (under Object Properties tab)
    # references https://blender.stackexchange.com/a/159540/138679
    blenderObject = get_object(object_name)

    assert (
        blenderObject.data is not None
    ), f"Object {object_name} does not have data to transform."

    decomposedMatrix: list[Any] = blenderObject.matrix_basis.decompose()  # type: ignore
    translationVector: mathutils.Vector = decomposedMatrix[0]
    rotationQuat: mathutils.Quaternion = decomposedMatrix[1]
    scaleVector: mathutils.Vector = decomposedMatrix[2]

    translation: mathutils.Matrix = mathutils.Matrix.Translation(translationVector)
    rotation: mathutils.Matrix = rotationQuat.to_matrix().to_4x4()
    scale: mathutils.Matrix = mathutils.Matrix.Diagonal(scaleVector).to_4x4()

    transformation: mathutils.Matrix = mathutils.Matrix()
    basis: mathutils.Matrix = mathutils.Matrix()

    if apply_rotation:
        transformation @= rotation
    else:
        basis @= rotation
    if apply_scale:
        transformation @= scale
    else:
        basis @= scale
    if apply_location:
        transformation @= translation
    else:
        basis @= translation

    mesh: bpy.types.Mesh = blenderObject.data  # type: ignore
    mesh.transform(transformation)

    # Set the object to its world translation
    blenderObject.matrix_basis = basis

    for child in blenderObject.children:
        child.matrix_basis = transformation @ child.matrix_basis  # type: ignore


def rotate_object(
    object_name: str,
    rotation_angles: list[Optional[Angle]],
    rotation_type: blender_definitions.BlenderRotationTypes,
):
    blenderObject = get_object(object_name)

    currentRotation = getattr(blenderObject, rotation_type.value)

    outputRotation = []

    for index in range(len(currentRotation)):
        angle = currentRotation[index]
        newAngle = rotation_angles[index]
        if newAngle is not None:
            angle = newAngle.to_radians().value
        outputRotation.append(angle)

    setattr(blenderObject, rotation_type.value, outputRotation)


def translate_object(
    object_name: str,
    translation_dimensions: list[Optional[Dimension]],
    translation_type: blender_definitions.BlenderTranslationTypes,
):
    blenderObject = get_object(object_name)

    assert len(translation_dimensions) == 3, "translation_dimensions must be length 3"

    currentLocation = blenderObject.location

    outputLocation = []

    for index in range(3):
        location = currentLocation[index]
        newLocation = translation_dimensions[index]
        if newLocation is not None:
            location = newLocation.value
        outputLocation.append(location)

    setattr(blenderObject, translation_type.value, outputLocation)


def set_object_location(
    object_name: str, location_dimensions: list[Optional[Dimension]]
):
    blenderObject = get_object(object_name)

    assert len(location_dimensions) == 3, "location_dimensions must be length 3"

    currentLocation = blenderObject.location

    outputLocation = []

    for index in range(3):
        location = currentLocation[index]
        newLocation = location_dimensions[index]
        if newLocation is not None:
            location = newLocation.value
        outputLocation.append(location)

    blenderObject.location = outputLocation


def scale_object(
    object_name: str,
    x_scale_factor: Optional[float],
    y_scale_factor: Optional[float],
    z_scale_factor: Optional[float],
):
    blenderObject = get_object(object_name)

    currentScale: mathutils.Vector = blenderObject.scale  # type: ignore

    blenderObject.scale = (
        x_scale_factor or currentScale.x,
        y_scale_factor or currentScale.y,
        z_scale_factor or currentScale.z,
    )


# MARK: collections and groups:


def get_collection(name: str, scene_name="Scene") -> bpy.types.Collection:
    collection = bpy.data.scenes[scene_name].collection.children.get(name)

    assert (
        collection is not None
    ), f"Collection {name} does not exists in scene {scene_name}"

    return collection


def create_collection(name: str, scene_name="Scene"):
    assert (
        scene_name in bpy.data.scenes
    ), f"Scene {scene_name} does not exist"  # type: ignore

    existing_collection = bpy.data.scenes[scene_name].collection.children.get(name)

    assert existing_collection is None, f"Collection {name} already exists"

    collection = bpy.data.collections.new(name)

    bpy.data.scenes[scene_name].collection.children.link(collection)


def remove_collection(name: str, scene_name: str, remove_children: bool):
    collection = get_collection(name, scene_name)

    if remove_children:
        for obj in collection.objects:
            try:
                remove_object(obj.name, True)
            except Exception as e:
                print(f"Could not remove {obj.name}. {e}")
                pass

    bpy.data.collections.remove(collection)


def remove_object_from_collection(
    existing_object_name: str, collection_name: str, scene_name: str
):
    blenderObject = get_object(existing_object_name)

    collection = get_collection(collection_name, scene_name)

    assert (
        collection.objects.get(existing_object_name) is not None
    ), f"Object {existing_object_name} does not exist in collection {collection_name}"

    collection.objects.unlink(blenderObject)


def assign_object_to_collection(
    existing_object_name: str,
    collection_name="Scene Collection",
    scene_name="Scene",
    remove_from_other_groups=True,
    move_children=True,
):
    blenderObject = get_object(existing_object_name)

    collection = bpy.data.collections.get(collection_name)

    if collection is None and collection_name == "Scene Collection":
        scene = bpy.data.scenes.get(scene_name)

        assert scene is not None, f"Scene {scene_name} does not exist"

        collection = scene.collection

    assert collection is not None, f"Collection {collection_name} does not exist"

    if remove_from_other_groups:
        currentCollections: list[
            bpy.types.Collection
        ] = blenderObject.users_collection  # type: ignore
        for currentCollection in currentCollections:
            currentCollection.objects.unlink(blenderObject)

    collection.objects.link(blenderObject)

    if move_children:
        for child in blenderObject.children:  # type: ignore
            assign_object_to_collection(
                child.name, collection_name, scene_name, True, True
            )


# MARK: Joints
def get_constraint(object_name: str, constraint_name) -> Optional[bpy.types.Constraint]:
    blenderObject = get_object(object_name)
    return blenderObject.constraints.get(constraint_name)


def apply_constraint(
    object_name: str,
    constraint_type: blender_definitions.BlenderConstraintTypes,
    **kwargs,
):
    blenderObject = get_object(object_name)

    constraint_name = kwargs.get("name") or constraint_type.get_default_blender_name()

    constraint = get_constraint(object_name, constraint_name)

    # If it doesn't exist, create it:
    if constraint is None:
        constraint = blenderObject.constraints.new(constraint_type.name)

    # Apply every parameter passed in for modifier:
    for key, value in kwargs.items():
        setattr(constraint, key, value)


def apply_limit_location_constraint(
    object_name: str,
    x: Optional[list[Optional[Dimension]]],
    y: Optional[list[Optional[Dimension]]],
    z: Optional[list[Optional[Dimension]]],
    relative_to_object_name: Optional[str],
    **kwargs,
):
    relativeToObject = (
        get_object(relative_to_object_name) if relative_to_object_name else None
    )

    [minX, maxX] = x or [None, None]
    [minY, maxY] = y or [None, None]
    [minZ, maxZ] = z or [None, None]

    keywordArguments = kwargs or {}

    keywordArguments[
        "name"
    ] = blender_definitions.BlenderConstraintTypes.LIMIT_LOCATION.format_constraint_name(
        object_name, relativeToObject
    )

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

    apply_constraint(
        object_name,
        blender_definitions.BlenderConstraintTypes.LIMIT_LOCATION,
        **keywordArguments,
    )


def apply_limit_rotation_constraint(
    object_name: str,
    x: Optional[list[Optional[Angle]]],
    y: Optional[list[Optional[Angle]]],
    z: Optional[list[Optional[Angle]]],
    relative_to_object_name: Optional[str],
    **kwargs,
):
    relativeToObject = (
        get_object(relative_to_object_name) if relative_to_object_name else None
    )

    [minX, maxX] = x or [None, None]
    [minY, maxY] = y or [None, None]
    [minZ, maxZ] = z or [None, None]

    keywordArguments = kwargs or {}

    keywordArguments[
        "name"
    ] = blender_definitions.BlenderConstraintTypes.LIMIT_ROTATION.format_constraint_name(
        object_name, relativeToObject
    )

    keywordArguments["owner_space"] = "CUSTOM" if relativeToObject else "WORLD"

    keywordArguments["space_object"] = relativeToObject

    keywordArguments["use_transform_limit"] = True

    if minX:
        keywordArguments["use_limit_x"] = True
        keywordArguments["min_x"] = minX.to_radians().value
    if minY:
        keywordArguments["use_limit_y"] = True
        keywordArguments["min_y"] = minY.to_radians().value
    if minZ:
        keywordArguments["use_limit_z"] = True
        keywordArguments["min_z"] = minZ.to_radians().value
    if maxX:
        keywordArguments["use_limit_x"] = True
        keywordArguments["max_x"] = maxX.to_radians().value
    if maxY:
        keywordArguments["use_limit_y"] = True
        keywordArguments["max_y"] = maxY.to_radians().value
    if maxZ:
        keywordArguments["use_limit_z"] = True
        keywordArguments["max_z"] = maxZ.to_radians().value

    apply_constraint(
        object_name,
        blender_definitions.BlenderConstraintTypes.LIMIT_ROTATION,
        **keywordArguments,
    )


def apply_copy_location_constraint(
    object_name: str,
    copied_object_name: str,
    copy_x: bool,
    copy_y: bool,
    copy_z: bool,
    use_offset: bool,
    **kwargs,
):
    copiedObject = get_object(copied_object_name)

    apply_constraint(
        object_name,
        blender_definitions.BlenderConstraintTypes.COPY_LOCATION,
        name=blender_definitions.BlenderConstraintTypes.COPY_LOCATION.format_constraint_name(
            object_name, copied_object_name
        ),
        target=copiedObject,
        use_x=copy_x,
        use_y=copy_y,
        use_z=copy_z,
        use_offset=use_offset,
        **kwargs,
    )


def apply_copy_rotation_constraint(
    object_name: str,
    copied_object_name: str,
    copy_x: bool,
    copy_y: bool,
    copy_z: bool,
    **kwargs,
):
    copiedObject = get_object(copied_object_name)

    apply_constraint(
        object_name,
        blender_definitions.BlenderConstraintTypes.COPY_ROTATION,
        name=blender_definitions.BlenderConstraintTypes.COPY_ROTATION.format_constraint_name(
            object_name, copied_object_name
        ),
        target=copiedObject,
        use_x=copy_x,
        use_y=copy_y,
        use_z=copy_z,
        mix_mode="BEFORE",
        **kwargs,
    )


def apply_pivot_constraint(object_name: str, pivot_object_name: str, **kwargs):
    pivotObject = get_object(pivot_object_name)

    apply_constraint(
        object_name,
        blender_definitions.BlenderConstraintTypes.PIVOT,
        name=blender_definitions.BlenderConstraintTypes.PIVOT.format_constraint_name(
            object_name, pivot_object_name
        ),
        target=pivotObject,
        rotation_range="ALWAYS_ACTIVE",
        **kwargs,
    )


def apply_gear_constraint(
    object_name: str, gear_object_name: str, ratio: float = 1, **kwargs
):
    for axis in Axis:
        # e.g. constraints["Limit Location"].min_x
        driver = create_driver(object_name, "rotation_euler", axis.value)
        set_driver(driver, "SCRIPTED", f"{-1*ratio} * gearRotation")
        set_driverVariableSingleProp(
            driver, "gearRotation", gear_object_name, f"rotation_euler[{axis.value}]"
        )


# MARK: Drivers / Computed variables


def create_driver(object_name: str, path: str, index=-1):
    blenderObject = get_object(object_name)

    return blenderObject.driver_add(path, index).driver


def remove_driver(object_name: str, path: str, index=-1):
    blenderObject = get_object(object_name)

    blenderObject.driver_remove(path, index)


def get_driver(
    object_name: str,
    path: str,
):
    blenderObject = get_object(object_name)

    # this returns an FCurve object
    # https://docs.blender.org/api/current/bpy.types.FCurve.html
    fcurve = blenderObject.animation_data.drivers.find(path)

    assert fcurve is not None, f"Could not find driver {path} for object {object_name}."

    return fcurve.driver


def set_driver(
    driver: bpy.types.Driver,
    driver_type,  # : blender_definitions.BlenderDriverTypes,
    expression="",
):
    driver.type = driver_type

    driver.expression = expression if expression else ""


def set_driverVariableSingleProp(
    driver: bpy.types.Driver,
    variable_name: str,
    target_object_name: str,
    target_data_path: str,
):
    variable = driver.variables.get(variable_name)

    if variable is None:
        variable = driver.variables.new()
        driver.variables[-1].name = variable_name

    variable.type = "SINGLE_PROP"

    target_object = get_object(target_object_name)

    variable.targets[0].id = target_object

    variable.targets[0].data_path = target_data_path


def set_driverVariableTransforms(
    driver: bpy.types.Driver,
    variable_name: str,
    target_object_name: str,
    transform_type,  # : blender_definitions.BlenderDriverVariableTransformTypes,
    transform_space,  # : blender_definitions.BlenderDriverVariableTransformSpaces
):
    variable = driver.variables.get(variable_name)

    if variable is None:
        variable = driver.variables.new()
        driver.variables[-1].name = variable_name

    variable.type = "‘TRANSFORMS’"

    target_object = get_object(target_object_name)

    variable.targets[0].id = target_object

    variable.targets[0].transform_type = transform_type

    variable.targets[0].transform_space = transform_space


def set_driverVariableLocationDifference(
    driver: bpy.types.Driver,
    variable_name: str,
    target1_object_name: str,
    target2_object_name: str,
):
    variable = driver.variables.get(variable_name)

    if variable is None:
        variable = driver.variables.new()
        driver.variables[-1].name = variable_name

    variable.type = "‘LOC_DIFF’"

    target1Object = get_object(target1_object_name)

    variable.targets[0].id = target1Object

    target2Object = get_object(target2_object_name)

    variable.targets[1].id = target2Object


def set_driverVariableRotationDifference(
    driver: bpy.types.Driver,
    variable_name: str,
    target1_object_name: str,
    target2_object_name: str,
):
    variable = driver.variables.get(variable_name)

    if variable is None:
        variable = driver.variables.new()
        driver.variables[-1].name = variable_name

    variable.type = "‘ROTATION_DIFF’"

    target1Object = get_object(target1_object_name)

    variable.targets[0].id = target1Object

    target2Object = get_object(target2_object_name)

    variable.targets[1].id = target2Object


# MARK: Landmarks


def translate_landmark_onto_another(
    object_to_translate_name: str,
    object1_landmark_name: str,
    object2_landmark_name: str,
):
    update_view_layer()
    object1LandmarkLocation = get_object_world_location(object1_landmark_name)
    object2LandmarkLocation = get_object_world_location(object2_landmark_name)

    translation = (object1LandmarkLocation) - (object2LandmarkLocation)

    blenderDefaultUnit = blender_definitions.BlenderLength.DEFAULT_BLENDER_UNIT.value

    translate_object(
        object_to_translate_name,
        [
            Dimension(translation.x.value, blenderDefaultUnit),
            Dimension(translation.y.value, blenderDefaultUnit),
            Dimension(translation.z.value, blenderDefaultUnit),
        ],  # type: ignore
        blender_definitions.BlenderTranslationTypes.ABSOLUTE,
    )


# MARK: creating and manipulating objects


def make_parent(
    name: str,
    parent_name: str,
):
    blenderObject = get_object(name)
    blenderParentObject = get_object(parent_name)

    blenderObject.parent = blenderParentObject


def update_object_name(
    old_name: str,
    new_name: str,
):
    blenderObject = get_object(old_name)

    blenderObject.name = new_name


def get_object_collection_name(
    object_name: str,
) -> str:
    blenderObject = get_object(object_name)

    # Assumes the first collection is the main collection
    [currentCollection] = blenderObject.users_collection  # type: ignore

    return currentCollection.name


def update_object_data_name(
    parent_object_name: str,
    new_name: str,
):
    blenderObject = get_object(parent_object_name)

    assert (
        blenderObject.data is not None
    ), f"Object {parent_object_name} does not have data to name."

    blenderObject.data.name = new_name


# This assumes that landmarks are named with format: `{parentPartName}_{landmarkName}`
def update_object_landmark_names(
    parent_object_name: str,
    old_namePrefix: str,
    new_namePrefix: str,
):
    blenderObject = get_object(parent_object_name)

    blenderObjectChildren: list[
        bpy.types.Object
    ] = blenderObject.children  # type: ignore

    for child in blenderObjectChildren:
        if f"{old_namePrefix}_" in child.name and child.type == "EMPTY":
            update_object_name(
                child.name,
                child.name.replace(f"{old_namePrefix}_", f"{new_namePrefix}_"),
            )


def remove_object(existing_object_name: str, remove_children=False):
    blenderObject = get_object(existing_object_name)

    if remove_children:
        blenderObjectChildren: list[
            bpy.types.Object
        ] = blenderObject.children  # type: ignore
        for child in blenderObjectChildren:
            try:
                remove_object(child.name, True)
            except Exception as e:
                print(f"Could not remove {child.name}. {e}")
                pass

    # Not all objects have data, but if they do, then deleting the data
    # deletes the object
    if blenderObject.data and isinstance(blenderObject.data, bpy.types.Mesh):
        bpy.data.meshes.remove(blenderObject.data)
    elif blenderObject.data and isinstance(blenderObject.data, bpy.types.Curve):
        bpy.data.curves.remove(blenderObject.data)
    elif blenderObject.data and isinstance(blenderObject.data, bpy.types.TextCurve):
        bpy.data.curves.remove(blenderObject.data)
    else:
        bpy.data.objects.remove(blenderObject)


def create_object(name: str, data: Optional[Any] = None):
    blenderObject = bpy.data.objects.get(name)

    assert blenderObject is None, f"Object {name} already exists"

    return bpy.data.objects.new(name, data)


def create_object_vertex_group(
    object_name: str,
    vertex_group_name: str,
):
    blenderObject = get_object(object_name)
    return blenderObject.vertex_groups.new(name=vertex_group_name)


def get_object_vertex_group(
    object_name: str,
    vertex_group_name: str,
):
    blenderObject = get_object(object_name)
    return blenderObject.vertex_groups.get(vertex_group_name)


def add_verticies_to_vertex_group(vertex_group_object, vertex_indecies: list[int]):
    vertex_group_object.add(vertex_indecies, 1.0, "ADD")


def convert_object_using_ops(
    existing_object_name: str, convert_to_type: blender_definitions.BlenderTypes
):
    existingObject = get_object(existing_object_name)
    with get_context_view_3d(
        active_object=existingObject, selected_objects=[existingObject]
    ):
        existingObject.select_set(True)
        bpy.context.view_layer.objects.active = existingObject
        update_view_layer()

        bpy.ops.object.convert(target=convert_to_type.name)


def create_mesh_from_curve(
    existing_curve_object_name: str,
    new_object_name: Optional[str] = None,
):
    existingCurveObject = get_object(existing_curve_object_name)

    if new_object_name is None:
        update_object_name(existing_curve_object_name, str(uuid4()))
        new_object_name = existing_curve_object_name

    dependencyGraph = bpy.context.evaluated_depsgraph_get()
    evaluatedObject: bpy.types.Object = existingCurveObject.evaluated_get(
        dependencyGraph
    )  # type: ignore
    mesh: bpy.types.Mesh = bpy.data.meshes.new_from_object(
        evaluatedObject, depsgraph=dependencyGraph
    )

    blenderObject = create_object(new_object_name, mesh)

    blenderObject.matrix_world = existingCurveObject.matrix_world

    assign_object_to_collection(new_object_name)

    existingCurveObjectChildren: list[
        bpy.types.Object
    ] = existingCurveObject.children  # type: ignore
    for child in existingCurveObjectChildren:
        if (
            isinstance(child, blender_definitions.BlenderTypes.OBJECT.value)
            and child.type == "EMPTY"
        ):
            child.parent = blenderObject

    # twisted logic here, but if we renamed this above, we want to nuke it because we're done with it.
    if existingCurveObject.name != existing_curve_object_name:
        remove_object(existingCurveObject.name, remove_children=True)


def get_object_visibility(
    existing_object_name: str,
) -> bool:
    blenderObject = get_object(existing_object_name)

    return blenderObject.visible_get()


def set_object_visibility(existing_object_name: str, is_visible: bool):
    blenderObject = get_object(existing_object_name)

    # blenderObject.hide_viewport = not is_visible
    # blenderObject.hide_render = not is_visible
    blenderObject.hide_set(not is_visible)


def transfer_landmarks(
    from_object_name: str,
    to_object_name: str,
):
    update_view_layer()

    fromBlenderObject = get_object(from_object_name)
    toBlenderObject = get_object(to_object_name)

    translation = (
        get_object_world_location(from_object_name)
        - get_object_world_location(to_object_name)
    ).to_list()

    translation = [
        axisValue.value
        for axisValue in blender_definitions.BlenderLength.convert_dimensions_to_blender_unit(
            translation
        )
    ]

    defaultCollection = get_object_collection_name(to_object_name)

    fromBlenderObjectChildren: list[
        bpy.types.Object
    ] = fromBlenderObject.children  # type: ignore
    for child in fromBlenderObjectChildren:
        if (
            isinstance(child, blender_definitions.BlenderTypes.OBJECT.value)
            and child.type == "EMPTY"
        ):
            child.name = f"{to_object_name}_{child.name}"
            isAlreadyExists = bpy.data.objects.get(child.name) is None
            if isAlreadyExists:
                print(f"{child.name} already exists. Skipping landmark transfer.")
                continue
            child.parent = toBlenderObject
            child.location = child.location + mathutils.Vector(
                translation
            )  # type: ignore
            assign_object_to_collection(child.name, defaultCollection)


def duplicate_object(
    existing_object_name: str, new_object_name: str, copy_landmarks: bool = True
):
    clonedObject = bpy.data.objects.get(new_object_name)  # type: ignore

    assert clonedObject is None, f"Object with name {new_object_name} already exists."

    blenderObject = get_object(existing_object_name)

    clonedObject: bpy.types.Object = blenderObject.copy()  # type: ignore
    clonedObject.name = new_object_name
    clonedObject.data = blenderObject.data.copy()
    clonedObject.data.name = new_object_name

    # Link clonedObject to the original object's collection.
    defaultCollection = get_object_collection_name(existing_object_name)

    assign_object_to_collection(new_object_name, defaultCollection)

    if copy_landmarks:
        blenderObjectChildren: list[
            bpy.types.Object
        ] = blenderObject.children  # type: ignore
        for child in blenderObjectChildren:
            if (
                isinstance(child, blender_definitions.BlenderTypes.OBJECT.value)
                and child.type == "EMPTY"
            ):
                newChild: bpy.types.Object = child.copy()  # type: ignore
                newChild.name = child.name.replace(
                    existing_object_name, new_object_name
                )
                newChild.parent = clonedObject
                assign_object_to_collection(newChild.name, defaultCollection)


def update_view_layer():
    bpy.context.view_layer.update()


def get_object_local_location(
    object_name: str,
):
    blenderObject = get_object(object_name)

    return Point.from_list(
        [
            Dimension(p, blender_definitions.BlenderLength.DEFAULT_BLENDER_UNIT.value)
            for p in blenderObject.location
        ]
    )


def get_object_world_location(
    object_name: str,
):
    blenderObject = get_object(object_name)

    return Point.from_list(
        [
            Dimension(p, blender_definitions.BlenderLength.DEFAULT_BLENDER_UNIT.value)
            for p in blenderObject.matrix_world.translation  # type: ignore
        ]
    )


def get_object_world_pose(
    object_name: str,
) -> list[float]:
    blenderObject = get_object(object_name)

    listOfTuples = [
        v.to_tuple() for v in list(blenderObject.matrix_world)
    ]  # type: ignore

    return [value for values in listOfTuples for value in values]


def get_object(
    object_name: str,
) -> bpy.types.Object:
    blenderObject = bpy.data.objects.get(object_name)

    assert blenderObject is not None, f"Object {object_name} does not exists"

    return blenderObject


def get_mesh(
    mesh_name: str,
) -> bpy.types.Mesh:
    blenderMesh = bpy.data.meshes.get(mesh_name)

    assert blenderMesh is not None, f"Mesh {mesh_name} does not exists"

    return blenderMesh


def get_objectType(object_name: str) -> blender_definitions.BlenderObjectTypes:
    blenderObject = bpy.data.objects.get(object_name)

    assert blenderObject is not None, f"Object {object_name} does not exists"

    return blender_definitions.BlenderObjectTypes[blenderObject.type]


# Applies the dependency graph to the object and persists its data using .copy()
# This allows us to apply modifiers, UV data, etc.. to the mesh.
# This is different from apply_object_transformations()
def apply_dependency_graph(
    existing_object_name: str,
):
    blenderObject = get_object(existing_object_name)
    blenderObjectEvaluated: bpy.types.Object = blenderObject.evaluated_get(
        bpy.context.evaluated_depsgraph_get()
    )  # type: ignore
    blenderObject.data = blenderObjectEvaluated.data.copy()


def clear_modifiers(
    object_name: str,
):
    blenderObject = get_object(object_name)

    blenderObject.modifiers.clear()


def remove_mesh(
    mesh_nameOrInstance: Union[str, bpy.types.Mesh],
):
    mesh: bpy.types.Mesh = mesh_nameOrInstance  # type: ignore
    # if a (str) name is passed in, fetch the mesh object reference
    if isinstance(mesh_nameOrInstance, str):
        mesh = get_mesh(mesh_nameOrInstance)

    bpy.data.meshes.remove(mesh)


def set_edges_mean_crease(mesh_name: str, mean_crease_value: float):
    blenderMesh = get_mesh(mesh_name)

    for edge in blenderMesh.edges:
        edge.crease = mean_crease_value


def recalculate_normals(mesh_name: str):
    # references https://blender.stackexchange.com/a/72687

    mesh = get_mesh(mesh_name)

    bMesh = bmesh.new()
    bMesh.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bMesh, faces=bMesh.faces)  # type: ignore
    bMesh.to_mesh(mesh)
    bMesh.clear()

    mesh.update()


# Note: transformations have to be applied for this to be reliable.
def is_collision_between_two_objects(
    object1_name: str,
    object2_name: str,
):
    update_view_layer()

    blenderObject1 = get_object(object1_name)
    blenderObject2 = get_object(object2_name)

    # References https://blender.stackexchange.com/a/144609
    bm1 = bmesh.new()
    bm2 = bmesh.new()

    bm1.from_mesh(get_mesh(blenderObject1.name))
    bm2.from_mesh(get_mesh(blenderObject2.name))

    bm1.transform(blenderObject1.matrix_world)  # type: ignore
    bm2.transform(blenderObject2.matrix_world)  # type: ignore

    obj_now_BVHtree = BVHTree.FromBMesh(bm1)
    obj_next_BVHtree = BVHTree.FromBMesh(bm2)

    uniqueIndecies = obj_now_BVHtree.overlap(obj_next_BVHtree)  # type: ignore

    return len(uniqueIndecies) > 0


# References https://docs.blender.org/api/current/mathutils.kdtree.html
def create_kd_tree_for_object(
    object_name: str,
):
    blenderObject = get_object(object_name)
    mesh: bpy.types.Mesh = blenderObject.data  # type: ignore
    size = len(mesh.vertices)
    kd = KDTree(size)

    for i, v in enumerate(mesh.vertices):
        kd.insert(v.co, i)

    kd.balance()
    return kd


# uses object.closest_point_on_mesh https://docs.blender.org/api/current/bpy.types.Object.html#bpy.types.Object.closest_point_on_mesh
def get_closest_face_to_vertex(object_name: str, vertex) -> bpy.types.MeshPolygon:
    blenderObject = get_object(object_name)

    assert (
        len(vertex) == 3
    ), "Vertex is not length 3. Please provide a proper vertex (x,y,z)"

    matrixWorld: mathutils.Matrix = blenderObject.matrix_world  # type: ignore
    invertedMatrixWorld = matrixWorld.inverted()

    # vertex in object space:
    vertexInverted = invertedMatrixWorld @ mathutils.Vector(vertex)

    # polygonIndex references an index at blenderObject.data.polygons[polygonIndex], in other words, the face or edge data
    [isFound, closestPoint, normal, polygonIndex] = blenderObject.closest_point_on_mesh(
        vertexInverted
    )  # type: ignore

    assert isFound, f"Could not find a point close to {vertex} on {object_name}"

    assert (
        polygonIndex is not None and polygonIndex != -1
    ), f"Could not find a face near {vertex} on {object_name}"

    mesh: bpy.types.Mesh = blenderObject.data  # type: ignore
    blenderPolygon = mesh.polygons[polygonIndex]

    return blenderPolygon


# Returns a list of (co, index, dist)
def get_closest_points_to_vertex(
    object_name: str, vertex, number_of_points=2, object_kd_tree=None
):
    blenderObject = get_object(object_name)

    kdTree = object_kd_tree or create_kd_tree_for_object(object_name)

    assert (
        len(vertex) == 3
    ), "Vertex is not length 3. Please provide a proper vertex (x,y,z)"

    matrixWorld: mathutils.Matrix = blenderObject.matrix_world  # type: ignore
    invertedMatrixWorld = matrixWorld.inverted()

    vertexInverted: mathutils.Vector = invertedMatrixWorld @ mathutils.Vector(
        vertex
    )  # type: ignore

    return kdTree.find_n(vertexInverted, number_of_points)


# References https://blender.stackexchange.com/a/32288/138679
def get_bounding_box(
    object_name: str,
):
    update_view_layer()

    blenderObject = get_object(object_name)

    local_coords = blenderObject.bound_box[:]

    # om = blenderObject.matrix_world
    om = blenderObject.matrix_basis

    # matrix multiple world transform by all the vertices in the boundary
    coords = [
        (om @ mathutils.Vector(p[:])).to_tuple() for p in local_coords  # type: ignore
    ]
    coords = coords[::-1]
    # Coords should be a 1x8 array containing 1x3 vertices, example:
    # [(1.0, 1.0, -1.0), (1.0, 1.0, 1.0), (1.0, -1.0, 1.0), (1.0, -1.0, -1.0), (-1.0, 1.0, -1.0), (-1.0, 1.0, 1.0), (-1.0, -1.0, 1.0), (-1.0, -1.0, -1.0)]

    # After zipping we should get
    # x (1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0, -1.0)
    # y (1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0, -1.0)
    # z (-1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0)
    zipped = zip("xyz", zip(*coords))

    boundingBox = BoundaryBox(None, None, None)

    for axis, _list in zipped:
        minVal = min(_list)
        maxVal = max(_list)

        setattr(boundingBox, axis, BoundaryAxis(minVal, maxVal, "m"))

    return boundingBox


# MARK: ADDONS


def addon_set_enabled(addon_name: str, is_enabled: bool):
    preferences = bpy.ops.preferences

    command = preferences.addon_enable if is_enabled else preferences.addon_disable

    command(module=addon_name)


# MARK: Curves and Sketches


def get_curve(curve_name: str) -> bpy.types.Curve:
    curve = bpy.data.curves.get(curve_name)

    assert curve is not None, f"Curve {curve_name} does not exists"

    return curve


def extrude_curve(curve_name: str, length: Dimension):
    curve = get_curve(curve_name)

    length = blender_definitions.BlenderLength.convert_dimension_to_blender_unit(length)

    curve.extrude = length.value


def offset_curve_geometry(curve_name: str, offset: Dimension):
    curve = get_curve(curve_name)

    length = blender_definitions.BlenderLength.convert_dimension_to_blender_unit(offset)

    curve.offset = length.value


def set_curve_resolution_u(curve_name: str, resolution: int):
    curve = get_curve(curve_name)

    curve.resolution_u = resolution


def set_curve_resolution_v(curve_name: str, resolution: int):
    curve = get_curve(curve_name)

    curve.resolution_v = resolution


def create_text(
    curve_name: str,
    text: str,
    size=Dimension(1),
    bold=False,
    italic=False,
    underlined=False,
    character_spacing=1,
    word_spacing=1,
    line_spacing=1,
    font_file_path: Optional[str] = None,
):
    curveData = bpy.data.curves.new(type="FONT", name=curve_name)

    setattr(curveData, "body", text)
    setattr(
        curveData,
        "size",
        blender_definitions.BlenderLength.convert_dimension_to_blender_unit(size).value,
    )
    setattr(curveData, "space_character", character_spacing)
    setattr(curveData, "space_word", word_spacing)
    setattr(curveData, "space_line", line_spacing)

    if font_file_path:
        fontData = bpy.data.fonts.load(font_file_path.replace("\\", "/"))
        setattr(curveData, "font", fontData)

    if bold or italic or underlined:
        curveDataBodyFormat = curveData.body_format  # type: ignore
        for index in range(len(text)):
            curveDataBodyFormat[index].use_underline = underlined
            curveDataBodyFormat[index].use_bold = bold
            curveDataBodyFormat[index].use_italic = italic

        # setattr(curveData, "body_format", curveDataBodyFormat)

    create_object(curve_name, curveData)

    assign_object_to_collection(curve_name)

    # issue-160: scaling doesn't work well for TextCurves, so we'll convert it to a normal Curve.
    convert_object_using_ops(curve_name, blender_definitions.BlenderTypes.CURVE)

    curveData.use_path = False


def create_3d_curve(
    curve_name: str,
    curve_type: blender_definitions.BlenderCurveTypes,
    coordinates,
    interpolation=64,
):
    curveData = bpy.data.curves.new(curve_name, type="CURVE")
    curveData.dimensions = "3D"
    curveData.resolution_u = interpolation
    curveData.use_path = False

    create_spline(curveData, curve_type, coordinates)

    create_object(curve_name, curveData)

    assign_object_to_collection(curve_name)


# Creates a new Splines instance in the bpy.types.curves object passed in as blender_curve
# then assigns the coordinates to them.
# references https://blender.stackexchange.com/a/6751/138679
def create_spline(
    blender_curve: bpy.types.Curve,
    curve_type: blender_definitions.BlenderCurveTypes,
    coordinates,
):
    coordinates = [
        blender_definitions.BlenderLength.convert_dimensions_to_blender_unit(
            get_dimension_list_from_string_list(coordinate) or []
        )
        for coordinate in coordinates
    ]
    coordinates = [
        [dimension.value for dimension in coordinate] for coordinate in coordinates
    ]

    spline = blender_curve.splines.new(curve_type.name)
    spline.order_u = 2

    # subtract 1 so the end and origin points are not connected
    number_of_points = len(coordinates) - 1

    if curve_type == blender_definitions.BlenderCurveTypes.BEZIER:
        # subtract 1 so the end and origin points are not connected
        spline.bezier_points.add(number_of_points)
        for i, coord in enumerate(coordinates):
            x, y, z = coord
            spline.bezier_points[i].co = (x, y, z)
            spline.bezier_points[i].handle_left = (x, y, z)
            spline.bezier_points[i].handle_right = (x, y, z)

    else:
        # subtract 1 so the end and origin points are not connected
        spline.points.add(number_of_points)

        for i, coord in enumerate(coordinates):
            x, y, z = coord
            spline.points[i].co = (x, y, z, 1)


def add_bevel_object_to_curve(
    path_curve_object_name: str, profile_curve_object_name: str, fill_cap=False
):
    pathCurveObject = get_object(path_curve_object_name)

    profileCurveObject = get_object(profile_curve_object_name)

    assert isinstance(
        profileCurveObject.data, bpy.types.Curve
    ), f"Profile Object {profile_curve_object_name} is not a Curve object. Please use a Curve object."

    curve: bpy.types.Curve = pathCurveObject.data  # type: ignore

    curve.bevel_mode = "OBJECT"
    curve.bevel_object = profileCurveObject
    curve.use_fill_caps = fill_cap


def get_blender_curve_primitive_function(
    curve_primitive: blender_definitions.BlenderCurvePrimitiveTypes,
):
    if curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Point:
        return BlenderCurvePrimitives.create_point
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.LineTo:
        return BlenderCurvePrimitives.create_line_to
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Distance:
        return BlenderCurvePrimitives.create_line
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Angle:
        return BlenderCurvePrimitives.create_angle
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Circle:
        return BlenderCurvePrimitives.create_circle
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Ellipse:
        return BlenderCurvePrimitives.create_ellipse
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Sector:
        return BlenderCurvePrimitives.create_sector
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Segment:
        return BlenderCurvePrimitives.create_segment
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Rectangle:
        return BlenderCurvePrimitives.create_rectangle
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Rhomb:
        return BlenderCurvePrimitives.create_rhomb
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Trapezoid:
        return BlenderCurvePrimitives.create_trapezoid
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Polygon:
        return BlenderCurvePrimitives.create_polygon
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Polygon_ab:
        return BlenderCurvePrimitives.create_polygon_ab
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Arc:
        return BlenderCurvePrimitives.create_arc
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Spiral:
        return BlenderCurvePrimitives.create_spiral

    raise TypeError("Unknown primitive")


class BlenderCurvePrimitives:
    @staticmethod
    def create_point(curve_type=blender_definitions.BlenderCurveTypes.NURBS, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.Point,
            use_cyclic_u=False,
            **kwargs,
        )

    @staticmethod
    def create_line_to(end_location, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.LineTo,
            Simple_endlocation=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(end_location)
            ).value,
            use_cyclic_u=False,
            **kwargs,
        )

    @staticmethod
    def create_line(length, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.Distance,
            Simple_length=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(length)
            ).value,
            Simple_center=True,
            use_cyclic_u=False,
            **kwargs,
        )

    @staticmethod
    def create_angle(length, angle, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.Angle,
            Simple_length=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(length)
            ).value,
            Simple_angle=Angle.from_string(angle).to_degrees().value,
            use_cyclic_u=False,
            **kwargs,
        )

    @staticmethod
    def create_circle(radius, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.Circle,
            Simple_radius=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(radius)
            ).value,
            Simple_sides=64,
            **kwargs,
        )

    @staticmethod
    def create_ellipse(radius_x, radius_y, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.Ellipse,
            Simple_a=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(radius_x)
            ).value,
            Simple_b=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(radius_y)
            ).value,
            **kwargs,
        )

    @staticmethod
    def create_arc(radius, angle, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.Arc,
            Simple_sides=64,
            Simple_radius=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(radius)
            ).value,
            Simple_startangle=0,
            Simple_endangle=Angle.from_string(angle).to_degrees().value,
            use_cyclic_u=False,
            **kwargs,
        )

    @staticmethod
    def create_sector(radius, angle, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.Sector,
            Simple_sides=64,
            Simple_radius=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(radius)
            ).value,
            Simple_startangle=0,
            Simple_endangle=Angle.from_string(angle).to_degrees().value,
            **kwargs,
        )

    @staticmethod
    def create_segment(outter_radius, inner_radius, angle, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.Segment,
            Simple_sides=64,
            Simple_a=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(outter_radius)
            ).value,
            Simple_b=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(inner_radius)
            ).value,
            Simple_startangle=0,
            Simple_endangle=Angle.from_string(angle).to_degrees().value,
            **kwargs,
        )

    @staticmethod
    def create_rectangle(length, width, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.Rectangle,
            Simple_length=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(length)
            ).value,
            Simple_width=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(width)
            ).value,
            Simple_rounded=0,
            **kwargs,
        )

    @staticmethod
    def create_rhomb(length, width, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.Rhomb,
            Simple_length=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(length)
            ).value,
            Simple_width=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(width)
            ).value,
            Simple_center=True,
            **kwargs,
        )

    @staticmethod
    def create_polygon(number_of_sides, radius, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.Polygon,
            Simple_sides=number_of_sides,
            Simple_radius=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(radius)
            ).value,
            **kwargs,
        )

    @staticmethod
    def create_polygon_ab(number_of_sides, length, width, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.Polygon_ab,
            Simple_sides=number_of_sides,
            Simple_a=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(length)
            ).value,
            Simple_b=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(width)
            ).value,
            **kwargs,
        )

    @staticmethod
    def create_trapezoid(length_upper, length_lower, height, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.Trapezoid,
            Simple_a=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(length_upper)
            ).value,
            Simple_b=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(length_lower)
            ).value,
            Simple_h=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(height)
            ).value,
            **kwargs,
        )

    @staticmethod
    def create_spiral(
        number_of_turns: "int",
        height: DimensionOrItsFloatOrStringValue,
        radius: DimensionOrItsFloatOrStringValue,
        is_clockwise: bool = True,
        radius_end: Optional[DimensionOrItsFloatOrStringValue] = None,
        **kwargs,
    ):
        enable_curve_extra_objects_addon()

        heightMeters = (
            blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(height)
            ).value
        )

        radiusMeters = (
            blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(radius)
            ).value
        )

        radius_endMeters = (
            blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(radius_end)
            )
            if radius_end
            else None
        )

        radiusDiff = (
            0 if radius_endMeters is None else (radius_endMeters - radiusMeters).value
        )

        curve_type: blender_definitions.BlenderCurveTypes = (
            kwargs["curve_type"]
            if "curve_type" in kwargs and kwargs["curve_type"]
            else blender_definitions.BlenderCurvePrimitiveTypes.Spiral.get_default_curve_type()
        )

        curve_typeName: str = curve_type.name

        bpy.ops.curve.spirals(
            spiral_type="ARCH",  # type: ignore
            turns=number_of_turns,
            steps=24,
            edit_mode=False,
            radius=radiusMeters,
            dif_z=heightMeters / number_of_turns,
            dif_radius=radiusDiff,
            curve_type=curve_typeName,
            spiral_direction="CLOCKWISE" if is_clockwise else "COUNTER_CLOCKWISE",
        )


def enable_curve_extra_objects_addon():
    addon_name = "add_curve_extra_objects"

    # check if the addon is enabled, enable it if it is not.
    addon = bpy.context.preferences.addons.get(addon_name)
    if addon is None:
        addon_set_enabled(addon_name, True)
        addon = bpy.context.preferences.addons.get(addon_name)

    assert (
        addon is not None
    ), f"Could not enable the {addon_name} addon to create simple curves"


# assumes add_curve_extra_objects is enabled
# https://github.com/blender/blender-addons/blob/master/add_curve_extra_objects/add_curve_simple.py
def create_simple_curve(
    curve_primitiveType: blender_definitions.BlenderCurvePrimitiveTypes, **kwargs
):
    curve_type: blender_definitions.BlenderCurveTypes = (
        kwargs["curve_type"]
        if "curve_type" in kwargs and kwargs["curve_type"]
        else curve_primitiveType.get_default_curve_type()
    )

    kwargs.pop("curve_type", None)  # remove curve_type from kwargs

    enable_curve_extra_objects_addon()

    assert isinstance(
        curve_primitiveType, blender_definitions.BlenderCurvePrimitiveTypes
    ), "{} is not a known curve primitive. Options: {}".format(
        curve_primitiveType,
        [b.name for b in blender_definitions.BlenderCurvePrimitiveTypes],
    )

    assert isinstance(
        curve_type, blender_definitions.BlenderCurveTypes
    ), "{} is not a known simple curve type. Options: {}".format(
        curve_type, [b.name for b in blender_definitions.BlenderCurveTypes]
    )

    # Make sure an object or curve with the same name don't already exist:
    blenderObject = bpy.data.objects.get(curve_primitiveType.name)
    blender_curve = bpy.data.curves.get(curve_primitiveType.name)

    assert (
        blenderObject is None
    ), f"An object with name {curve_primitiveType.name} already exists."
    assert (
        blender_curve is None
    ), f"A curve with name {curve_primitiveType.name} already exists."

    # Default values:
    # bpy.ops.curve.simple(align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), Simple=True, Simple_Change=False, Simple_Delete="", Simple_Type='Point', Simple_endlocation=(2, 2, 2), Simple_a=2, Simple_b=1, Simple_h=1, Simple_angle=45, Simple_startangle=0, Simple_endangle=45, Simple_sides=3, Simple_radius=1, Simple_center=True, Simple_degrees_or_radians='Degrees', Simple_width=2, Simple_length=2, Simple_rounded=0, shape='2D', outputType='BEZIER', use_cyclic_u=True, endp_u=True, order_u=4, handleType='VECTOR', edit_mode=True)
    bpy.ops.curve.simple(
        Simple_Type=curve_primitiveType.name,
        outputType=curve_type.name,  # type: ignore
        order_u=2,
        shape="2D",
        edit_mode=False,
        **kwargs,
    )


def set_curve_use_path(curve_name: str, is_use_path: bool):
    curveObject = get_object(curve_name)

    curve: bpy.types.Curve = curveObject.data  # type: ignore

    curve.use_path = is_use_path


# MARK: manipulating the Scene

# locks the scene interface


def scene_lock_interface(is_locked: bool):
    bpy.context.scene.render.use_lock_interface = is_locked


def set_default_unit(
    blender_unit: blender_definitions.BlenderLength, scene_name="Scene"
):
    blenderScene = bpy.data.scenes.get(scene_name)

    assert blenderScene is not None, f"Scene {scene_name} does not exist"

    blenderScene.unit_settings.system = blender_unit.get_system()
    blenderScene.unit_settings.length_unit = blender_unit.name


def select_object(object_name: str):
    blenderObject = get_object(object_name)

    blenderObject.select_set(True)


def get_selected_object_name() -> str:
    selectedObjects = bpy.context.selected_objects

    assert len(selectedObjects) > 0, "There are no selected objects."

    return selectedObjects[0].name


def get_context_view_3d(**kwargs):
    window = bpy.context.window_manager.windows[0]
    for area in window.screen.areas:
        if area.type == "VIEW_3D":
            for region in area.regions:
                if region.type == "WINDOW":
                    return bpy.context.temp_override(
                        window=window, area=area, region=region, **kwargs
                    )
    raise Exception("Could not find a VIEW_3D region.")


def zoom_to_selected_objects():
    bpy.context.view_layer.update()
    # References https://blender.stackexchange.com/a/7419/138679
    with get_context_view_3d():
        bpy.ops.view3d.view_selected(use_all_regions=True)
        return


def add_dependency_graph_update_listener(callback):
    bpy.app.handlers.depsgraph_update_post.append(callback)  # type: ignore


def add_timer(callback):
    bpy.app.timers.register(callback)


def get_material(
    material_name: str,
) -> bpy.types.Material:
    blenderMaterial = bpy.data.materials.get(material_name)

    assert blenderMaterial is not None, f"Material {material_name} does not exist."

    return blenderMaterial


def create_material(
    new_material_name: str,
):
    material = bpy.data.materials.get(new_material_name)

    assert material is None, f"Material with name {material} already exists."

    material = bpy.data.materials.new(name=new_material_name)

    return material


def set_material_color(material_name: str, r_value, g_value, b_value, a_value=1.0):
    if isinstance(r_value, int):
        r_value /= 255.0

    if isinstance(g_value, int):
        g_value /= 255.0

    if isinstance(b_value, int):
        b_value /= 255.0

    if isinstance(a_value, int):
        a_value /= 255.0

    material = get_material(material_name)

    material.diffuse_color = (r_value, g_value, b_value, a_value)

    return material


def set_material_metallicness(material_name: str, value: float):
    material = get_material(material_name)
    material.metallic = value


def set_material_roughness(material_name: str, value: float):
    material = get_material(material_name)
    material.roughness = value


def set_material_specularness(material_name: str, value: float):
    material = get_material(material_name)
    material.specular_intensity = value


def set_material_to_object(
    material_name: str,
    object_name: str,
):
    material = get_material(material_name)

    object = get_object(object_name)

    mesh: bpy.types.Mesh = object.data  # type: ignore

    objectMaterial = mesh.materials

    if len(objectMaterial) == 0:
        objectMaterial.append(material)
    else:
        objectMaterial[0] = material

    return material


def get_blender_version() -> tuple:
    return bpy.app.version  # type: ignore


fileExportFunctions = {
    "stl": lambda file_path, scale: bpy.ops.export_mesh.stl(
        filepath=file_path, use_selection=True, global_scale=scale
    ),
    "obj": lambda file_path, scale: bpy.ops.wm.obj_export(
        filepath=file_path, export_selected_objects=True, global_scale=scale
    )
    if get_blender_version() >= blender_definitions.BlenderVersions.THREE_DOT_ONE.value
    else bpy.ops.export_scene.obj(
        filepath=file_path, use_selection=True, global_scale=scale
    ),
}


def export_object(object_name: str, file_path: str, overwrite=True, scale=1.0):
    path = Path(file_path).resolve()

    # Check if the file exists:
    if not overwrite:
        assert not path.is_file(), f"File {file_path} already exists"

    bpy.ops.object.select_all(action="DESELECT")

    blenderObject = get_object(object_name)

    blenderObject.select_set(True)

    # Check if this is a file-type we support:
    file_type = path.suffix.replace(".", "")

    assert file_type in fileImportFunctions, f"File type {file_type} is not supported"

    # export the file:
    isSuccess = fileExportFunctions[file_type](file_path, scale) == {"FINISHED"}

    assert isSuccess is True, f"Could not export {file_path}"


# TODO: bind this to blender_provider
def separate_object(object_name):
    bpy.ops.object.select_all(action="DESELECT")

    blenderObject = get_object(object_name)

    blenderObject.select_set(True)

    isSuccess = bpy.ops.mesh.separate(type="LOOSE") == {"FINISHED"}

    assert isSuccess is True, "Could not separate object"


# MARK: Animation


def add_keyframe_to_object(object_name: str, frame_number: int, data_path: str):
    blenderObject = get_object(object_name)

    # Acts on https://docs.blender.org/api/current/bpy.types.Keyframe.html
    blenderObject.keyframe_insert(data_path=data_path, frame=frame_number)


def set_frame_start(frame_number: int, scene_name: Optional[str]):
    scene = get_scene(scene_name)
    scene.frame_start = frame_number


def set_frame_end(frame_number: int, scene_name: Optional[str]):
    scene = get_scene(scene_name)
    scene.frame_end = frame_number


def set_frame_step(step: int, scene_name: Optional[str]):
    scene = get_scene(scene_name)
    scene.frame_step = step


def set_frame_current(frame_number: int, scene_name: Optional[str]):
    scene = get_scene(scene_name)
    scene.frame_set(frame_number)


# def getTexture(textureName):
# 	blenderTexture = bpy.data.textures.get(textureName)

# 	assert \
# 		blenderTexture is not None, \
# 			f"Texture {textureName} does not exist."

# 	return blenderTexture


# def createImageTexture(textureName, image_file_path, repeatMode:blender_definitions.RepeatMode):
#   image = bpy.data.images.load(image_file_path)
#   blenderTexture = bpy.data.textures.new(name=textureName, type="IMAGE")
#   blenderTexture.image = image
#   blenderTexture.extension = repeatMode.getBlenderName

# ref https://blender.stackexchange.com/questions/118646/add-a-texture-to-an-object-using-python-and-blender-2-8/129014#129014


def add_texture_to_material(
    material_name: str,
    image_file_path: str,
):
    material = get_material(material_name)
    material.use_nodes = True
    bsdf = material.node_tree.nodes["Principled BSDF"]
    texImage: bpy.types.ShaderNodeTexImage = material.node_tree.nodes.new(
        "ShaderNodeTexImage"
    )  # type: ignore
    image = bpy.data.images.load(image_file_path)
    texImage.image = image
    material.node_tree.links.new(bsdf.inputs["Base Color"], texImage.outputs["Color"])


def log_message(
    message: str,
):
    bpy.ops.code_to_cad.log_message(message=message)  # type: ignore


def create_light(obj_name: str, energy_level, type):
    light_data = bpy.data.lights.new(name=obj_name, type=type)
    setattr(light_data, "energy", energy_level)
    create_object(obj_name, data=light_data)
    assign_object_to_collection(obj_name)


def get_light(
    light_name: str,
):
    blenderLight = bpy.data.lights.get(light_name)

    assert blenderLight is not None, f"Light {light_name} does not exist."

    return blenderLight


def set_light_color(light_name: str, r_value, g_value, b_value):
    if isinstance(r_value, int):
        r_value /= 255.0

    if isinstance(g_value, int):
        g_value /= 255.0

    if isinstance(b_value, int):
        b_value /= 255.0

    light = get_light(light_name)

    light.color = (r_value, g_value, b_value)

    return light


def create_camera(obj_name: str, type):
    camera_data = bpy.data.cameras.new(name=obj_name)
    create_object(obj_name, data=camera_data)
    assign_object_to_collection(obj_name)


def get_camera(
    camera_name: str,
):
    blenderCamera = bpy.data.cameras.get(camera_name)

    assert blenderCamera is not None, f"Camera {camera_name} does not exist."

    return blenderCamera


def set_scene_camera(camera_name: str, scene_name: Optional[str] = None):
    blenderCamera = get_object(camera_name)
    scene = get_scene(scene_name)

    scene.camera = blenderCamera


def set_focal_length(camera_name: str, length=50.0):
    camera = get_camera(camera_name)
    assert length >= 1, "Length needs to be greater than or equal to 1."

    camera.lens = length


def add_hdr_texture(
    scene_name: str,
    image_file_path: str,
):
    delete_nodes(scene_name)
    nodeBackground = create_nodes(scene_name, "ShaderNodeBackground")
    nodeEnvironment: bpy.types.ShaderNodeTexEnvironment = create_nodes(
        scene_name, "ShaderNodeTexEnvironment"
    )  # type: ignore
    nodeEnvironment.image = bpy.data.images.load(image_file_path)
    nodeEnvironment.location = 0, 0
    nodeOutput = create_nodes(scene_name, "ShaderNodeOutputWorld")
    nodeOutput.location = 0, 0
    links = get_node_tree(scene_name).links
    links.new(nodeEnvironment.outputs["Color"], nodeBackground.inputs["Color"])
    links.new(nodeBackground.outputs["Background"], nodeOutput.inputs["Surface"])


def get_node_tree(
    scene_name: str,
) -> bpy.types.NodeTree:
    scene = get_scene(scene_name)
    nodeTree = scene.world.node_tree
    return nodeTree


def delete_nodes(
    scene_name: str,
):
    nodes = get_node_tree(scene_name).nodes
    nodes.clear()


def create_nodes(scene_name: str, type) -> bpy.types.Node:
    nodes = get_node_tree(scene_name).nodes.new(type=type)
    return nodes


def set_background_location(scene_name: str, x, y):
    envTexture: bpy.types.ShaderNodeTexEnvironment = get_node_tree(
        scene_name
    ).nodes.get(
        "Environment Texture"
    )  # type: ignore
    envTexture.location = x, y


def get_scene(scene_name: Optional[str] = "Scene") -> bpy.types.Scene:
    blenderScene = bpy.data.scenes.get(scene_name or "Scene")

    assert blenderScene is not None, f"Scene{scene_name} does not exists"

    return blenderScene


def render_image(output_filepath: str, overwrite: bool):
    bpy.context.scene.render.use_overwrite = overwrite
    bpy.context.scene.render.filepath = output_filepath
    bpy.ops.render.render(write_still=True)


def render_animation(output_filepath: str, overwrite: bool):
    bpy.context.scene.render.use_overwrite = overwrite
    bpy.context.scene.render.filepath = output_filepath
    bpy.ops.render.render(animation=True)


def set_render_frame_rate(rate: int):
    bpy.context.scene.render.fps = rate


def set_render_quality(percentage: int):
    bpy.context.scene.render.image_settings.quality = percentage


def set_render_file_format(format: blender_definitions.FileFormat):
    bpy.context.scene.render.image_settings.file_format = format.name


def set_render_engine(engine: blender_definitions.RenderEngines):
    bpy.context.scene.render.engine = engine.name


def set_render_resolution(x: int, y: int):
    bpy.context.scene.render.resolution_x = x
    bpy.context.scene.render.resolution_y = y
