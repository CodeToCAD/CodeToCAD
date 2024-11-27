from typing import Any, Optional, Type
import bpy
from codetocad.core.angle import Angle
from codetocad.core.dimension import Dimension
from codetocad.core.point import Point
from providers.blender.blender_provider.blender_actions.addons import addon_set_enabled


from codetocad.utilities import get_dimension_list_from_string_list
from providers.blender.blender_provider.blender_definitions import (
    BlenderLength,
    BlenderObjectPrimitiveTypes,
    BlenderObjectTypes,
)


def blender_primitive_function(
    primitive: BlenderObjectPrimitiveTypes, dimensions, **kwargs
):
    primitiveName = primitive.default_name_in_blender()

    # Make sure an object or mesh with the same name don't already exist.
    blender_object = bpy.data.objects.get(primitiveName)
    blenderMesh = bpy.data.meshes.get(primitiveName)

    assert (
        blender_object is None
    ), f"An object with name {primitiveName} already exists."

    orphanMeshMessage = ""
    if blenderMesh is not None and blenderMesh.users == 0:
        orphanMeshMessage += " Your mesh is an orphan, please delete it."

        # issue-182, add a warning for the Default Cube:
        if primitiveName == "Cube":
            orphanMeshMessage += "If you are starting with the Default Cube, please remove both the object and the mesh using Delete Hierarchy (not just Delete), then try again."

    assert (
        blenderMesh is None
    ), f"A mesh with name {primitiveName} already exists. {orphanMeshMessage}"

    if primitive == BlenderObjectPrimitiveTypes.cube:
        return bpy.ops.mesh.primitive_cube_add(
            size=1, scale=[dimension.value for dimension in dimensions[:3]], **kwargs
        )

    if primitive == BlenderObjectPrimitiveTypes.cone:
        return bpy.ops.mesh.primitive_cone_add(
            radius1=dimensions[0].value,
            radius2=dimensions[1].value,
            depth=dimensions[2].value,
            **kwargs,
        )

    if primitive == BlenderObjectPrimitiveTypes.cylinder:
        return bpy.ops.mesh.primitive_cylinder_add(
            radius=dimensions[0].value, depth=dimensions[1].value, **kwargs
        )

    if primitive == BlenderObjectPrimitiveTypes.torus:
        return bpy.ops.mesh.primitive_torus_add(
            mode="EXT_INT",
            abso_minor_rad=dimensions[0].value,
            abso_major_rad=dimensions[1].value,
            **kwargs,
        )

    if primitive == BlenderObjectPrimitiveTypes.sphere:
        return bpy.ops.mesh.primitive_ico_sphere_add(
            radius=dimensions[0].value, **kwargs
        )

    if primitive == BlenderObjectPrimitiveTypes.uvsphere:
        return bpy.ops.mesh.primitive_uv_sphere_add(
            radius=dimensions[0].value, **kwargs
        )

    if primitive == BlenderObjectPrimitiveTypes.circle:
        return bpy.ops.mesh.primitive_circle_add(radius=dimensions[0].value, **kwargs)

    if primitive == BlenderObjectPrimitiveTypes.grid:
        return bpy.ops.mesh.primitive_grid_add(size=dimensions[0].value, **kwargs)

    if primitive == BlenderObjectPrimitiveTypes.monkey:
        return bpy.ops.mesh.primitive_monkey_add(size=dimensions[0].value, **kwargs)

    if primitive == BlenderObjectPrimitiveTypes.empty:
        return bpy.ops.object.empty_add(radius=dimensions[0].value, **kwargs)

    if primitive == BlenderObjectPrimitiveTypes.plane:
        return bpy.ops.mesh.primitive_plane_add(**kwargs)

    raise Exception(f"Primitive with name {primitive.name} is not implemented.")


# Extracts dimensions from a string, then passes them as arguments to the blender_primitive_function
def add_primitive(
    primitive_type: BlenderObjectPrimitiveTypes,
    dimensions: str,
    **kwargs,
):
    assert primitive_type is not None, "Primitive type is required."

    # Convert the dimensions:
    dimensionsList: list[Dimension] = (
        get_dimension_list_from_string_list(dimensions) or []
    )

    dimensionsList = BlenderLength.convert_dimensions_to_blender_unit(dimensionsList)

    # Add the object:
    blender_primitive_function(primitive_type, dimensionsList, **kwargs)


def create_gear(
    object_name: str,
    outer_radius: str | float | Dimension,
    addendum: str | float | Dimension,
    inner_radius: str | float | Dimension,
    dedendum: str | float | Dimension,
    height: str | float | Dimension,
    pressure_angle: str | float | Angle = "20d",
    number_of_teeth: "int" = 12,
    skew_angle: str | float | Angle = 0,
    conical_angle: str | float | Angle = 0,
    crown_angle: str | float | Angle = 0,
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

    outer_radius_dimension = BlenderLength.convert_dimension_to_blender_unit(
        Dimension.from_string(outer_radius)
    ).value
    inner_radius_dimension = BlenderLength.convert_dimension_to_blender_unit(
        Dimension.from_string(inner_radius)
    ).value
    addendum_dimension = BlenderLength.convert_dimension_to_blender_unit(
        Dimension.from_string(addendum)
    ).value
    dedendum_dimension = BlenderLength.convert_dimension_to_blender_unit(
        Dimension.from_string(dedendum)
    ).value
    heightDimension = BlenderLength.convert_dimension_to_blender_unit(
        Dimension.from_string(height)
    ).value

    if addendum_dimension > outer_radius_dimension / 2:
        addendum_dimension = outer_radius_dimension / 2
    if inner_radius_dimension > outer_radius_dimension:
        inner_radius_dimension = outer_radius_dimension
    if dedendum_dimension + inner_radius_dimension > outer_radius_dimension:
        dedendum_dimension = outer_radius_dimension - inner_radius_dimension

    pressure_angleValue = Angle.from_string(pressure_angle).to_radians().value
    skew_angleValue = Angle.from_string(skew_angle).to_radians().value
    conical_angleValue = Angle.from_string(conical_angle).to_radians().value
    crown_angleValue = Angle.from_string(crown_angle).to_radians().value

    return bpy.ops.mesh.primitive_gear(
        name=object_name,
        number_of_teeth=number_of_teeth,
        radius=outer_radius_dimension,
        addendum=addendum_dimension,
        dedendum=dedendum_dimension,
        angle=pressure_angleValue,
        base=inner_radius_dimension,
        width=heightDimension,
        skew=skew_angleValue,
        conangle=conical_angleValue,
        crown=crown_angleValue,
    )


def make_parent(
    name: str,
    parent_name: str,
):
    blender_object = get_object(name)
    blender_parent_object = get_object(parent_name)

    blender_object.parent = blender_parent_object


def update_object_name(
    old_name: str,
    new_name: str,
):
    blender_object = get_object(old_name)

    blender_object.name = new_name


def get_object_collection_name(
    object_name: str,
) -> str:
    blender_object = get_object(object_name)

    # Assumes the first collection is the main collection
    [currentCollection] = blender_object.users_collection

    return currentCollection.name


def update_object_data_name(
    parent_object_name: str,
    new_name: str,
):
    blender_object = get_object(parent_object_name)

    assert (
        blender_object.data is not None
    ), f"Object {parent_object_name} does not have data to name."

    blender_object.data.name = new_name


# This assumes that landmarks are named with format: `{parent_part_name}_{landmarkName}`
def update_object_landmark_names(
    parent_object_name: str,
    old_namePrefix: str,
    new_namePrefix: str,
):
    blender_object = get_object(parent_object_name)

    blender_object_children: list[bpy.types.Object] = blender_object.children

    for child in blender_object_children:
        if f"{old_namePrefix}_" in child.name and child.type == "EMPTY":
            update_object_name(
                child.name,
                child.name.replace(f"{old_namePrefix}_", f"{new_namePrefix}_"),
            )


def remove_data(
    blender_data: (
        bpy.types.Armature
        | bpy.types.Camera
        | bpy.types.Curve
        | bpy.types.Curves
        | bpy.types.GreasePencil
        | bpy.types.GreasePencilv3
        | bpy.types.Lattice
        | bpy.types.Light
        | bpy.types.LightProbe
        | bpy.types.Mesh
        | bpy.types.MetaBall
        | bpy.types.PointCloud
        | bpy.types.Speaker
        | bpy.types.SurfaceCurve
        | bpy.types.TextCurve
        | bpy.types.Volume
    ),
):
    if isinstance(blender_data, bpy.types.Mesh):
        bpy.data.meshes.remove(blender_data)
    elif isinstance(blender_data, (bpy.types.Curve, bpy.types.TextCurve)):
        bpy.data.curves.remove(blender_data)
    else:
        raise NotImplementedError(f"{type(blender_data)} is not supported yet.")


def remove_object(
    existing_object_name: str, remove_children=False, is_remove_data=True
):
    blender_object = get_object(existing_object_name)

    if remove_children:
        blender_object_children: list[bpy.types.Object] = blender_object.children
        for child in blender_object_children:
            try:
                remove_object(child.name, True)
            except Exception as e:
                print(f"Could not remove {child.name}. {e}")

    # Not all objects have data, but if they do, then deleting the data
    # deletes the object
    if blender_object.data and is_remove_data:
        remove_data(blender_object.data)
    else:
        bpy.data.objects.remove(blender_object)


def create_object(name: str, data: Optional[Any] = None):
    """
    Creates an object in Blender. The object will exist in data, but will not appear in the scene until `assign_object_to_collection()` is called.
    """
    blender_object = bpy.data.objects.get(name)

    assert blender_object is None, f"Object {name} already exists"

    return bpy.data.objects.new(name, data)


def create_object_vertex_group(
    object_name: str,
    vertex_group_name: str,
):
    blender_object = get_object(object_name)
    return blender_object.vertex_groups.new(name=vertex_group_name)


def get_object_vertex_group(
    object_name: str,
    vertex_group_name: str,
):
    blender_object = get_object(object_name)
    return blender_object.vertex_groups.get(vertex_group_name)


def add_verticies_to_vertex_group(vertex_group_object, vertex_indecies: list[int]):
    vertex_group_object.add(vertex_indecies, 1.0, "ADD")


def get_object_visibility(
    existing_object_name: str,
) -> bool:
    blender_object = get_object(existing_object_name)

    return blender_object.visible_get()


def set_object_visibility(existing_object_name: str, is_visible: bool):
    blender_object = get_object(existing_object_name)

    # blender_object.hide_viewport = not is_visible
    # blender_object.hide_render = not is_visible
    blender_object.hide_set(not is_visible)


def get_object_local_location(
    object_name: str,
):
    blender_object = get_object(object_name)

    return Point.from_list(
        [
            Dimension(p, BlenderLength.DEFAULT_BLENDER_UNIT.value)
            for p in blender_object.location
        ]
    )


def get_object_world_location(
    object_name: str,
):
    blender_object = get_object(object_name)

    return Point.from_list(
        [
            Dimension(p, BlenderLength.DEFAULT_BLENDER_UNIT.value)
            for p in blender_object.matrix_world.translation
        ]
    )


def get_object_world_pose(
    object_name: str,
) -> list[float]:
    blender_object = get_object(object_name)

    listOfTuples = [v.to_tuple() for v in list(blender_object.matrix_world)]

    return [value for values in listOfTuples for value in values]


def get_object(
    object_name: str,
    of_type: Type[bpy.types.Mesh] | Type[bpy.types.Curve] | None = None,
) -> bpy.types.Object:
    blender_object = get_object_or_none(object_name, of_type)

    assert blender_object is not None, f"Object {object_name} does not exists"

    return blender_object


def get_object_or_none(
    object_name: str,
    of_type: Type[bpy.types.Mesh] | Type[bpy.types.Curve] | None = None,
) -> Optional[bpy.types.Object]:
    blender_object = bpy.data.objects.get(object_name)

    if blender_object and of_type is not None:
        if not blender_object.type == of_type:
            return None

    return blender_object


def get_objectType(object_name: str) -> BlenderObjectTypes:
    blender_object = bpy.data.objects.get(object_name)

    assert blender_object is not None, f"Object {object_name} does not exists"

    return BlenderObjectTypes[blender_object.type]
