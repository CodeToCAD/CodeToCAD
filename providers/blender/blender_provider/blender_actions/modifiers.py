from codetocad.core.angle import Angle
from codetocad.core.dimension import Dimension
from codetocad.enums.axis import Axis
from providers.blender.blender_provider.blender_actions.objects import get_object
import providers.blender.blender_provider.blender_definitions as blender_definitions


def clear_modifiers(
    object_name: str,
):
    blenderObject = get_object(object_name)

    blenderObject.modifiers.clear()


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
