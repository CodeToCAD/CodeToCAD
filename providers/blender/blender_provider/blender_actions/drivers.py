import bpy

from . import get_object


def create_driver(object_name: str, path: str, index=-1):
    blenderObject = get_object(object_name)

    return blenderObject.driver_add(path, index).driver


def remove_driver(object_name: str, path: str, index=-1):
    blenderObject = get_object(object_name)

    blenderObject.driver_remove(path, index)


def get_driver(
    object_name: str,
    path: str,
):
    blenderObject = get_object(object_name)

    # this returns an FCurve object
    # https://docs.blender.org/api/current/bpy.types.FCurve.html
    fcurve = blenderObject.animation_data.drivers.find(path)

    assert fcurve is not None, f"Could not find driver {path} for object {object_name}."

    return fcurve.driver


def set_driver(
    driver: bpy.types.Driver,
    driver_type,  # : blender_definitions.BlenderDriverTypes,
    expression="",
):
    driver.type = driver_type

    driver.expression = expression if expression else ""


def set_driver_variable_single_prop(
    driver: bpy.types.Driver,
    variable_name: str,
    target_object_name: str,
    target_data_path: str,
):
    variable = driver.variables.get(variable_name)

    if variable is None:
        variable = driver.variables.new()
        driver.variables[-1].name = variable_name

    variable.type = "SINGLE_PROP"

    target_object = get_object(target_object_name)

    variable.targets[0].id = target_object

    variable.targets[0].data_path = target_data_path


def set_driver_variable_transforms(
    driver: bpy.types.Driver,
    variable_name: str,
    target_object_name: str,
    transform_type,  # : blender_definitions.BlenderDriverVariableTransformTypes,
    transform_space,  # : blender_definitions.BlenderDriverVariableTransformSpaces
):
    variable = driver.variables.get(variable_name)

    if variable is None:
        variable = driver.variables.new()
        driver.variables[-1].name = variable_name

    variable.type = "‘TRANSFORMS’"

    target_object = get_object(target_object_name)

    variable.targets[0].id = target_object

    variable.targets[0].transform_type = transform_type

    variable.targets[0].transform_space = transform_space


def set_driver_variable_location_difference(
    driver: bpy.types.Driver,
    variable_name: str,
    target1_object_name: str,
    target2_object_name: str,
):
    variable = driver.variables.get(variable_name)

    if variable is None:
        variable = driver.variables.new()
        driver.variables[-1].name = variable_name

    variable.type = "‘LOC_DIFF’"

    target1Object = get_object(target1_object_name)

    variable.targets[0].id = target1Object

    target2Object = get_object(target2_object_name)

    variable.targets[1].id = target2Object


def set_driver_variable_rotation_difference(
    driver: bpy.types.Driver,
    variable_name: str,
    target1_object_name: str,
    target2_object_name: str,
):
    variable = driver.variables.get(variable_name)

    if variable is None:
        variable = driver.variables.new()
        driver.variables[-1].name = variable_name

    variable.type = "‘ROTATION_DIFF’"

    target1Object = get_object(target1_object_name)

    variable.targets[0].id = target1Object

    target2Object = get_object(target2_object_name)

    variable.targets[1].id = target2Object
