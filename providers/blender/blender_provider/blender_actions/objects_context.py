from providers.blender.blender_provider import blender_definitions
from providers.blender.blender_provider.blender_actions.context import (
    get_context_view_3d,
    update_view_layer,
)
from providers.blender.blender_provider.blender_actions.objects import get_object


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
