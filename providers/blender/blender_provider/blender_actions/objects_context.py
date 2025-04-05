from typing import Literal
from providers.blender.blender_provider.blender_actions.context import (
    get_context_view_3d,
    update_view_layer,
)
from providers.blender.blender_provider.blender_definitions import (
    BlenderObjectTypes,
)
import bpy


def convert_object_using_ops(
    existing_object: bpy.types.Object, convert_to_type: BlenderObjectTypes
):
    with get_context_view_3d(
        active_object=existing_object, selected_objects=[existing_object]
    ):
        existing_object.select_set(True)
        bpy.context.view_layer.objects.active = existing_object
        update_view_layer()

        convert_to: Literal["MESH", "CURVE"] = convert_to_type.name  # type: ignore

        if not convert_to in ["MESH", "CURVE"]:
            raise NotImplementedError(f"{convert_to} type is not supported")

        bpy.ops.object.convert(target=convert_to)
