import bpy


def update_view_layer():
    """
    This forces Blender to update internal data. Useful for some operations like getting the location matrix of objects, etc..
    """
    bpy.context.view_layer.update()


def apply_dependency_graph(
    blender_object: bpy.types.Object,
):
    """
    Applies the dependency graph to the object and persists its data using .copy()
    This allows us to apply modifiers, UV data, etc.. to the mesh.
    This is different from apply_object_transformations()
    """
    blender_object_evaluated: bpy.types.Object = blender_object.evaluated_get(
        bpy.context.evaluated_depsgraph_get()
    )
    mesh_or_curve = blender_object_evaluated.data

    if not isinstance(mesh_or_curve, (bpy.types.Mesh, bpy.types.Curve)):
        raise NotImplementedError(f"{type(mesh_or_curve)} is not supported")

    blender_object.data = mesh_or_curve.copy()


def select_object(blender_object: bpy.types.Object):
    """
    Attempts to select the object in the Blender UI
    """
    blender_object.select_set(True)


def get_selected_objects() -> list[bpy.types.Object]:
    """
    Attempts to retrieve the selected objects in Blender UI.
    """
    selectedObjects = bpy.context.selected_objects

    return selectedObjects


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
    bpy.app.handlers.depsgraph_update_post.append(callback)


def add_timer(callback):
    bpy.app.timers.register(callback)


def get_blender_version() -> tuple:
    return bpy.app.version


def log_message(
    message: str,
):
    # This calls our addon:
    bpy.ops.codetocad.log_message(message=message)  # type: ignore
