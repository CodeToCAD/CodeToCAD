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
    get_object_world_location,
)
from providers.blender.blender_provider.blender_actions.transformations import (
    translate_object,
)
from providers.blender.blender_provider.blender_definitions import (
    BlenderConstraintTypes,
    BlenderLength,
    BlenderTranslationTypes,
)


def get_constraint(
    blender_object: bpy.types.Object, constraint_name
) -> bpy.types.Constraint | None:
    """
    Get contraint from Blender
    """
    return blender_object.constraints.get(constraint_name)


def apply_constraint(
    blender_object: bpy.types.Object,
    constraint_type: BlenderConstraintTypes,
    **kwargs,
):
    constraint_name = kwargs.get("name") or constraint_type.get_default_blender_name()

    constraint = get_constraint(blender_object, constraint_name)

    # If it doesn't exist, create it:
    if constraint is None:
        constraint = blender_object.constraints.new(constraint_type.name)

    # Apply every parameter passed in for modifier:
    for key, value in kwargs.items():
        setattr(constraint, key, value)


def apply_limit_location_constraint(
    blender_object: bpy.types.Object,
    x: list[Dimension | None] | None,
    y: list[Dimension | None] | None,
    z: list[Dimension | None] | None,
    relative_to_object: bpy.types.Object | None,
    **kwargs,
):

    [minX, maxX] = x or [None, None]
    [minY, maxY] = y or [None, None]
    [minZ, maxZ] = z or [None, None]

    keyword_args = kwargs or {}

    keyword_args["name"] = BlenderConstraintTypes.LIMIT_LOCATION.format_constraint_name(
        blender_object.name, relative_to_object.name if relative_to_object else ""
    )

    keyword_args["owner_space"] = "CUSTOM" if relative_to_object else "WORLD"

    keyword_args["space_object"] = relative_to_object

    keyword_args["use_transform_limit"] = True

    if minX:
        keyword_args["use_min_x"] = True
        keyword_args["min_x"] = minX.value
    if minY:
        keyword_args["use_min_y"] = True
        keyword_args["min_y"] = minY.value
    if minZ:
        keyword_args["use_min_z"] = True
        keyword_args["min_z"] = minZ.value
    if maxX:
        keyword_args["use_max_x"] = True
        keyword_args["max_x"] = maxX.value
    if maxY:
        keyword_args["use_max_y"] = True
        keyword_args["max_y"] = maxY.value
    if maxZ:
        keyword_args["use_max_z"] = True
        keyword_args["max_z"] = maxZ.value

    apply_constraint(
        blender_object,
        BlenderConstraintTypes.LIMIT_LOCATION,
        **keyword_args,
    )


def apply_limit_rotation_constraint(
    blender_object: bpy.types.Object,
    x: list[Angle | None] | None,
    y: list[Angle | None] | None,
    z: list[Angle | None] | None,
    relative_to_object: bpy.types.Object | None,
    **kwargs,
):

    [minX, maxX] = x or [None, None]
    [minY, maxY] = y or [None, None]
    [minZ, maxZ] = z or [None, None]

    keyword_args = kwargs or {}

    keyword_args["name"] = BlenderConstraintTypes.LIMIT_ROTATION.format_constraint_name(
        blender_object.name, relative_to_object.name if relative_to_object else ""
    )

    keyword_args["owner_space"] = "CUSTOM" if relative_to_object else "WORLD"

    keyword_args["space_object"] = relative_to_object

    keyword_args["use_transform_limit"] = True

    if minX:
        keyword_args["use_limit_x"] = True
        keyword_args["min_x"] = minX.to_radians().value
    if minY:
        keyword_args["use_limit_y"] = True
        keyword_args["min_y"] = minY.to_radians().value
    if minZ:
        keyword_args["use_limit_z"] = True
        keyword_args["min_z"] = minZ.to_radians().value
    if maxX:
        keyword_args["use_limit_x"] = True
        keyword_args["max_x"] = maxX.to_radians().value
    if maxY:
        keyword_args["use_limit_y"] = True
        keyword_args["max_y"] = maxY.to_radians().value
    if maxZ:
        keyword_args["use_limit_z"] = True
        keyword_args["max_z"] = maxZ.to_radians().value

    apply_constraint(
        blender_object,
        BlenderConstraintTypes.LIMIT_ROTATION,
        **keyword_args,
    )


def apply_copy_location_constraint(
    blender_object: bpy.types.Object,
    copied_blender_object: bpy.types.Object,
    copy_x: bool,
    copy_y: bool,
    copy_z: bool,
    use_offset: bool,
    **kwargs,
):
    apply_constraint(
        blender_object,
        BlenderConstraintTypes.COPY_LOCATION,
        name=BlenderConstraintTypes.COPY_LOCATION.format_constraint_name(
            blender_object.name, copied_blender_object.name
        ),
        target=copied_blender_object,
        use_x=copy_x,
        use_y=copy_y,
        use_z=copy_z,
        use_offset=use_offset,
        **kwargs,
    )


def apply_copy_rotation_constraint(
    blender_object: bpy.types.Object,
    copied_blender_object: bpy.types.Object,
    copy_x: bool,
    copy_y: bool,
    copy_z: bool,
    **kwargs,
):
    apply_constraint(
        blender_object,
        BlenderConstraintTypes.COPY_ROTATION,
        name=BlenderConstraintTypes.COPY_ROTATION.format_constraint_name(
            blender_object.name, copied_blender_object.name
        ),
        target=copied_blender_object,
        use_x=copy_x,
        use_y=copy_y,
        use_z=copy_z,
        mix_mode="BEFORE",
        **kwargs,
    )


def apply_pivot_constraint(
    blender_object: bpy.types.Object, pivot_blender_object: bpy.types.Object, **kwargs
):
    apply_constraint(
        blender_object,
        BlenderConstraintTypes.PIVOT,
        name=BlenderConstraintTypes.PIVOT.format_constraint_name(
            blender_object.name, pivot_blender_object.name
        ),
        target=pivot_blender_object,
        rotation_range="ALWAYS_ACTIVE",
        **kwargs,
    )


def apply_gear_constraint(
    blender_object: bpy.types.Object,
    gear_blender_object: bpy.types.Object,
    ratio: float = 1,
    **kwargs,
):
    for axis in Axis:
        # e.g. constraints["Limit Location"].min_x
        driver = create_driver(blender_object, "rotation_euler", axis.value)
        set_driver(driver, "SCRIPTED", f"{-1*ratio} * gearRotation")
        set_driver_variable_single_prop(
            driver, "gearRotation", gear_blender_object, f"rotation_euler[{axis.value}]"
        )


def translate_landmark_onto_another(
    object_to_translate: bpy.types.Object,
    object1_landmark: bpy.types.Object,
    object2_landmark: bpy.types.Object,
):
    update_view_layer()
    object1LandmarkLocation = get_object_world_location(object1_landmark)
    object2LandmarkLocation = get_object_world_location(object2_landmark)

    translation = (object1LandmarkLocation) - (object2LandmarkLocation)

    blender_default_unit = BlenderLength.DEFAULT_BLENDER_UNIT.value

    translate_object(
        object_to_translate,
        [
            Dimension(translation.x.value, blender_default_unit),
            Dimension(translation.y.value, blender_default_unit),
            Dimension(translation.z.value, blender_default_unit),
        ],
        BlenderTranslationTypes.ABSOLUTE,
    )
