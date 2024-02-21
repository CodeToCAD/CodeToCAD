from typing import Optional
import bpy
from codetocad.core.angle import Angle
from codetocad.core.dimension import Dimension
from codetocad.enums.axis import Axis
from providers.blender.blender_provider.blender_actions.context import update_view_layer
from providers.blender.blender_provider.blender_actions.drivers import (
    create_driver,
    set_driver,
    set_driver_variable_single_prop,
)
from providers.blender.blender_provider.blender_actions.objects import (
    get_object,
    get_object_world_location,
)
from providers.blender.blender_provider.blender_actions.transformations import (
    translate_object,
)
import providers.blender.blender_provider.blender_definitions as blender_definitions


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
        set_driver_variable_single_prop(
            driver, "gearRotation", gear_object_name, f"rotation_euler[{axis.value}]"
        )


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
        ],
        blender_definitions.BlenderTranslationTypes.ABSOLUTE,
    )
