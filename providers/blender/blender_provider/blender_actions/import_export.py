from typing import Optional
import bpy
from providers.blender.blender_provider.blender_actions.context import (
    get_blender_version,
    get_context_view_3d,
    update_view_layer,
)

from pathlib import Path

from codetocad.utilities import get_file_extension
from providers.blender.blender_provider.blender_definitions import BlenderVersions

fileImportFunctions = {
    "stl": lambda file_path: bpy.ops.wm.stl_import(filepath=file_path),
    "ply": lambda file_path: bpy.ops.wm.ply_import(filepath=file_path),
    "svg": lambda file_path: bpy.ops.import_curve.svg(filepath=file_path),
    "png": lambda file_path: bpy.ops.image.open(filepath=file_path),
    "fbx": lambda file_path: bpy.ops.import_scene.fbx(filepath=file_path),
    "gltf": lambda file_path: bpy.ops.import_scene.gltf(filepath=file_path),
    "obj": lambda file_path: bpy.ops.wm.obj_import(
        filepath=file_path, use_split_objects=False
    ),
}


def import_file(file_path: str, file_type: Optional[str] = None) -> str:
    path = Path(file_path).resolve()

    # Check if the file exists:
    assert path.is_file(), f"File {file_path} does not exist"

    fileName = path.stem

    # Make sure an object or mesh with the same name don't already exist:
    blender_object = bpy.data.objects.get(fileName)
    blenderMesh = bpy.data.meshes.get(fileName)

    assert blender_object is None, f"An object with name {fileName} already exists."
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


fileExportFunctions = {
    "stl": lambda file_path, scale: bpy.ops.wm.stl_export(
        filepath=file_path, export_selected_objects=True, global_scale=scale
    ),
    "obj": lambda file_path, scale: (
        bpy.ops.wm.obj_export(
            filepath=file_path, export_selected_objects=True, global_scale=scale
        )
        if get_blender_version() >= BlenderVersions.THREE_DOT_ONE.value
        else bpy.ops.wm.obj_export(filepath=file_path, global_scale=scale)
    ),
}


def export_object(
    blender_object: bpy.types.Object, file_path: str, overwrite=True, scale=1.0
):
    path = Path(file_path).resolve()

    # Check if the file exists:
    if not overwrite:
        assert not path.is_file(), f"File {file_path} already exists"

    bpy.ops.object.select_all(action="DESELECT")

    blender_object.select_set(True)

    # Check if this is a file-type we support:
    file_type = path.suffix.replace(".", "")

    assert file_type in fileImportFunctions, f"File type {file_type} is not supported"

    # export the file:
    isSuccess = fileExportFunctions[file_type](file_path, scale) == {"FINISHED"}

    assert isSuccess is True, f"Could not export {file_path}"
