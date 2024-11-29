from codetocad.core.angle import Angle
from codetocad.core.dimension import Dimension
from codetocad.enums.axis import Axis
from providers.blender.blender_provider.blender_definitions import (
    BlenderBooleanTypes,
    BlenderLength,
    BlenderModifiers,
    BlenderTypes,
)
import bpy


def clear_modifiers(
    blender_object: bpy.types.Object,
):
    blender_object.modifiers.clear()


def apply_modifier(
    blender_object: bpy.types.Object, modifier: BlenderModifiers, **kwargs
):
    # references https://docs.blender.org/api/current/bpy.types.BooleanModifier.html?highlight=boolean#bpy.types.BooleanModifier and https://docs.blender.org/api/current/bpy.types.ObjectModifiers.html#bpy.types.ObjectModifiers and https://docs.blender.org/api/current/bpy.types.Modifier.html#bpy.types.Modifier
    blenderModifier = blender_object.modifiers.new(
        type=modifier.name, name=modifier.name
    )

    # blenderModifier.show_viewport = False

    # Apply every parameter passed in for modifier:
    for key, value in kwargs.items():
        setattr(blenderModifier, key, value)


def apply_decimate_modifier(blender_object: bpy.types.Object, amount: int):
    apply_modifier(
        blender_object,
        BlenderModifiers.DECIMATE,
        decimate_type="UNSUBDIV",
        iterations=amount,
    )


def apply_bevel_modifier(
    blender_object: bpy.types.Object,
    radius: Dimension,
    vertex_group_name=None,
    use_edges=True,
    use_width=False,
    chamfer=False,
    **kwargs,
):
    apply_modifier(
        blender_object,
        BlenderModifiers.BEVEL,
        affect="EDGES" if use_edges else "VERTICES",
        offset_type="WIDTH" if use_width else "OFFSET",
        width=radius.value,
        segments=1 if chamfer else 24,
        limit_method="VGROUP" if vertex_group_name else "ANGLE",
        vertex_group=vertex_group_name or "",
        **kwargs,
    )


def apply_linear_pattern(
    blender_object: bpy.types.Object,
    instance_count,
    direction: Axis,
    offset: float,
    **kwargs,
):
    offset_array = [0.0, 0.0, 0.0]

    offset_array[direction.value] = offset

    apply_modifier(
        blender_object,
        BlenderModifiers.ARRAY,
        use_relative_offset=False,
        count=instance_count,
        use_constant_offset=True,
        constant_offset_displace=offset_array,
        **kwargs,
    )


def apply_circular_pattern(
    blender_object: bpy.types.Object,
    instance_count: int,
    blender_around_object: bpy.types.Object,
    **kwargs,
):

    apply_modifier(
        blender_object,
        BlenderModifiers.ARRAY,
        count=instance_count,
        use_relative_offset=False,
        use_object_offset=True,
        offset_object=blender_around_object,
        **kwargs,
    )


def apply_solidify_modifier(
    blender_object: bpy.types.Object, thickness: Dimension, **kwargs
):
    apply_modifier(
        blender_object,
        BlenderModifiers.SOLIDIFY,
        thickness=BlenderLength.convert_dimension_to_blender_unit(thickness).value,
        offset=0,
        **kwargs,
    )


def apply_curve_modifier(
    blender_object: bpy.types.Object, curve_blender_object: bpy.types.Object, **kwargs
):
    apply_modifier(
        blender_object,
        BlenderModifiers.CURVE,
        object=curve_blender_object,
        **kwargs,
    )


def apply_boolean_modifier(
    blender_object: bpy.types.Object,
    blender_boolean_type: BlenderBooleanTypes,
    blender_boolean_object: bpy.types.Object,
    **kwargs,
):

    assert isinstance(
        blender_object.data, BlenderTypes.MESH.value
    ), f"Object {blender_object.name} is not an Object. Cannot use the Boolean modifier with {type(blender_object.data)} type."
    assert isinstance(
        blender_boolean_object.data, BlenderTypes.MESH.value
    ), f"Object {blender_boolean_object.name} is not an Object. Cannot use the Boolean modifier with {type(blender_boolean_object.data)} type."

    apply_modifier(
        blender_object,
        BlenderModifiers.BOOLEAN,
        operation=blender_boolean_type.name,
        object=blender_boolean_object,
        use_self=True,
        use_hole_tolerant=True,
        # "solver= "EXACT",
        # "double_threshold= 1e-6,
        **kwargs,
    )


def apply_mirror_modifier(
    blender_object: bpy.types.Object,
    blender_mirror_across_object: bpy.types.Object,
    axis: Axis,
    **kwargs,
):
    axis_list = [False, False, False]
    axis_list[axis.value] = True

    apply_modifier(
        blender_object,
        BlenderModifiers.MIRROR,
        mirror_object=blender_mirror_across_object,
        use_axis=axis_list,
        use_mirror_merge=False,
        **kwargs,
    )


def apply_screw_modifier(
    blender_object: bpy.types.Object,
    angle: Angle,
    axis: Axis,
    screw_pitch: Dimension = Dimension(0),
    iterations=1,
    blender_mirror_across_object: bpy.types.Object | None = None,
    resolution=16,
    **kwargs,
):
    # https://docs.blender.org/api/current/bpy.types.ScrewModifier.html
    properties = {
        "axis": axis.name,
        "angle": angle.value,
        "screw_offset": BlenderLength.convert_dimension_to_blender_unit(
            screw_pitch
        ).value,
        "steps": resolution,
        "render_steps": resolution,
        "use_merge_vertices": True,
        "iterations": iterations,
    }

    if blender_mirror_across_object is not None:
        properties["object"] = blender_mirror_across_object

    apply_modifier(blender_object, BlenderModifiers.SCREW, **properties, **kwargs)
