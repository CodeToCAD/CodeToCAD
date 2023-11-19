from typing import Any, Optional
from uuid import uuid4
import bpy
import mathutils
from codetocad.codetocad_types import (
    AngleOrItsFloatOrStringValue,
    DimensionOrItsFloatOrStringValue,
)
from codetocad.core.angle import Angle
from codetocad.core.dimension import Dimension
from codetocad.core.point import Point
from .. import blender_definitions

from codetocad.utilities import get_dimension_list_from_string_list


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

    from . import addon_set_enabled

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

    return bpy.ops.mesh.primitive_gear(
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
    [currentCollection] = blenderObject.users_collection

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

    blenderObjectChildren: list[bpy.types.Object] = blenderObject.children

    for child in blenderObjectChildren:
        if f"{old_namePrefix}_" in child.name and child.type == "EMPTY":
            update_object_name(
                child.name,
                child.name.replace(f"{old_namePrefix}_", f"{new_namePrefix}_"),
            )


def remove_object(existing_object_name: str, remove_children=False):
    blenderObject = get_object(existing_object_name)

    if remove_children:
        blenderObjectChildren: list[bpy.types.Object] = blenderObject.children
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
    from . import get_context_view_3d, update_view_layer

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
    from . import assign_object_to_collection

    existingCurveObject = get_object(existing_curve_object_name)

    if new_object_name is None:
        update_object_name(existing_curve_object_name, str(uuid4()))
        new_object_name = existing_curve_object_name

    dependencyGraph = bpy.context.evaluated_depsgraph_get()
    evaluatedObject: bpy.types.Object = existingCurveObject.evaluated_get(
        dependencyGraph
    )
    mesh: bpy.types.Mesh = bpy.data.meshes.new_from_object(
        evaluatedObject, depsgraph=dependencyGraph
    )

    blenderObject = create_object(new_object_name, mesh)

    blenderObject.matrix_world = existingCurveObject.matrix_world

    assign_object_to_collection(new_object_name)

    existingCurveObjectChildren: list[bpy.types.Object] = existingCurveObject.children
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
    from . import update_view_layer, assign_object_to_collection

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

    fromBlenderObjectChildren: list[bpy.types.Object] = fromBlenderObject.children
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
            child.location = child.location + mathutils.Vector(translation)
            assign_object_to_collection(child.name, defaultCollection)


def duplicate_object(
    existing_object_name: str, new_object_name: str, copy_landmarks: bool = True
):
    from . import assign_object_to_collection

    clonedObject = bpy.data.objects.get(new_object_name)

    assert clonedObject is None, f"Object with name {new_object_name} already exists."

    blenderObject = get_object(existing_object_name)

    clonedObject: bpy.types.Object = blenderObject.copy()
    clonedObject.name = new_object_name
    clonedObject.data = blenderObject.data.copy()
    clonedObject.data.name = new_object_name

    # Link clonedObject to the original object's collection.
    defaultCollection = get_object_collection_name(existing_object_name)

    assign_object_to_collection(new_object_name, defaultCollection)

    if copy_landmarks:
        blenderObjectChildren: list[bpy.types.Object] = blenderObject.children
        for child in blenderObjectChildren:
            if (
                isinstance(child, blender_definitions.BlenderTypes.OBJECT.value)
                and child.type == "EMPTY"
            ):
                newChild: bpy.types.Object = child.copy()
                newChild.name = child.name.replace(
                    existing_object_name, new_object_name
                )
                newChild.parent = clonedObject
                assign_object_to_collection(newChild.name, defaultCollection)


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
            for p in blenderObject.matrix_world.translation
        ]
    )


def get_object_world_pose(
    object_name: str,
) -> list[float]:
    blenderObject = get_object(object_name)

    listOfTuples = [v.to_tuple() for v in list(blenderObject.matrix_world)]

    return [value for values in listOfTuples for value in values]


def get_object(
    object_name: str,
) -> bpy.types.Object:
    blenderObject = bpy.data.objects.get(object_name)

    assert blenderObject is not None, f"Object {object_name} does not exists"

    return blenderObject


def get_object_or_none(
    object_name: str,
) -> Optional[bpy.types.Object]:
    return bpy.data.objects.get(object_name)


def get_objectType(object_name: str) -> blender_definitions.BlenderObjectTypes:
    blenderObject = bpy.data.objects.get(object_name)

    assert blenderObject is not None, f"Object {object_name} does not exists"

    return blender_definitions.BlenderObjectTypes[blenderObject.type]
